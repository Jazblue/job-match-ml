from flask import Flask, render_template, request
import joblib
import json

app = Flask(__name__)

# Load trained ML model
model = joblib.load(r".\models\jobmatch_model.joblib")

# Load candidate profile
with open(r".\data\candidate.json", "r") as file:
    candidate = json.load(file)

# Scoring weights
ML_WEIGHT = 0.50
SKILL_WEIGHT = 0.30
EXPERIENCE_WEIGHT = 0.20


@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        job_title = request.form["job_title"]
        description = request.form["description"]

        job_skills = [
            skill.strip()
            for skill in request.form["skills"].split(",")
            if skill.strip()
        ]

        experience_required = int(request.form["experience"])

        # Build text for ML model
        experience_text = f"{experience_required} years experience"

        job_text = (
            job_title + " " +
            description + " " +
            ",".join(job_skills) + " " +
            experience_text
        )

        # ML prediction
        probability = model.predict_proba([job_text])[0][1]
        ml_score = probability * 100

        # Skill comparison
        candidate_skills = {
            skill.strip().lower()
            for skill in candidate["skills"]
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

        # Experience comparison
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

        # Final score
        final_score = (
            ml_score * ML_WEIGHT +
            skill_score * SKILL_WEIGHT +
            experience_score * EXPERIENCE_WEIGHT
        )

        # Rating
        if final_score >= 75:
            rating = "EXCELLENT MATCH"
        elif final_score >= 60:
            rating = "GOOD MATCH"
        elif final_score >= 45:
            rating = "BORDERLINE MATCH"
        else:
            rating = "POOR MATCH"

        # Recommendation
        if final_score >= 75:
            recommendation = "Apply - strong overall match."
        elif final_score >= 60:
            recommendation = "Consider applying - good match with some gaps."
        elif final_score >= 45:
            recommendation = "Review carefully - significant skill gaps may exist."
        else:
            recommendation = "Low priority - this role is not a strong match."

        result = {
            "job_title": job_title,
            "final_score": final_score,
            "rating": rating,
            "ml_score": ml_score,
            "skill_score": skill_score,
            "experience_score": experience_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "recommendation": recommendation
        }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)