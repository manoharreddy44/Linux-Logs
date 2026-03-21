"""
Decision Tree Classifier — Supervised anomaly detection model.

Learns decision rules from labeled training data to classify
log behavior as normal or abnormal.

Usage:
    docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/models/decision_tree.py
"""

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
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


def run_decision_tree(features_path="data/processed/features.csv"):
    """Train and evaluate Decision Tree classifier."""

    df = pd.read_csv(features_path)

    # Prepare data
    X = df[FEATURE_COLS].values
    y_true = (df["label"] == "abnormal").astype(int).values

    # Scale features (not strictly needed for DT, but keeps consistency)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_true, test_size=0.2, random_state=42, stratify=y_true
    )

    # Train Decision Tree
    model = DecisionTreeClassifier(
        max_depth=5,
        min_samples_split=5,
        min_samples_leaf=3,
        random_state=42,
    )
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Results
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=["normal", "abnormal"])
    cm = confusion_matrix(y_test, y_pred)

    print(f"\n{'='*50}")
    print(f"Decision Tree Classifier Results")
    print(f"{'='*50}")
    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"\nClassification Report:")
    print(report)
    print(f"Confusion Matrix:")
    print(f"  TN={cm[0][0]:4d}  FP={cm[0][1]:4d}")
    print(f"  FN={cm[1][0]:4d}  TP={cm[1][1]:4d}")

    # Feature importance
    importances = model.feature_importances_
    feature_importance = sorted(
        zip(FEATURE_COLS, importances), key=lambda x: x[1], reverse=True
    )
    print(f"\nTop Feature Importances:")
    for feat, imp in feature_importance[:7]:
        bar = "█" * int(imp * 50)
        print(f"  {feat:30s} {imp:.4f} {bar}")

    # Print tree rules
    print(f"\nDecision Tree Rules:")
    tree_rules = export_text(model, feature_names=FEATURE_COLS, max_depth=3)
    print(tree_rules)
    print(f"{'='*50}")

    # Save tree visualization
    os.makedirs("results/figures", exist_ok=True)
    fig, ax = plt.subplots(figsize=(20, 10))
    plot_tree(
        model, feature_names=FEATURE_COLS,
        class_names=["normal", "abnormal"],
        filled=True, rounded=True, ax=ax,
        fontsize=8, proportion=True,
    )
    plt.title("Decision Tree for Anomaly Detection", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("results/figures/decision_tree.png", dpi=150, bbox_inches="tight")
    print(f"\n  Tree visualization saved: results/figures/decision_tree.png")
    plt.close()

    # Save model
    os.makedirs("results/models", exist_ok=True)
    joblib.dump(model, "results/models/decision_tree.joblib")
    print(f"  Model saved: results/models/decision_tree.joblib")

    return {
        "model": "Decision Tree",
        "accuracy": accuracy,
        "y_true": y_test,
        "y_pred": y_pred,
    }


if __name__ == "__main__":
    run_decision_tree()
