from sklearn.preprocessing import StandardScaler, LabelEncoder

def process_features(X_train, X_test):
    scaler = StandardScaler()
    encoder = LabelEncoder()

    # Handle categorical column
    if "performance_trend" in X_train.columns:
        X_train["performance_trend"] = encoder.fit_transform(X_train["performance_trend"])
        X_test["performance_trend"] = encoder.transform(X_test["performance_trend"])

    # Scale features
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, scaler