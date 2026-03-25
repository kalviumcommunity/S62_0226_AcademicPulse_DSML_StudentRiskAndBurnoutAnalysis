from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report


def evaluate_model(model, X_test, y_test):
    # Predictions
    y_pred = model.predict(X_test)

    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)

    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)

    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred, zero_division=0))

    return accuracy, precision, recall