import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

df = pd.read_csv(r".\data\jobs.csv")

df["experience_text"] = df["experience_required"].astype(str) + " years experience"

df["text"] = (
    df["job_title"] + " " +
    df["description"] + " " +
    df["skills"] + " " +
    df["experience_text"]
)

X = df["text"]
y = df["match"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression())
])

pipeline.fit(X_train, y_train)

predictions = pipeline.predict(X_test)
probabilities = pipeline.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, predictions)

print("JobMatch ML - Training")
print("----------------------")
print(f"Training examples: {len(y_train)}")
print(f"Testing examples:  {len(y_test)}")
print(f"Accuracy:          {accuracy:.2%}")

joblib.dump(pipeline, r".\models\jobmatch_model.joblib")

print()
print("Model saved to:")
print(r".\models\jobmatch_model.joblib")
