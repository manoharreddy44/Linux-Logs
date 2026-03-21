"""
Rule-Based Baseline Detector — Simple heuristic anomaly detection.

Uses hand-crafted rules to classify log behavior as normal or abnormal.
This serves as a baseline to compare ML models against.

Usage:
    docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/models/baseline.py
"""

import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def rule_based_predict(df):
    """
    Apply heuristic rules to classify each sample.

    Rules:
    - breakin_attempts > 0 → abnormal
    - failed_login_count > 3 → abnormal
    - invalid_user_count > 2 → abnormal
    - fail_to_success_ratio > 2.0 → abnormal
    - attack_event_count > 3 → abnormal
    - Otherwise → normal
    """
    predictions = []

    for _, row in df.iterrows():
        if row["breakin_attempts"] > 0:
            predictions.append(1)  # abnormal
        elif row["failed_login_count"] > 3:
            predictions.append(1)
        elif row["invalid_user_count"] > 2:
            predictions.append(1)
        elif row["fail_to_success_ratio"] > 2.0:
            predictions.append(1)
        elif row["attack_event_count"] > 3:
            predictions.append(1)
        else:
            predictions.append(0)  # normal

    return np.array(predictions)


def run_baseline(features_path="data/processed/features.csv"):
    """Run the rule-based baseline and print results."""

    df = pd.read_csv(features_path)

    # Encode labels
    y_true = (df["label"] == "abnormal").astype(int).values

    # Predict
    y_pred = rule_based_predict(df)

    # Results
    accuracy = accuracy_score(y_true, y_pred)
    report = classification_report(y_true, y_pred, target_names=["normal", "abnormal"])
    cm = confusion_matrix(y_true, y_pred)

    print(f"\n{'='*50}")
    print(f"Rule-Based Baseline Results")
    print(f"{'='*50}")
    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"\nClassification Report:")
    print(report)
    print(f"Confusion Matrix:")
    print(f"  TN={cm[0][0]:4d}  FP={cm[0][1]:4d}")
    print(f"  FN={cm[1][0]:4d}  TP={cm[1][1]:4d}")
    print(f"{'='*50}")

    return {
        "model": "Rule-Based Baseline",
        "accuracy": accuracy,
        "y_true": y_true,
        "y_pred": y_pred,
    }


if __name__ == "__main__":
    run_baseline()
