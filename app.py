import re
import sqlite3
import joblib
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

# Load trained model and vectorizer
model = joblib.load("model/phishing_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

SUSPICIOUS_KEYWORDS = [
    "urgent", "click here", "verify", "password", "login", "bank",
    "reset", "account suspended", "immediately", "free", "winner",
    "claim", "security alert", "confirm", "limited time", "offer",
    "deactivated", "reward", "update account", "unusual login",
    "suspended", "act now", "secure your account", "payment failed"
]

TRUSTED_DOMAINS = [
    "gmail.com", "outlook.com", "yahoo.com", "hotmail.com",
    "company.com", "microsoft.com", "google.com", "amazon.com",
    "apple.com", "paypal.com", "jainuniversity.ac.in"
]

BRAND_KEYWORDS = [
    "paypal", "google", "microsoft", "amazon", "apple", "bank", "mastercard"
]


def init_db():
    conn = sqlite3.connect("scan_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_email TEXT,
            subject TEXT,
            body TEXT,
            prediction TEXT,
            risk TEXT,
            probability REAL,
            suspicious_keywords TEXT,
            url_detected TEXT,
            sender_flag TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_scan(sender_email, subject, body, prediction, risk, probability,
              suspicious_keywords, url_detected, sender_flag):
    conn = sqlite3.connect("scan_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scans (
            sender_email, subject, body, prediction, risk, probability,
            suspicious_keywords, url_detected, sender_flag, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        sender_email,
        subject,
        body,
        prediction,
        risk,
        probability,
        ", ".join(suspicious_keywords),
        url_detected,
        sender_flag,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()


def get_scan_history():
    conn = sqlite3.connect("scan_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sender_email, subject, prediction, risk, probability,
               url_detected, sender_flag, created_at
        FROM scans
        ORDER BY id DESC
        LIMIT 10
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def preprocess_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def find_suspicious_keywords(text: str):
    text_lower = text.lower()
    found = [word for word in SUSPICIOUS_KEYWORDS if word in text_lower]
    return found


def detect_urls(text: str) -> bool:
    url_pattern = r"(https?://\S+|www\.\S+)"
    return bool(re.search(url_pattern, text.lower()))


def check_sender_email(sender_email: str):
    if not sender_email:
        return "No sender email provided"

    sender_email = sender_email.lower().strip()

    if "@" not in sender_email:
        return "Invalid sender email"

    domain = sender_email.split("@")[-1]

    # random digits in username
    username = sender_email.split("@")[0]
    digit_count = sum(char.isdigit() for char in username)

    if domain not in TRUSTED_DOMAINS:
        for brand in BRAND_KEYWORDS:
            if brand in domain and domain not in TRUSTED_DOMAINS:
                return "Possible fake branded domain"

        if digit_count >= 4:
            return "Suspicious sender pattern"

        return "Unknown or untrusted domain"

    return "Looks safe"


def get_risk_level(prediction: str, keyword_count: int, url_detected: bool, sender_flag: str) -> str:
    if prediction == "phishing":
        return "High"
    if prediction == "spam":
        if url_detected or sender_flag in ["Possible fake branded domain", "Suspicious sender pattern"]:
            return "High"
        return "Medium"
    if keyword_count >= 3 or url_detected:
        return "Medium"
    return "Low"


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    risk = None
    suspicious_words = []
    subject = ""
    body = ""
    sender_email = ""
    probability = None
    url_detected = False
    sender_flag = ""
    history = get_scan_history()

    if request.method == "POST":
        sender_email = request.form.get("sender_email", "").strip()
        subject = request.form.get("subject", "").strip()
        body = request.form.get("body", "").strip()

        combined_text = f"{subject} {body}".strip()

        if combined_text:
            clean_text = preprocess_text(combined_text)
            text_vector = vectorizer.transform([clean_text])

            prediction = model.predict(text_vector)[0]
            probabilities = model.predict_proba(text_vector)[0]
            class_names = model.classes_

            probability_dict = {
                class_names[i]: round(float(probabilities[i]) * 100, 2)
                for i in range(len(class_names))
            }

            probability = probability_dict.get(prediction, 0.0)

            suspicious_words = find_suspicious_keywords(combined_text)
            url_detected = detect_urls(combined_text)
            sender_flag = check_sender_email(sender_email)
            risk = get_risk_level(prediction, len(suspicious_words), url_detected, sender_flag)

            result = prediction.capitalize()

            save_scan(
                sender_email=sender_email,
                subject=subject,
                body=body,
                prediction=result,
                risk=risk,
                probability=probability,
                suspicious_keywords=suspicious_words,
                url_detected="Yes" if url_detected else "No",
                sender_flag=sender_flag
            )

            history = get_scan_history()

    return render_template(
        "index.html",
        result=result,
        risk=risk,
        suspicious_words=suspicious_words,
        subject=subject,
        body=body,
        sender_email=sender_email,
        probability=probability,
        url_detected=url_detected,
        sender_flag=sender_flag,
        history=history
    )


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)