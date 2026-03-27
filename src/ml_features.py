# src/ml_features.py

import pandas as pd
import numpy as np


def create_ml_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # -------------------------------
    # Academic Features
    # -------------------------------
    exam_cols = ["exam1", "exam2", "exam3", "exam4"]

    df["avg_exam_score"] = df[exam_cols].mean(axis=1)
    df["exam_volatility"] = df[exam_cols].std(axis=1)

    # Trend (last - first)
    df["exam_trend"] = df["exam4"] - df["exam1"]

    # -------------------------------
    # Behavioral Risk Flags (0/1)
    # -------------------------------
    df["sleep_risk"] = (df["sleep_hours_per_night"] < 6).astype(int)
    df["study_risk"] = (df["study_hours_per_week"] < 10).astype(int)
    df["attendance_risk"] = (df["attendance"] < 75).astype(int)
    df["delay_risk"] = (df["avg_assignment_delay_days"] > 3).astype(int)
    df["engagement_risk"] = (df["engagement_score"] < 5).astype(int)

    # -------------------------------
    # Combined Behavioral Score
    # -------------------------------
    risk_cols = [
        "sleep_risk",
        "study_risk",
        "attendance_risk",
        "delay_risk",
        "engagement_risk",
    ]

    df["behavioral_risk_score"] = df[risk_cols].sum(axis=1)

    return df