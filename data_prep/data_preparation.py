"""
Data Preparation for Heart Disease Tableau Project
----------------------------------------------------
Reads the raw extracted dataset (as pulled from heart_disease_db via SQL),
cleans it, engineers features used across the Tableau dashboards, and
writes out analysis-ready extracts that Tableau (or the Flask/Plotly
stand-in dashboards in this deliverable) consume.

Run:  python data_preparation.py
"""
import pandas as pd
import numpy as np
import os

RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "heart_disease.csv")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def load_and_clean(path):
    df = pd.read_csv(path)

    # 1. Missing value handling (defensive - synthetic data has none, but
    #    a real extract from hospital systems will).
    num_cols = ["age", "bmi", "resting_bp", "cholesterol", "max_heart_rate", "oldpeak"]
    cat_cols = ["sex", "region", "smoking_status", "physical_activity",
                "diet_quality", "alcohol_consumption", "family_history",
                "exercise_angina", "chest_pain_type", "thalassemia"]

    for c in num_cols:
        df[c] = df[c].fillna(df[c].median())
    for c in cat_cols:
        df[c] = df[c].fillna(df[c].mode()[0])

    # 2. Remove impossible / outlier rows (clinical bounds)
    df = df[(df.age.between(18, 100)) &
            (df.resting_bp.between(70, 220)) &
            (df.cholesterol.between(100, 450)) &
            (df.bmi.between(12, 60))]

    # 3. Standardize categorical text
    for c in cat_cols:
        df[c] = df[c].astype(str).str.strip().str.title()

    # 4. Feature engineering used by the dashboards
    df["age_group"] = pd.cut(
        df.age, bins=[0, 39, 54, 69, 120],
        labels=["Under 40", "40-54 (Middle-aged)", "55-69", "70+"]
    )

    df["bmi_category"] = pd.cut(
        df.bmi, bins=[0, 18.5, 25, 30, 100],
        labels=["Underweight", "Normal", "Overweight", "Obese"]
    )

    df["bp_category"] = pd.cut(
        df.resting_bp, bins=[0, 120, 129, 139, 300],
        labels=["Normal", "Elevated", "Stage 1 Hypertension", "Stage 2 Hypertension"]
    )

    df["cholesterol_category"] = pd.cut(
        df.cholesterol, bins=[0, 200, 240, 500],
        labels=["Desirable", "Borderline High", "High"]
    )

    # composite lifestyle risk score (0-9) - drives risk_bands lookup in SQL
    df["risk_score"] = (
        (df.age > 55).astype(int) +
        (df.sex == "Male").astype(int) +
        df.smoking_status.map({"Current": 2, "Former": 1, "Never": 0}) +
        (df.physical_activity == "Sedentary").astype(int) +
        (df.bmi > 30).astype(int) +
        (df.cholesterol > 240).astype(int) +
        (df.resting_bp > 140).astype(int) +
        (df.family_history == "Yes").astype(int) +
        (df.exercise_angina == "Yes").astype(int)
    )
    df["risk_band"] = pd.cut(df.risk_score, bins=[-1, 3, 7, 15],
                              labels=["Low", "Moderate", "High"])

    return df


def export_extracts(df):
    # Full cleaned extract (Tableau primary data source)
    df.to_csv(os.path.join(OUT_DIR, "heart_disease_clean.csv"), index=False)

    # Pre-aggregated extracts (mirrors the SQL views, useful for fast
    # dashboard rendering / smaller Tableau extracts)
    df.groupby(["age_group", "sex", "smoking_status"], observed=True).agg(
        total_patients=("patient_id", "count"),
        disease_cases=("heart_disease", "sum"),
        avg_bmi=("bmi", "mean"),
        avg_cholesterol=("cholesterol", "mean"),
    ).reset_index().to_csv(os.path.join(OUT_DIR, "agg_age_group_risk.csv"), index=False)

    df.groupby(["region", "physical_activity", "diet_quality"], observed=True).agg(
        total_patients=("patient_id", "count"),
        disease_cases=("heart_disease", "sum"),
        avg_bp=("resting_bp", "mean"),
        avg_cholesterol=("cholesterol", "mean"),
    ).reset_index().to_csv(os.path.join(OUT_DIR, "agg_region_lifestyle.csv"), index=False)

    df.to_csv(os.path.join(OUT_DIR, "patient_benchmark.csv"), index=False)

    print("Exported: heart_disease_clean.csv, agg_age_group_risk.csv, "
          "agg_region_lifestyle.csv, patient_benchmark.csv")


if __name__ == "__main__":
    df = load_and_clean(RAW_PATH)
    print(f"Cleaned dataset shape: {df.shape}")
    print(df.isna().sum().sum(), "missing values remaining")
    export_extracts(df)
