import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(file)))
MODEL_PATH = os.path.join(BASE_DIR, "lung_cancer_pipeline.pkl")
artrifacts = joblib.load(MODEL_PATH)
model = artrifacts["model"]
scaler = artrifacts["scaler"]
label_encoder = artrifacts["label_encoder"]
feature_names = artrifacts["feature_names"]
columns_to_scale = artrifacts["columns_to_scale"]

def pridict_lung_cancer(input_data):
    df = pd.DataFrame([input_data], columns=feature_names)

    for col in df.columns:
        df[col] = pd.to_numeric(df[col],errors="coerce")
    
    df_scaled = df.copy()
    df_scaled[columns_to_scale]= scaler.transform(df[columns_to_scale])

    prediction = model.predict(df.scaled)[0]
    prediction_label.inversed_transform([prediction])[0]

    return prediction_label