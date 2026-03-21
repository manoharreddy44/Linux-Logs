"""
Attack Scenario Simulator — Tests models against specific threat patterns.

Generates synthetic attack scenarios and evaluates how each model responds.

Usage:
    docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/attack_simulator.py
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from models.baseline import rule_based_predict

FEATURE_COLS = [
    "total_events", "failed_login_count", "invalid_user_count",
    "success_login_count", "breakin_attempts", "session_opened_count",
    "sudo_count", "unique_users_attempted", "fail_to_success_ratio",
    "invalid_to_total_ratio", "attack_event_count", "hour_of_day",
    "is_night", "is_weekend", "events_per_minute",
]

# ──────────────────────────────────────────────────
# Define attack scenarios as feature vectors
# ──────────────────────────────────────────────────

SCENARIOS = {
    "Brute Force SSH Attack": {
        "total_events": 55, "failed_login_count": 50, "invalid_user_count": 0,
        "success_login_count": 0, "breakin_attempts": 5, "session_opened_count": 0,
        "sudo_count": 0, "unique_users_attempted": 1, "fail_to_success_ratio": 50.0,
        "invalid_to_total_ratio": 0.0, "attack_event_count": 55,
        "hour_of_day": 3, "is_night": 1, "is_weekend": 0, "events_per_minute": 0.917,
        "label": "abnormal",
    },
    "Credential Stuffing": {
        "total_events": 30, "failed_login_count": 5, "invalid_user_count": 25,
        "success_login_count": 0, "breakin_attempts": 0, "session_opened_count": 0,
        "sudo_count": 0, "unique_users_attempted": 25, "fail_to_success_ratio": 5.0,
        "invalid_to_total_ratio": 0.806, "attack_event_count": 30,
        "hour_of_day": 2, "is_night": 1, "is_weekend": 1, "events_per_minute": 0.5,
        "label": "abnormal",
    },
    "Break-in Attempt": {
        "total_events": 10, "failed_login_count": 3, "invalid_user_count": 2,
        "success_login_count": 0, "breakin_attempts": 5, "session_opened_count": 0,
        "sudo_count": 0, "unique_users_attempted": 3, "fail_to_success_ratio": 3.0,
        "invalid_to_total_ratio": 0.182, "attack_event_count": 10,
        "hour_of_day": 23, "is_night": 1, "is_weekend": 0, "events_per_minute": 0.167,
        "label": "abnormal",
    },
    "Normal Work Activity": {
        "total_events": 8, "failed_login_count": 0, "invalid_user_count": 0,
        "success_login_count": 3, "breakin_attempts": 0, "session_opened_count": 3,
        "sudo_count": 2, "unique_users_attempted": 2, "fail_to_success_ratio": 0.0,
        "invalid_to_total_ratio": 0.0, "attack_event_count": 0,
        "hour_of_day": 10, "is_night": 0, "is_weekend": 0, "events_per_minute": 0.133,
        "label": "normal",
    },
    "Night-time Attack": {
        "total_events": 20, "failed_login_count": 15, "invalid_user_count": 3,
        "success_login_count": 0, "breakin_attempts": 2, "session_opened_count": 0,
        "sudo_count": 0, "unique_users_attempted": 5, "fail_to_success_ratio": 15.0,
        "invalid_to_total_ratio": 0.143, "attack_event_count": 20,
        "hour_of_day": 1, "is_night": 1, "is_weekend": 0, "events_per_minute": 0.333,
        "label": "abnormal",
    },
    "Privilege Escalation": {
        "total_events": 12, "failed_login_count": 1, "invalid_user_count": 0,
        "success_login_count": 1, "breakin_attempts": 0, "session_opened_count": 1,
        "sudo_count": 9, "unique_users_attempted": 1, "fail_to_success_ratio": 0.5,
        "invalid_to_total_ratio": 0.0, "attack_event_count": 1,
        "hour_of_day": 14, "is_night": 0, "is_weekend": 0, "events_per_minute": 0.2,
        "label": "normal",  # Borderline — many sudos but from valid user
    },
}


def train_all_models(features_path="data/processed/features.csv"):
    """Train all models on the full dataset."""
    df = pd.read_csv(features_path)
    X = df[FEATURE_COLS].values
    y = (df["label"] == "abnormal").astype(int).values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Decision Tree
    dt = DecisionTreeClassifier(max_depth=5, min_samples_split=5, min_samples_leaf=3, random_state=42)
    dt.fit(X_scaled, y)

    # Isolation Forest
    iso = IsolationForest(n_estimators=100, contamination=y.mean(), random_state=42, n_jobs=-1)
    iso.fit(X_scaled)

    # PCA
    pca = PCA(n_components=0.95, random_state=42)
    pca.fit(X_scaled)
    train_errors = np.mean((X_scaled - pca.inverse_transform(pca.transform(X_scaled))) ** 2, axis=1)
    pca_threshold = np.percentile(train_errors, 95)

    return dt, iso, pca, pca_threshold, scaler, df


def run_scenarios():
    """Test all scenarios against all models."""
    print(f"\n{'='*70}")
    print(f"ATTACK SCENARIO SIMULATION")
    print(f"{'='*70}")

    dt, iso, pca, pca_threshold, scaler, df = train_all_models()

    results = []
    scenario_df = pd.DataFrame([v for v in SCENARIOS.values()])

    for name, scenario in SCENARIOS.items():
        x = np.array([[scenario[f] for f in FEATURE_COLS]])
        x_scaled = scaler.transform(x)
        expected = scenario["label"]

        # Baseline
        scenario_row = pd.DataFrame([scenario])
        baseline_pred = "abnormal" if rule_based_predict(scenario_row)[0] == 1 else "normal"

        # Decision Tree
        dt_pred = "abnormal" if dt.predict(x_scaled)[0] == 1 else "normal"

        # Isolation Forest
        iso_raw = iso.predict(x_scaled)[0]
        iso_pred = "abnormal" if iso_raw == -1 else "normal"

        # PCA
        error = np.mean((x_scaled - pca.inverse_transform(pca.transform(x_scaled))) ** 2)
        pca_pred = "abnormal" if error > pca_threshold else "normal"

        result = {
            "scenario": name,
            "expected": expected,
            "baseline": baseline_pred,
            "isolation_forest": iso_pred,
            "pca_detector": pca_pred,
            "decision_tree": dt_pred,
        }
        results.append(result)

        # Correctness symbols
        b_ok = "✅" if baseline_pred == expected else "❌"
        i_ok = "✅" if iso_pred == expected else "❌"
        p_ok = "✅" if pca_pred == expected else "❌"
        d_ok = "✅" if dt_pred == expected else "❌"

        print(f"\n{'─'*70}")
        print(f"  Scenario: {name}")
        print(f"  Expected: {expected}")
        print(f"{'─'*70}")
        print(f"  Baseline:        {baseline_pred:10s} {b_ok}")
        print(f"  Isolation Forest:{iso_pred:10s} {i_ok}")
        print(f"  PCA Detector:    {pca_pred:10s} {p_ok}")
        print(f"  Decision Tree:   {dt_pred:10s} {d_ok}")

    # Summary table
    results_df = pd.DataFrame(results)
    print(f"\n\n{'='*70}")
    print(f"SCENARIO RESULTS SUMMARY")
    print(f"{'='*70}\n")
    print(results_df.to_string(index=False))

    # Per-model accuracy across scenarios
    print(f"\n--- Model Accuracy Across Scenarios ---")
    for model_col in ["baseline", "isolation_forest", "pca_detector", "decision_tree"]:
        correct = sum(1 for _, r in results_df.iterrows() if r[model_col] == r["expected"])
        total = len(results_df)
        print(f"  {model_col:20s} {correct}/{total} ({correct/total*100:.0f}%)")

    # Save results
    os.makedirs("results/reports", exist_ok=True)
    results_df.to_csv("results/reports/scenario_results.csv", index=False)
    print(f"\n  ✅ Saved: results/reports/scenario_results.csv")

    return results_df


if __name__ == "__main__":
    run_scenarios()
