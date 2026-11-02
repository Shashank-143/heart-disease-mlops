import joblib
import pandas as pd

def test_model_prediction():

    model = joblib.load("model.pkl")

    sample = pd.DataFrame([{
        "Age": 45,
        "Sex": "M",
        "ChestPainType": "ATA",
        "RestingBP": 120,
        "Cholesterol": 200,
        "FastingBS": 0,
        "RestingECG": "Normal",
        "MaxHR": 150,
        "ExerciseAngina": "N",
        "Oldpeak": 1.0,
        "ST_Slope": "Up"
    }])

    prediction = model.predict(sample)

    assert len(prediction) == 2
    assert prediction[0] in [0, 1]