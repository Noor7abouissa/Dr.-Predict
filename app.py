from flask import Flask, render_template, request, redirect, url_for, session, json, jsonify, make_response, flash 
from datetime import datetime, date
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# Load SVM model and scaler
svm_model = joblib.load('models/svm_model.pkl')
scaler = joblib.load('models/scaler.pkl')
le = joblib.load('models/label_encoder.pkl')

# Database connection
conn = mysql.connector.connect(host='localhost', user='root', password='', database='progrex_rex')
cursor = conn.cursor()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

    # Fetching user name
    cursor.execute("SELECT name FROM progrex_rex WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    user_name = user[0] if user else "Doctor"

    # Fetching predictions
    cursor.execute("SELECT * FROM predictions")
    predictions = cursor.fetchall()

    # Calculating dashboard statistics
    today = date.today()
    total_patients_today = 0
    high_risk_patients = 0
    risk_scores = []

    # Risk mapping
    risk_mapping = {'High': 90, 'Medium': 60, 'Low': 30, 'No': 0}

    # Process predictions
    for prediction in predictions:
        # Columns: id, patient_name, age, gender, chronic_disease, smoker, num_medications, prev_admissions, bmi, days_since_last, predicted_risk, predicted_at
        prediction_date = prediction[11]
        if isinstance(prediction_date, datetime):
            prediction_date = prediction_date.date()

        if prediction_date == today:
            total_patients_today += 1
            predicted_risk = prediction[10]
            if predicted_risk == 'High':
                high_risk_patients += 1
            risk_score = risk_mapping.get(predicted_risk, 0)
            risk_scores.append(risk_score)

    # Calculate average risk score
    average_risk_score = round(sum(risk_scores) / len(risk_scores), 2) if risk_scores else 0

    
    patients = []
    for prediction in predictions:
        prediction_date = prediction[11]
        if isinstance(prediction_date, datetime):
            prediction_date = prediction_date.date()
        if prediction_date == today:
            predicted_risk = prediction[10]
            risk_score = risk_mapping.get(predicted_risk, 0)
            patients.append({
                'id': prediction[0],
                'name': prediction[1],
                'age': prediction[2],
                'condition': prediction[4],
                'risk_score': f"{risk_score}%"
            })

    return render_template('dashboard.html',
                          user_name=user_name,
                          total_patients_today=total_patients_today,
                          high_risk_patients=high_risk_patients,
                          average_risk_score=average_risk_score,
                          patients=patients)

@app.route('/patient_details', methods=['GET'])
def patient_details():
    search_query = request.args.get('search', '').strip()

    if search_query:
        cursor.execute("SELECT * FROM predictions WHERE patient_name LIKE %s", ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT * FROM predictions")
    
    patients = cursor.fetchall()

    # Preparing list of patients
    patient_list = []
    for patient in patients:
        patient_data = {
            'id': patient[0],
            'name': patient[1],
            'age': patient[2],
            'gender': patient[3],
            'chronic_disease': patient[4],
            'smoker': patient[5],
            'num_medications': patient[6],
            'prev_admissions': patient[7],
            'bmi': patient[8],
            'days_since_last': patient[9],
            'predicted_risk': patient[10]
        }
        patient_list.append(patient_data)

    return render_template('patient_details.html', patients=patient_list)

@app.route('/my_patients')
def my_patients():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    return render_template('my_patients.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Login validation
@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    cursor.execute("SELECT * FROM progrex_rex WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user:
        # Hashing passwords
        if check_password_hash(user[3], password):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect password. Please try again.', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Email not found. Please register.', 'warning')
        return redirect(url_for('register'))
    
    # the captcha code
    captcha_response = request.form.get('g-recaptcha-response')
    verify_url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {
    'secret': '6Le9CxwrAAAAACEU0vogo8SjH8osg5dTf75mk_X1',
    'response': captcha_response
    }
    r = requests.post(verify_url, data=payload)
    result = r.json()

    if not result['success']:
        flash("Captcha verification failed. Please try again.", "danger")
        return redirect(url_for('login'))
# captcha code ends here

# Register user
@app.route('/register_user', methods=['POST'])
def register_user():
    # Getting form data
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')


    # Checking if email already exists
    cursor.execute("SELECT * FROM `progrex_rex` WHERE `email` = %s", (email,))
    user = cursor.fetchone()

    if user:
        flash("Email already exists. Please use a different email.", "warning")
        return redirect(url_for('register'))

    # Hashing the password
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Inserting into database
    try:
        cursor.execute("""
            INSERT INTO progrex_rex (name, email, password)
            VALUES (%s, %s, %s)
        """, (name, email, hashed_password))
        conn.commit()
        flash('Registration successful! You can now login.', 'success')
        return redirect(url_for('login'))
    except Exception as e:
        flash('An error occurred during registration. Please try again.', 'danger')
        print(f"Error: {e}")
        return redirect(url_for('register'))

    # the captcha code for registration
    captcha_response = request.form.get('g-recaptcha-response')
    verify_url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {
    'secret': '6Le9CxwrAAAAACEU0vogo8SjH8osg5dTf75mk_X1',
    'response': captcha_response
    }
    r = requests.post(verify_url, data=payload)
    result = r.json()

    if not result['success']:
        flash("Captcha verification failed. Please try again.", "danger")
        return redirect(url_for('register'))
# captcha code ends here




# The Forgot Password Route
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        cursor.execute("SELECT * FROM progrex_rex WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            return render_template('reset_password.html', email=email)
        else:
            flash("Email not found. Please register.", "warning")
            return redirect(url_for('register'))
    
    return render_template('forgot_password.html')

# Reset Password Code
@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if new_password != confirm_password:
        flash("Passwords do not match. Try again.", "danger")
        return render_template('reset_password.html', email=email)

    hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
    try:
        cursor.execute("UPDATE progrex_rex SET password = %s WHERE email = %s", (hashed_password, email))
        conn.commit()
        flash("Password reset successfully! You can now login.", "success")
        return redirect(url_for('login'))
    except Exception as e:
        print("Error updating password:", e)
        flash("An error occurred. Please try again.", "danger")
        return render_template('reset_password.html', email=email)

le = LabelEncoder()

# Code for label encoding code

le = LabelEncoder()
le.classes_ = ['No risk', 'Low risk', 'Medium risk', 'High risk']

le = LabelEncoder()
le.fit(['No', 'Low', 'Medium', 'High'])

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    prediction_result = None

    if request.method == 'POST':
        try:
            patient_name = request.form['patient_name']
            age = int(request.form['age'])
            gender = 1 if request.form['gender'] == 'Female' else 0
            chronic_disease = request.form['chronic_disease']
            smoker = 1 if request.form['smoker'] == 'Yes' else 0
            num_medications = int(request.form['num_medications'])
            prev_admissions = int(request.form['prev_admissions'])
            bmi = float(request.form['bmi'])
            days_since_last = int(request.form['days_since_last'])

            disease_list = ['Diabetes', 'Heart Disease', 'Hypertension', 'No Chronic Disease']
            disease_encoding = [1 if chronic_disease == dis else 0 for dis in disease_list]

            # Converting numerical features into list
            numerical_features = [age, num_medications, prev_admissions, bmi, days_since_last]

            # Converting numerical features to a DataFrame
            numerical_features_df = pd.DataFrame(
                [numerical_features],
                columns=['Age', 'Number_of_Medications', 'Previous_Admissions', 'BMI', 'Days_Since_Last_Admission']
            )

            # Scaling the numerical features
            scaled_numerical_features = scaler.transform(numerical_features_df)[0]

            # Full features as a DataFrame
            final_features_df = pd.DataFrame(
                [[scaled_numerical_features[0], gender, smoker, scaled_numerical_features[1], scaled_numerical_features[2], scaled_numerical_features[3], scaled_numerical_features[4]] + disease_encoding],
                columns=['Age', 'Gender', 'Smoker', 'Number_of_Medications', 'Previous_Admissions', 'BMI', 'Days_Since_Last_Admission', 'Disease_Diabetes', 'Disease_Heart Disease', 'Disease_Hypertension', 'Disease_No Chronic Disease']
            )

            # Making prediction
            prediction = svm_model.predict(final_features_df)
            prediction_label = le.inverse_transform(prediction)[0]
            prediction_result = prediction_label

            # Saving to MySQL database
             
            cursor.execute("""
                INSERT INTO predictions 
                (patient_name, age, gender, chronic_disease, smoker, num_medications, prev_admissions, bmi, days_since_last, predicted_risk)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                patient_name, age, 'Female' if gender == 1 else 'Male', chronic_disease,
                'Yes' if smoker == 1 else 'No', num_medications, prev_admissions, bmi, days_since_last, prediction_label
            ))
            conn.commit()
        

        except Exception as e:
            print("Error in prediction route:", e)
            flash("Something went wrong while predicting. Please try again.", "error")

    return render_template('predict.html', prediction_result=prediction_result)
if __name__ == "__main__":
    app.run(debug=True)