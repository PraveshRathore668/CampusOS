import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import classification_report

DATA_PATH = "app/ml/data/training_data.csv"
MODEL_DIR = "app/ml/models"
os.makedirs(MODEL_DIR, exist_ok=True)


def train_and_evaluate(df, target_column, model_name, use_class_weight=False):
    print(f"\n{'='*60}")
    print(f"Training model for: {target_column}")
    print(f"{'='*60}")

    X = df["text"]
    y = df[target_column]

    vectorizer = TfidfVectorizer()
    X_vec = vectorizer.fit_transform(X)

    class_weight = "balanced" if use_class_weight else None
    model = LogisticRegression(max_iter=1000, class_weight=class_weight)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    y_pred = cross_val_predict(model, X_vec, y, cv=cv)

    print(f"\nTotal examples: {len(y)} (evaluated via 5-fold cross-validation)")
    print(f"class_weight: {class_weight}")
    print("\nClassification Report:")
    print(classification_report(y, y_pred, zero_division=0))

    model.fit(X_vec, y)

    joblib.dump(model, f"{MODEL_DIR}/{model_name}_model.joblib")
    joblib.dump(vectorizer, f"{MODEL_DIR}/{model_name}_vectorizer.joblib")
    print(f"Saved model and vectorizer for '{model_name}'")


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)

    train_and_evaluate(df, "category", "category", use_class_weight=False)
    train_and_evaluate(df, "priority", "priority", use_class_weight=True)

    print("\nTraining complete for both models.")
