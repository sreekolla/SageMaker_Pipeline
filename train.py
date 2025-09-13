import argparse
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def generate_synthetic_data(num_samples=1000, num_features=5, n_classes=2):
    """Generate synthetic dataset if input data is missing."""
    X = np.random.rand(num_samples, num_features)
    y = np.random.randint(0, n_classes, size=num_samples)
    df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(num_features)])
    df["target"] = y
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-data", type=str, default="/opt/ml/input/data")
    parser.add_argument("--model-dir", type=str, default="/opt/ml/model")
    args = parser.parse_args()

    # Check if S3 training data exists
    input_file = os.path.join(args.input_data, "train.csv")
    if os.path.exists(input_file):
        print(f"Loading training data from {input_file}")
        data = pd.read_csv(input_file)
    else:
        print("No input data found. Generating synthetic data...")
        data = generate_synthetic_data()

    # Prepare features and target
    X = data.drop("target", axis=1)
    y = data["target"]

    # Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Evaluate
    preds = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, preds))

    # Save model
    os.makedirs(args.model_dir, exist_ok=True)
    joblib.dump(model, os.path.join(args.model_dir, "model.joblib"))
    print(f"Model saved to {args.model_dir}")
