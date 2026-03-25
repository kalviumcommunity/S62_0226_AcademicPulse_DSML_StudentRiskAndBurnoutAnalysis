from sklearn.ensemble import RandomForestClassifier
import joblib

from src.data_preprocessing import load_data, clean_data, split_data
from src.feature_engineering import process_features
from src.config import MODEL_PATH, PIPELINE_PATH, RANDOM_STATE


def train_model():
    # Load and clean data
    df = load_data()
    df = clean_data(df)

    # Split data
    X_train, X_test, y_train, y_test = split_data(df)

    # Process features (encoding + scaling)
    X_train_scaled, X_test_scaled, scaler = process_features(X_train, X_test)

    # Train model
    model = RandomForestClassifier(random_state=RANDOM_STATE)
    model.fit(X_train_scaled, y_train)

    # Save model and preprocessing pipeline
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, PIPELINE_PATH)

    return model, X_test_scaled, y_test