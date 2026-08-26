import joblib
import os

MODEL_DIR = "app/ml/models"

_category_model = joblib.load(f"{MODEL_DIR}/category_model.joblib")
_category_vectorizer = joblib.load(f"{MODEL_DIR}/category_vectorizer.joblib")
_priority_model = joblib.load(f"{MODEL_DIR}/priority_model.joblib")
_priority_vectorizer = joblib.load(f"{MODEL_DIR}/priority_vectorizer.joblib")


def predict_ticket_labels(text: str) -> dict:
    category_vec = _category_vectorizer.transform([text])
    priority_vec = _priority_vectorizer.transform([text])

    predicted_category = _category_model.predict(category_vec)[0]
    predicted_priority = _priority_model.predict(priority_vec)[0]

    category_confidence = _category_model.predict_proba(category_vec).max()
    priority_confidence = _priority_model.predict_proba(priority_vec).max()

    return {
        "category": predicted_category,
        "priority": predicted_priority,
        "category_confidence": round(float(category_confidence), 3),
        "priority_confidence": round(float(priority_confidence), 3),
    }
