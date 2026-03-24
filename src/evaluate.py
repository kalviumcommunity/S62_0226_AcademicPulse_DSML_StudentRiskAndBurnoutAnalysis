from sklearn.metrics import accuracy_score

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)

    acc = accuracy_score(y_test, predictions)

    print("Accuracy:", acc)

    return acc

    