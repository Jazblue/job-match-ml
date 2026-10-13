from pathlib import Path
import json
import joblib

# --------------------------------------------------
# JobMatch ML - Prediction
# --------------------------------------------------

# Scoring weights
ML_WEIGHT = 0.50
SKILL_WEIGHT = 0.30
EXPERIENCE_WEIGHT = 0.20

# Load trained model
model = joblib.load(r".\models\jobmatch_model.joblib")

# Load candidate profile
with open(r".\data\candidate.json", "r") as file:
    candidate = json.load(file)

# --------------------------------------------------
# New job
# --------------------------------------------------
job_path = Path(__file__).resolve().parent.parent / "data" / "job.json"
job = json.loads(job_path.read_text(encoding="utf-8-sig"))

job_title = job["job_title"]
description = job["description"]
job_skills = job["skills"]
experience_required = job["experience_required"]
# --------------------------------------------------
# ML prediction
# --------------------------------------------------

experience_text = f"{experience_required} years experience"

job_text = (
    job_title + " " +
    description + " " +
    ",".join(job_skills) + " " +
    experience_text
)

probability = model.predict_proba([job_text])[0][1]
ml_score = probability * 100

# --------------------------------------------------
# Skill comparison
# --------------------------------------------------

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

# --------------------------------------------------
# Experience comparison
# --------------------------------------------------

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

# --------------------------------------------------
# Final score
# --------------------------------------------------

final_score = (
    ml_score * ML_WEIGHT +
    skill_score * SKILL_WEIGHT +
    experience_score * EXPERIENCE_WEIGHT
)

# --------------------------------------------------
# Rating
# --------------------------------------------------

if final_score >= 75:
    rating = "EXCELLENT MATCH"
elif final_score >= 60:
    rating = "GOOD MATCH"
elif final_score >= 45:
    rating = "BORDERLINE MATCH"
else:
    rating = "POOR MATCH"

# --------------------------------------------------
# Results
# --------------------------------------------------

print("JobMatch ML")
print("===========")
print(f"Job:                {job_title}")
print()
print(f"FINAL MATCH SCORE:  {final_score:.2f}%")
print(f"Rating:             {rating}")
print()
print(f"ML relevance:       {ml_score:.2f}%")
print(f"Skill compatibility:{skill_score:.2f}%")
print(f"Experience fit:     {experience_score:.0f}%")
print()
print("Matched skills:")
for skill in matched_skills:
    print(f"  + {skill}")

print()
print("Missing skills:")
for skill in missing_skills:
    print(f"  - {skill}")

print()
print("Recommendation:")

if final_score >= 75:
    print("  Apply - strong overall match.")
elif final_score >= 60:
    print("  Consider applying - good match with some gaps.")
elif final_score >= 45:
    print("  Review carefully - significant skill gaps may exist.")
else:
    print("  Low priority - this role is not a strong match.")