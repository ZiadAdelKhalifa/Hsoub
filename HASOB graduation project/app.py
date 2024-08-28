from flask import Flask, request, jsonify, render_template
import numpy as np
from joblib import load
from keras.models import load_model

app = Flask(__name__)

# Load the required models and encoders
labelencoder_loaded = load("heart_disease_encoder.pkl")
ct_loaded = load("heart_disease_OneHotEncoder.pkl")
sc_loaded = load("heart_disease_standard_scaler.pkl")
loaded_model = load_model("heart_disease_model.keras")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from the form
    age = int(request.form['age'])
    sex = request.form['sex']
    cp = request.form['cp']
    trestbps = float(request.form['trestbps'])
    chol = float(request.form['chol'])
    fbs = request.form['fbs'] == 'True'
    restecg = request.form['restecg']
    thalach = float(request.form['thalach'])
    exang = request.form['exang'] == 'True'
    oldpeak = float(request.form['oldpeak'])
    slope = request.form['slope']
    ca = float(request.form['ca'])
    thal = request.form['thal']

    # Create a new patient array
    new_patient = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]], dtype=object)

    # Refit the LabelEncoder with the new data for the appropriate columns
    new_patient[:, 2] = labelencoder_loaded.fit_transform(new_patient[:, 2])  # Encode 'cp'
    new_patient[:, 6] = labelencoder_loaded.fit_transform(new_patient[:, 6])  # Encode 'restecg'
    new_patient[:, 10] = labelencoder_loaded.fit_transform(new_patient[:, 10])  # Encode 'slope'

    # Convert types for bool and object columns
    new_patient[0, 1] = str(new_patient[0, 1])  # Convert 'sex' to string
    new_patient[0, 5] = bool(new_patient[0, 5])  # Convert 'fbs' to boolean
    new_patient[0, 8] = bool(new_patient[0, 8])  # Convert 'exang' to boolean
    new_patient[0, 12] = str(new_patient[0, 12])  # Convert 'thal' to string

    # Apply the OneHotEncoder and StandardScaler
    new_patient = ct_loaded.transform(new_patient)
    new_patient_scaled = sc_loaded.transform(new_patient)

    # Make the prediction
    new_prediction_proba = loaded_model.predict(new_patient_scaled)
    predicted_category = np.argmax(new_prediction_proba, axis=1)[0]  # Extracting the value

    # Map predicted category to its label
    category_labels = {
        0: "No heart disease",
        1: "Stage 1 heart disease",
        2: "Stage 2 heart disease",
        3: "Stage 3 heart disease",
        4: "Stage 4 heart disease"
    }
    predicted_label = category_labels.get(predicted_category, "Unknown stage")

    # Return the result
    return jsonify({
        'prediction_probability': new_prediction_proba.tolist(),
        'predicted_category': int(predicted_category),
        'predicted_label': predicted_label
    })

if __name__ == "__main__":
    app.run(debug=True)
