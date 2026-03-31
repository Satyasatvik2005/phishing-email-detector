🛡️ Phishing Email Detector

A Machine Learning-based Web Application that detects whether an email is Phishing, Spam, or Legitimate using Natural Language Processing (NLP) techniques and a modern Flask-based dashboard.

🚀 Live Demo

🔗 https://phishing-email-detector.onrender.com

📌 Features
🧠 ML-based Email Classification (Phishing / Spam / Legitimate)
📊 Probability Score (Confidence %)
⚠️ Risk Level Detection (Low / Medium / High)
🔍 Suspicious Keyword Detection
🔗 URL Detection in Email Content
👤 Sender Email Analysis
🗂️ Scan History Storage (SQLite Database)
🎨 Modern Dashboard UI (Glassmorphism Design)
⚡ Real-time Email Analysis
🛠️ Tech Stack
👨‍💻 Backend
Python
Flask
scikit-learn
Pandas
Joblib
🎨 Frontend
HTML
CSS
JavaScript
📊 Machine Learning
TF-IDF Vectorization
Naive Bayes Classifier
🗄️ Database
SQLite
🌐 Deployment
Render
🧠 How It Works
User enters:
Sender Email
Email Subject
Email Body
System performs:
Text preprocessing
TF-IDF feature extraction
ML model prediction
Output:
Email classification
Probability score
Risk level
Suspicious keywords
URL detection
Sender analysis
📂 Project Structure
phishing-email-detector/
│
├── app.py
├── train_model.py
├── dataset.csv
├── requirements.txt
├── Procfile
│
├── model/
│   ├── phishing_model.pkl
│   └── vectorizer.pkl
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── scan_history.db
⚙️ Installation & Setup
1. Clone Repository
git clone https://github.com/YOUR_USERNAME/phishing-email-detector.git
cd phishing-email-detector
2. Install Dependencies
pip install -r requirements.txt
3. Run Application
python app.py
4. Open in Browser
http://127.0.0.1:5000
🧪 Example Inputs
🔴 Phishing Email
Your account has been suspended. Click here immediately to verify your password.
🟡 Spam Email
Get 50% discount today only. Limited time offer.
🟢 Legitimate Email
The meeting is scheduled for tomorrow at 11 AM.
📈 Future Improvements
📊 Model accuracy improvement with larger datasets
🔐 User authentication system
📄 Export scan report (PDF)
📱 Mobile-friendly UI enhancements
☁️ Cloud database integration
🎯 Use Cases
Cybersecurity awareness
Email filtering systems
Fraud detection tools
Educational ML projects
👨‍🎓 Author

Kamisetty Satya Satvik
B.Tech CSE (3rd Year)

⭐ Show your support

If you like this project, please ⭐ star the repository!
