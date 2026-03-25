import joblib
import pandas as pd

from src.config import MODEL_PATH
from src.feature_engineering import process_features


def predict(input_data: dict):
    # Convert input to DataFrame
    df = pd.DataFrame([input_data])

    # Load model
    model = joblib.load(MODEL_PATH)

    # Since we don't have separate train/test here,
    # we pass same df twice just to reuse function
    X_scaled, _, scaler = process_features(df.copy(), df.copy())

    # Predict
    prediction = model.predict(X_scaled)

    return prediction[0]


if __name__ == "__main__":
    sample_student = {
        "attendance": 65,
        "exam1": 60,
        "exam2": 58,
        "exam3": 55,
        "exam4": 50,
        "performance_trend": "declining",
        "study_hours_per_week": 10,
        "sleep_hours_per_night": 5,
        "avg_assignment_delay_days": 4,
        "engagement_score": 3,
        "avg_exam_score": 55,
        "exam_volatility": 4
    }

    result = predict(sample_student)
    print("Predicted Risk:", result)