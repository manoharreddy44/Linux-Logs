"""
Isolation Forest — Unsupervised anomaly detection model.

Detects anomalies by isolating outliers using random partitioning.
Points that are isolated quickly (short path length) are anomalies.

Usage:
    docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/models/isolation_forest.py
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
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


def run_isolation_forest(features_path="data/processed/features.csv"):
    """Train and evaluate Isolation Forest model."""

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

    # Calculate contamination from actual data
    contamination = y_true.mean()
    print(f"  Contamination (actual abnormal ratio): {contamination:.4f}")

    # Train Isolation Forest
    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train)

    # Predict (-1 = anomaly, 1 = normal in sklearn convention)
    y_pred_raw = model.predict(X_test)
    y_pred = (y_pred_raw == -1).astype(int)  # Convert: -1→1 (abnormal), 1→0 (normal)

    # Results
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=["normal", "abnormal"])
    cm = confusion_matrix(y_test, y_pred)

    print(f"\n{'='*50}")
    print(f"Isolation Forest Results")
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
    joblib.dump(model, "results/models/isolation_forest.joblib")
    joblib.dump(scaler, "results/models/scaler.joblib")
    print(f"\n  Model saved: results/models/isolation_forest.joblib")

    return {
        "model": "Isolation Forest",
        "accuracy": accuracy,
        "y_true": y_test,
        "y_pred": y_pred,
    }


if __name__ == "__main__":
    run_isolation_forest()
