"""
Feature Extractor — Converts parsed log CSV into ML-ready feature vectors.

Features are computed per source_ip within configurable time windows.

Usage:
    docker compose exec sdp-ubuntu /opt/venv/bin/python3 /app/src/feature_extractor.py \
        --input data/processed/parsed_auth.csv \
        --output data/processed/features.csv \
        --window 60
"""

import pandas as pd
import numpy as np
import argparse
import os
from datetime import datetime


def parse_log_timestamp(ts_str, year=2026):
    """Convert log timestamp (e.g., 'Mar 21 08:30:15') to datetime."""
    try:
        return datetime.strptime(f"{year} {ts_str}", "%Y %b %d %H:%M:%S")
    except ValueError:
        return None


def determine_label(group):
    """
    Determine if a group of events (per IP per time window) is normal or abnormal.

    Heuristic rules:
    - If there are any break-in attempts → abnormal
    - If failed logins > 5 in one window → abnormal
    - If invalid user attempts > 3 → abnormal
    - If fail-to-success ratio > 3 → abnormal
    - Otherwise → normal
    """
    breakin_count = len(group[group["event_type"] == "breakin_attempt"])
    failed_count = len(group[group["event_type"] == "failed_login"])
    invalid_count = len(group[group["event_type"] == "invalid_user_login"])
    success_count = len(group[group["event_type"] == "accepted_login"])

    if breakin_count > 0:
        return "abnormal"
    if failed_count > 5:
        return "abnormal"
    if invalid_count > 3:
        return "abnormal"
    if success_count > 0 and (failed_count / (success_count + 1)) > 3:
        return "abnormal"
    return "normal"


def extract_features(input_path, output_path, window_minutes=60):
    """
    Extract features per source_ip per time window.

    Args:
        input_path: Path to parsed CSV
        output_path: Path to save feature CSV
        window_minutes: Size of the time window in minutes
    """
    # Load parsed data
    df = pd.read_csv(input_path)

    # Parse timestamps
    df["datetime"] = df["timestamp"].apply(parse_log_timestamp)
    df = df.dropna(subset=["datetime"])
    df = df.sort_values("datetime")

    # Create time window column
    df["time_window"] = df["datetime"].dt.floor(f"{window_minutes}min")

    # Group by source_ip and time window
    grouped = df.groupby(["source_ip", "time_window"])

    feature_records = []

    for (ip, window), group in grouped:
        # Event type counts
        failed_count = len(group[group["event_type"] == "failed_login"])
        invalid_count = len(group[group["event_type"] == "invalid_user_login"])
        success_count = len(group[group["event_type"] == "accepted_login"])
        breakin_count = len(group[group["event_type"] == "breakin_attempt"])
        session_count = len(group[group["event_type"] == "session_opened"])
        sudo_count = len(group[group["event_type"] == "sudo_command"])

        record = {
            "source_ip": ip,
            "time_window": window,
            "total_events": len(group),

            # Event type counts
            "failed_login_count": failed_count,
            "invalid_user_count": invalid_count,
            "success_login_count": success_count,
            "breakin_attempts": breakin_count,
            "session_opened_count": session_count,
            "sudo_count": sudo_count,

            # Derived features
            "unique_users_attempted": group["username"].nunique(),
            "fail_to_success_ratio": round(
                failed_count / (success_count + 1), 4
            ),
            "invalid_to_total_ratio": round(
                invalid_count / (len(group) + 1), 4
            ),
            "attack_event_count": failed_count + invalid_count + breakin_count,

            # Time-based features
            "hour_of_day": window.hour,
            "is_night": 1 if window.hour >= 23 or window.hour <= 5 else 0,
            "is_weekend": 1 if window.weekday() >= 5 else 0,

            # Events per minute (frequency)
            "events_per_minute": round(len(group) / window_minutes, 4),

            # Label
            "label": determine_label(group),
        }

        feature_records.append(record)

    # Create feature DataFrame
    features_df = pd.DataFrame(feature_records)

    # Save to CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    features_df.to_csv(output_path, index=False)

    # Print summary
    print(f"\n{'='*60}")
    print(f"Feature Extraction Complete!")
    print(f"{'='*60}")
    print(f"  Input:            {input_path}")
    print(f"  Output:           {output_path}")
    print(f"  Time Window:      {window_minutes} minutes")
    print(f"  Total Samples:    {len(features_df)}")
    print(f"  Normal Samples:   {len(features_df[features_df['label'] == 'normal'])}")
    print(f"  Abnormal Samples: {len(features_df[features_df['label'] == 'abnormal'])}")
    print(f"  Features:         {len(features_df.columns)} columns")
    print(f"{'='*60}")

    # Feature summary
    print(f"\n--- Feature Columns ---")
    for col in features_df.columns:
        if col not in ["source_ip", "time_window", "label"]:
            print(f"  {col:30s}  min={features_df[col].min():<8}  max={features_df[col].max():<8}  mean={features_df[col].mean():.2f}")

    return features_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract ML features from parsed log data")
    parser.add_argument("--input", default="data/processed/parsed_auth.csv", help="Parsed CSV path")
    parser.add_argument("--output", default="data/processed/features.csv", help="Feature CSV path")
    parser.add_argument("--window", type=int, default=60, help="Time window in minutes")
    args = parser.parse_args()

    features_df = extract_features(args.input, args.output, args.window)

    # Print sample
    print(f"\n--- Sample Feature Vectors (first 5) ---")
    print(features_df.head().to_string())
