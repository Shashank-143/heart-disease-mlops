import streamlit as st
import pandas as pd
import joblib
import time
from prometheus_client import start_http_server, Counter, Histogram

# Load trained model
model = joblib.load("model.pkl")

# Prometheus metrics
@st.cache_resource
def start_monitoring():
    start_http_server(8000)

    return {
        "requests": Counter(
            "prediction_requests_total",
            "Total prediction requests"
        ),
        "predictions": Counter(
            "predictions_total",
            "Total predictions made"
        ),
        "errors": Counter(
            "prediction_errors_total",
            "Total prediction errors"
        ),
        "latency": Histogram(
            "prediction_latency_seconds",
            "Prediction processing time"
)
    }

metrics = start_monitoring()

# Streamlit interface
st.title("Heart Disease Prediction")
st.write("Enter the details below to generate a model prediction.")

age = st.number_input("Age", 1, 120, 45)
sex = st.selectbox("Sex", ["M", "F"])
chest_pain = st.selectbox("Chest Pain Type",["TA", "ATA", "NAP", "ASY"])
resting_bp = st.number_input("Resting Blood Pressure", 0, 250, 120)
cholesterol = st.number_input("Cholesterol", 0, 700, 200)
fasting_bs = st.selectbox("Fasting Blood Sugar", [0, 1])
resting_ecg = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])
max_hr = st.number_input("Maximum Heart Rate", 50, 250, 150)
exercise_angina = st.selectbox("Exercise Angina", ["N", "Y"])
oldpeak = st.number_input("Oldpeak", min_value=0.0, max_value=10.0, value=1.0)
st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

if st.button("Predict"):

    metrics["requests"].inc()
    start_time = time.time()

    try:
        input_data = pd.DataFrame([{
            "Age": age,
            "Sex": sex,
            "ChestPainType": chest_pain,
            "RestingBP": resting_bp,
            "Cholesterol": cholesterol,
            "FastingBS": fasting_bs,
            "RestingECG": resting_ecg,
            "MaxHR": max_hr,
            "ExerciseAngina": exercise_angina,
            "Oldpeak": oldpeak,
            "ST_Slope": st_slope
        }])

        prediction = model.predict(input_data)[0]
        metrics["predictions"].inc()

        if prediction == 1:
            st.warning("The model predicts a positive heart disease class.")
        else:
            st.success("The model predicts a negative heart disease class.")

    except Exception as error:
        metrics["errors"].inc()
        st.error(f"Prediction failed: {error}")

    finally:
        metrics["latency"].observe(time.time() - start_time)