from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, classification_report

from src.data_preprocessing import load_data, clean_data, split_data


def run_baseline():
    # Load data
    df = load_data()
    df = clean_data(df)

    # Split data
    X_train, X_test, y_train, y_test = split_data(df)

    # Baseline model (predicts most frequent class)
    baseline = DummyClassifier(strategy="most_frequent")
    baseline.fit(X_train, y_train)

    # Predictions
    y_pred = baseline.predict(X_test)

    # Metrics
    accuracy = accuracy_score(y_test, y_pred)

    print("Baseline Accuracy:", accuracy)
    print("\nBaseline Classification Report:\n")
    print(classification_report(y_test, y_pred, zero_division=0))

    return accuracy