import os
import joblib
import pandas as pd
from django.conf import settings

ARTIFACT_PATH = os.path.join(settings.BASE_DIR, "predictor", "ml", "lung_cancer_artifacts.pkl")

if not os.path.exists(ARTIFACT_PATH):
    raise FileNotFoundError(
        "Model artifact not found. Run 'python train_model.py' first."
    )

artifacts = joblib.load(ARTIFACT_PATH)
model = artifacts["model"]
scaler = artifacts["scaler"]
feature_names = artifacts["feature_names"]
numeric_cols = artifacts["numeric_cols"]
gender_map = artifacts["gender_map"]
target_map = artifacts["target_map"]


def preprocess_input(input_data: dict) -> pd.DataFrame:
    row = input_data.copy()
    row["GENDER"] = gender_map[str(row["GENDER"]).strip().upper()]

    df = pd.DataFrame([row], columns=feature_names)
    df[numeric_cols] = scaler.transform(df[numeric_cols])
    return df


def predict_lung_cancer(input_data: dict) -> dict:
    processed = preprocess_input(input_data)
    pred_num = int(model.predict(processed)[0])

    if hasattr(model, "predict_proba"):
        proba = float(model.predict_proba(processed)[0][pred_num])
    else:
        proba = None

    return {
        "prediction_code": pred_num,
        "prediction_label": target_map[pred_num],
        "confidence": round(proba * 100, 2) if proba is not None else None,
    }
