from src.baseline import run_baseline
from src.train import train_model
from src.evaluate import evaluate_model


def main():
    print("----- BASELINE MODEL -----")
    baseline_acc = run_baseline()

    print("\n----- TRAINED MODEL -----")
    model, X_test, y_test = train_model()
    model_acc, _, _ = evaluate_model(model, X_test, y_test)


if __name__ == "__main__":
    main()