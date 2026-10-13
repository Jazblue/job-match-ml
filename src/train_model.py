import pandas as pd
import joblib

from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load job dataset
df = pd.read_csv(r".\data\jobs.csv")

# Prepare job text
df["experience_text"] = (
    df["experience_required"].astype(str) + " years experience"
)

df["text"] = (
    df["job_title"] + " "
    + df["description"] + " "
    + df["skills"] + " "
    + df["experience_text"]
)

X = df["text"]
y = df["match"]

# Build the machine learning pipeline
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression()),
])

# Set up five-fold stratified cross-validation
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42,
)

# Evaluate the model across five folds
scoring = {
    "accuracy": "accuracy",
    "precision": "precision",
    "recall": "recall",
    "f1": "f1",
}

results = cross_validate(
    pipeline,
    X,
    y,
    cv=cv,
    scoring=scoring,
)

# Display cross-validation results
print("JobMatch ML - Five-Fold Cross-Validation")
print("=" * 42)
print(f"Total examples: {len(df)}")
print("Cross-validation folds: 5")
print()

for metric in scoring:
    scores = results[f"test_{metric}"]
    print(
        f"{metric.capitalize():10} "
        f"Mean: {scores.mean():.2%}  "
        f"Std dev: {scores.std():.2%}"
    )

print()
print("Individual fold accuracy:")
for fold, score in enumerate(results["test_accuracy"], start=1):
    print(f"Fold {fold}: {score:.2%}")

# Train the final model using all available examples
pipeline.fit(X, y)

# Save the final trained model
joblib.dump(pipeline, r".\models\jobmatch_model.joblib")