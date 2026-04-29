import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

DATA_FILE = "survey_lung_cancer.csv"
ARTIFACT_DIR = os.path.join("predictor", "ml")
ARTIFACT_PATH = os.path.join(ARTIFACT_DIR, "lung_cancer_artifacts.pkl")


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip()

    if "GENDER" in df.columns:
        df["GENDER"] = (
            df["GENDER"]
            .astype(str)
            .str.strip()
            .str.upper()
            .map({"M": 1, "F": 0})
        )

    if "LUNG_CANCER" in df.columns:
        df["LUNG_CANCER"] = (
            df["LUNG_CANCER"]
            .astype(str)
            .str.strip()
            .str.upper()
            .map({"YES": 1, "NO": 0})
        )

    return df


def main():
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)
    df = clean_dataframe(df)
    df = df.dropna().drop_duplicates()

    X = df.drop(columns=["LUNG_CANCER"])
    y = df["LUNG_CANCER"]

    numeric_cols = [col for col in X.columns if col != "GENDER"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()

    X_train_scaled[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
    X_test_scaled[numeric_cols] = scaler.transform(X_test[numeric_cols])

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42
    )
    model.fit(X_train_scaled, y_train)

    preds = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, preds)

    print(f"Accuracy: {acc:.4f}")
    print(classification_report(y_test, preds, target_names=["NO", "YES"]))

    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    artifacts = {
        "model": model,
        "scaler": scaler,
        "feature_names": list(X.columns),
        "numeric_cols": numeric_cols,
        "gender_map": {"M": 1, "F": 0},
        "target_map": {1: "YES", 0: "NO"},
    }
    joblib.dump(artifacts, ARTIFACT_PATH)
    print(f"Saved artifacts to: {ARTIFACT_PATH}")


if __name__ == "__main__":
    main()
