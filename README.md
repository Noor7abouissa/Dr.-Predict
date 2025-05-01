Dr. Predict 🩺

Dr. Predict is a predictive analytics web application designed to help healthcare providers identify patients at high risk of hospital readmission within 30 days of discharge. The system uses machine learning to generate a personalized risk score based on patient information.

🔍 Project Overview

🎯 Goal: Reduce unnecessary hospital readmissions through early prediction.

💡 Solution: Use ML models trained on patient data to calculate a risk score and provide follow-up recommendations.

🛠️ Tech Stack
Frontend: HTML, CSS

Backend: Python (Flask)

Machine Learning: Scikit-learn (SVM model)

Database: MySQL

Deployment: Docker

Version Control: GitHub

🧠 How It Works
User logs in or registers an account.

Adds new patient data (age, gender, diagnosis, visits, smoking status, etc.).

The system calculates a risk score (1–10) using the ML model.

Dashboard displays risk level and recommended follow-up actions.

Users can view, search, and manage patient records.

📊 Model Performance
Training Accuracy: 96%

Validation Accuracy: 97%

Test Accuracy: 93%
Model used: Support Vector Machine (SVM)

💻 Run the Project Locally
git clone https://github.com/Noor7abouissa/Dr.-Predict.git
cd Dr.-Predict
📂 File Structure
app.py – Flask backend

Dr. Predict - Notebook.ipynb – ML model training and analysis

/static – CSS and images

/templates – HTML templates

hospital_readmission_dataset.csv – Dataset used for training

/models – Trained ML model

requirements.txt – List of Python packages
🔐 Disclaimer
This is a prototype version of the system. No real patient data is used. The system is not yet integrated with real hospital EHRs

📬 Contact

Reference Study:https://smj.org.sa/content/46/3/261

Developed by: Noor Abouissa

Supervised by: Dr. Nasriah

University: Almaarefa University – Health Informatics Department
