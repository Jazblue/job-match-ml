
from pathlib import Path
import json
import re

import joblib
from flask import Flask, render_template, request

app = Flask(__name__)

# Resolve paths relative to this file
PROJECT_DIR = Path(__file__).resolve().parent.parent

model = joblib.load(PROJECT_DIR / "models" / "jobmatch_model.joblib")

with open(PROJECT_DIR / "data" / "candidate.json", "r", encoding="utf-8") as file:
    candidate = json.load(file)

ML_WEIGHT = 0.50
SKILL_WEIGHT = 0.30
EXPERIENCE_WEIGHT = 0.20

# Skills this prototype knows how to identify in pasted adverts

KNOWN_SKILLS = [
    # IT and cloud
    "AWS", "Linux", "Networking", "Troubleshooting", "Terraform",
    "Docker", "Windows", "Active Directory", "AD", "IT Support",
    "Cloud Computing", "Cisco", "Python", "CloudWatch", "EC2",
    "S3", "Lambda", "RDS", "SQL", "Kubernetes", "Jenkins",
    "Git", "GitHub", "Microsoft 365", "Azure", "DevOps",

    # Retail and general workplace skills
    "Retail Management", "Retail", "Leadership", "Staff Training",
    "Training", "Stock Control", "Stock Management", "Sales",
    "Communication", "Customer Service", "Customer Complaints",
    "Budgeting", "Team Management", "Recruitment", "Health and Safety",
    "Time Management", "Problem Solving", "Organisation",
    "Project Management", "Data Analysis", "Microsoft Excel",
    "Administration", "Scheduling", "Report Writing"
]



def extract_job_details(advert):
    """Extract basic details from a pasted advert using simple rules."""
    lines = [line.strip() for line in advert.splitlines() if line.strip()]

    title = lines[0][:150] if lines else "Pasted Job Advert"

    found_skills = []
    advert_lower = advert.lower()

    for skill in KNOWN_SKILLS:
        # Match whole words where possible, avoiding partial matches
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"
        if re.search(pattern, advert_lower):
            canonical = "Active Directory" if skill == "AD" else skill
            if canonical not in found_skills:
                found_skills.append(canonical)


    # Find a stated requirement such as "3 years of experience"
    experience_matches = re.findall(
        r"\b(\d+)\+?\s+years?\b[^.\n]*?\bexperience\b",
        advert_lower
    )
    experience = int(experience_matches[0]) if experience_matches else 0


    # Use a reasonable title fallback if the first line is generic
    if title.lower() in {"job advert", "job description", "careers"}:
        title = "Pasted Job Advert"

    return title, found_skills, experience


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        job_advert = request.form.get("job_advert", "").strip()

        if job_advert:
            job_title, job_skills, experience_required = extract_job_details(
                job_advert
            )
            description = job_advert
        else:
            job_title = request.form.get("job_title", "").strip()
            description = request.form.get("description", "").strip()
            raw_skills = request.form.get("skills", "")
            job_skills = [
                skill.strip()
                for skill in raw_skills.split(",")
                if skill.strip()
            ]

            try:
                experience_required = int(request.form.get("experience", "0"))
            except (TypeError, ValueError):
                experience_required = 0

        # Build text for the ML model
        experience_text = f"{experience_required} years experience"
        job_text = (
            job_title + " " + description + " " +
            ",".join(job_skills) + " " + experience_text
        )

        probability = model.predict_proba([job_text])[0][1]
        ml_score = probability * 100

        candidate_skills = {
            skill.strip().lower() for skill in candidate["skills"]
        }

        matched_skills = [
            skill for skill in job_skills
            if skill.strip().lower() in candidate_skills
        ]
        missing_skills = [
            skill for skill in job_skills
            if skill.strip().lower() not in candidate_skills
        ]

        skill_score = (
            len(matched_skills) / len(job_skills) * 100
            if job_skills else 0
        )

        experience_level = candidate["experience_level"]
        experience_gap = experience_required - experience_level

        if experience_gap <= 0:
            experience_score = 100
        elif experience_gap == 1:
            experience_score = 70
        elif experience_gap == 2:
            experience_score = 40
        else:
            experience_score = 20

        final_score = (
            ml_score * ML_WEIGHT +
            skill_score * SKILL_WEIGHT +
            experience_score * EXPERIENCE_WEIGHT
        )

        if final_score >= 75:
            rating = "EXCELLENT MATCH"
            recommendation = "Apply - strong overall match."
        elif final_score >= 60:
            rating = "GOOD MATCH"
            recommendation = (
                "Consider applying - good match with some gaps."
            )
        elif final_score >= 45:
            rating = "BORDERLINE MATCH"
            recommendation = (
                "Review carefully - significant skill gaps may exist."
            )
        else:
            rating = "POOR MATCH"
            recommendation = (
                "Low priority - this role is not a strong match."
            )

        result = {
            "job_title": job_title or "Untitled Job",
            "final_score": final_score,
            "rating": rating,
            "ml_score": ml_score,
            "skill_score": skill_score,
            "experience_score": experience_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "recommendation": recommendation,
        }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
