import re
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


def preprocess_text(text: str) -> str:
    """Clean and normalize text."""
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)  # remove URLs
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)           # remove symbols
    text = re.sub(r"\s+", " ", text).strip()              # remove extra spaces
    return text


def main():
    # Load dataset
    df = pd.read_csv("dataset.csv")

    # Check required columns
    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError("dataset.csv must contain 'text' and 'label' columns.")

    # Preprocess text
    df["clean_text"] = df["text"].apply(preprocess_text)

    # Convert text to numerical features
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(df["clean_text"])

    # Labels
    y = df["label"]

    # Train model
    model = MultinomialNB()
    model.fit(X, y)

    # Save model and vectorizer
    joblib.dump(model, "model/phishing_model.pkl")
    joblib.dump(vectorizer, "model/vectorizer.pkl")

    print("Model training completed successfully.")
    print("Saved:")
    print("- model/phishing_model.pkl")
    print("- model/vectorizer.pkl")


if __name__ == "__main__":
    main()