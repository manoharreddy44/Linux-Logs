"""
Data Explorer — Loads parsed CSV and provides basic statistics.

Usage:
    docker compose exec sdp-ubuntu /opt/venv/bin/python3 /app/src/data_explorer.py
"""

import pandas as pd
import sys


def explore_data(csv_path="data/processed/parsed_auth.csv"):
    """Load and explore the parsed log data."""

    df = pd.read_csv(csv_path)

    print("=" * 60)
    print("DATA OVERVIEW")
    print("=" * 60)

    # Basic info
    print(f"\nTotal records: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    # Data types
    print(f"\n--- Data Types ---")
    print(df.dtypes.to_string())

    # Event type distribution
    print(f"\n--- Event Type Distribution ---")
    event_counts = df["event_type"].value_counts()
    for event, count in event_counts.items():
        pct = count / len(df) * 100
        print(f"  {event:25s} {count:5d}  ({pct:.1f}%)")

    # Label distribution (normal vs abnormal)
    print(f"\n--- Label Distribution ---")
    label_counts = df["label"].value_counts()
    for label, count in label_counts.items():
        pct = count / len(df) * 100
        print(f"  {label:25s} {count:5d}  ({pct:.1f}%)")

    # Unique source IPs
    print(f"\n--- Source IP Distribution ---")
    ip_counts = df["source_ip"].value_counts()
    for ip, count in ip_counts.items():
        pct = count / len(df) * 100
        print(f"  {ip:25s} {count:5d}  ({pct:.1f}%)")

    # Unique usernames
    print(f"\n--- Username Distribution ---")
    user_counts = df["username"].value_counts()
    for user, count in user_counts.items():
        pct = count / len(df) * 100
        print(f"  {user:25s} {count:5d}  ({pct:.1f}%)")

    # Sample records
    print(f"\n--- First 5 Records ---")
    print(df[["timestamp", "event_type", "username", "source_ip", "label"]].head().to_string(index=False))

    print(f"\n{'='*60}")

    return df


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/processed/parsed_auth.csv"
    explore_data(csv_path)
