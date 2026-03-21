"""
PCA Anomaly Detector — Unsupervised anomaly detection using reconstruction error.

Uses Principal Component Analysis to project data to lower dimensions and back.
High reconstruction error indicates anomalous behavior.

Usage:
    docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/models/pca_detector.py
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
import joblib
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

FEATURE_COLS = [
    "total_events", "failed_login_count", "invalid_user_count",
    "success_login_count", "breakin_attempts", "session_opened_count",
    "sudo_count", "unique_users_attempted", "fail_to_success_ratio",
    "invalid_to_total_ratio", "attack_event_count", "hour_of_day",
    "is_night", "is_weekend", "events_per_minute",
]


def compute_reconstruction_error(pca, X):
    """
    Compute reconstruction error for each sample.
    Transform to PCA space and back, then measure the difference.
    """
    X_transformed = pca.transform(X)
    X_reconstructed = pca.inverse_transform(X_transformed)
    errors = np.mean((X - X_reconstructed) ** 2, axis=1)
    return errors


def run_pca_detector(features_path="data/processed/features.csv"):
    """Train and evaluate PCA anomaly detector."""

    df = pd.read_csv(features_path)

    # Prepare data
    X = df[FEATURE_COLS].values
    y_true = (df["label"] == "abnormal").astype(int).values

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_true, test_size=0.2, random_state=42, stratify=y_true
    )

    # Fit PCA — keep components explaining 95% variance
    pca = PCA(n_components=0.95, random_state=42)
    pca.fit(X_train)

    n_components = pca.n_components_
    explained_var = pca.explained_variance_ratio_.sum()
    print(f"  PCA components: {n_components} (explains {explained_var:.2%} variance)")

    # Compute reconstruction errors on training data
    train_errors = compute_reconstruction_error(pca, X_train)

    # Set threshold at the 95th percentile of training errors
    threshold = np.percentile(train_errors, 95)
    print(f"  Anomaly threshold: {threshold:.6f} (95th percentile)")

    # Predict on test data
    test_errors = compute_reconstruction_error(pca, X_test)
    y_pred = (test_errors > threshold).astype(int)

    # Results
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=["normal", "abnormal"])
    cm = confusion_matrix(y_test, y_pred)

    print(f"\n{'='*50}")
    print(f"PCA Anomaly Detector Results")
    print(f"{'='*50}")
    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"\nClassification Report:")
    print(report)
    print(f"Confusion Matrix:")
    print(f"  TN={cm[0][0]:4d}  FP={cm[0][1]:4d}")
    print(f"  FN={cm[1][0]:4d}  TP={cm[1][1]:4d}")
    print(f"{'='*50}")

    # Save model
    os.makedirs("results/models", exist_ok=True)
    joblib.dump(pca, "results/models/pca_detector.joblib")
    print(f"\n  Model saved: results/models/pca_detector.joblib")

    return {
        "model": "PCA Anomaly Detector",
        "accuracy": accuracy,
        "y_true": y_test,
        "y_pred": y_pred,
        "threshold": threshold,
    }


if __name__ == "__main__":
    run_pca_detector()
