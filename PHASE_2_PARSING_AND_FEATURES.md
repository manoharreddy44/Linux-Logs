# 🔧 Phase 2 — Log Parsing & Feature Engineering

> **Goal:** Parse raw Linux log files into structured data, extract meaningful features, and build a labeled dataset ready for machine learning.
>
> **Duration:** Week 3–4
>
> **Prerequisites:** [Phase 1](./PHASE_1_SETUP_AND_DATA_COLLECTION.md) completed — Ubuntu 24.04 LTS environment with Python 3.14+, Pandas 3.0.1, NumPy 2.4.3, Scikit-learn 1.8.1, Matplotlib 3.10.8, and Seaborn 0.13.2 are set up and raw log files are collected.

---

## Step 1: Understand Log Structure Before Parsing

### What to do
Analyze the raw log file format so you know exactly what patterns to extract.

### How to do it

Open and study your raw auth.log:

```bash
head -30 data/raw/sample_auth.log
```

### Common auth.log patterns

| Pattern | Meaning | Label |
|---------|---------|-------|
| `Accepted password for <user> from <ip>` | Successful login | ✅ Normal |
| `Failed password for <user> from <ip>` | Failed login attempt | ⚠️ Suspicious |
| `Failed password for invalid user <user> from <ip>` | Login attempt with non-existent user | 🔴 Abnormal |
| `POSSIBLE BREAK-IN ATTEMPT from <ip>` | Detected break-in attempt | 🔴 Abnormal |
| `pam_unix(sshd:session): session opened for user <user>` | Session opened | ✅ Normal |
| `sudo: <user> : ... COMMAND=<cmd>` | Sudo command executed | ✅ Normal (usually) |

### Key fields to extract

| Field | Example | Purpose |
|-------|---------|---------|
| `timestamp` | `Mar 21 08:30:15` | Time-series analysis |
| `hostname` | `server` | Filter by host |
| `service` | `sshd`, `sudo` | Identify log source |
| `pid` | `12345` | Track process |
| `event_type` | `accepted`, `failed`, `invalid_user` | Classification label |
| `username` | `rahul`, `admin` | User behavior analysis |
| `source_ip` | `192.168.1.50` | Track source of connection |
| `port` | `54321` | Connection metadata |

---

## Step 2: Build the Log Parser

### What to do
Write a Python script that reads raw log lines and extracts structured fields using regex patterns.

### How to do it

Create `src/log_parser.py`:

```python
"""
Log Parser — Parses raw auth.log entries into structured records.

Usage:
    python src/log_parser.py --input data/raw/sample_auth.log --output data/processed/parsed_auth.csv
"""

import re
import csv
import argparse
from datetime import datetime

# ──────────────────────────────────────────────
# Regex patterns for different log event types
# ──────────────────────────────────────────────

PATTERNS = {
    "accepted_password": {
        "regex": re.compile(
            r"(?P<timestamp>\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s+"
            r"(?P<hostname>\S+)\s+sshd\[(?P<pid>\d+)\]:\s+"
            r"Accepted password for (?P<username>\S+)\s+"
            r"from (?P<source_ip>\S+)\s+port (?P<port>\d+)"
        ),
        "event_type": "accepted_login",
        "label": "normal",
    },
    "failed_password": {
        "regex": re.compile(
            r"(?P<timestamp>\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s+"
            r"(?P<hostname>\S+)\s+sshd\[(?P<pid>\d+)\]:\s+"
            r"Failed password for (?P<username>\S+)\s+"
            r"from (?P<source_ip>\S+)\s+port (?P<port>\d+)"
        ),
        "event_type": "failed_login",
        "label": "suspicious",
    },
    "invalid_user": {
        "regex": re.compile(
            r"(?P<timestamp>\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s+"
            r"(?P<hostname>\S+)\s+sshd\[(?P<pid>\d+)\]:\s+"
            r"Failed password for invalid user (?P<username>\S+)\s+"
            r"from (?P<source_ip>\S+)\s+port (?P<port>\d+)"
        ),
        "event_type": "invalid_user_login",
        "label": "abnormal",
    },
    "breakin_attempt": {
        "regex": re.compile(
            r"(?P<timestamp>\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s+"
            r"(?P<hostname>\S+)\s+sshd\[(?P<pid>\d+)\]:\s+"
            r"POSSIBLE BREAK-IN ATTEMPT from (?P<source_ip>\S+)"
        ),
        "event_type": "breakin_attempt",
        "label": "abnormal",
    },
    "session_opened": {
        "regex": re.compile(
            r"(?P<timestamp>\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s+"
            r"(?P<hostname>\S+)\s+sshd\[(?P<pid>\d+)\]:\s+"
            r"pam_unix\(sshd:session\): session opened for user (?P<username>\S+)"
        ),
        "event_type": "session_opened",
        "label": "normal",
    },
    "sudo_command": {
        "regex": re.compile(
            r"(?P<timestamp>\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s+"
            r"(?P<hostname>\S+)\s+sudo:\s+(?P<username>\S+)\s+:.*"
            r"COMMAND=(?P<command>.+)"
        ),
        "event_type": "sudo_command",
        "label": "normal",
    },
}


def parse_log_line(line):
    """
    Try to match a log line against known patterns.
    Returns a dict with extracted fields, or None if no pattern matches.
    """
    for pattern_name, config in PATTERNS.items():
        match = config["regex"].search(line)
        if match:
            record = match.groupdict()
            record["event_type"] = config["event_type"]
            record["label"] = config["label"]
            record["raw_line"] = line.strip()

            # Fill missing fields with defaults
            record.setdefault("username", "unknown")
            record.setdefault("source_ip", "unknown")
            record.setdefault("port", "0")
            record.setdefault("command", "")

            return record

    return None


def parse_log_file(input_path, output_path):
    """
    Parse an entire log file and write structured records to CSV.
    """
    fieldnames = [
        "timestamp", "hostname", "pid", "event_type",
        "username", "source_ip", "port", "label", "raw_line"
    ]

    parsed_count = 0
    skipped_count = 0

    with open(input_path, "r") as infile, open(output_path, "w", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()

        for line_num, line in enumerate(infile, 1):
            record = parse_log_line(line)
            if record:
                writer.writerow(record)
                parsed_count += 1
            else:
                skipped_count += 1

    print(f"\n{'='*50}")
    print(f"Parsing Complete!")
    print(f"{'='*50}")
    print(f"  Input:   {input_path}")
    print(f"  Output:  {output_path}")
    print(f"  Parsed:  {parsed_count} entries")
    print(f"  Skipped: {skipped_count} entries (no pattern match)")
    print(f"{'='*50}")

    return parsed_count, skipped_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Linux auth.log into structured CSV")
    parser.add_argument("--input", default="data/raw/sample_auth.log", help="Input log file path")
    parser.add_argument("--output", default="data/processed/parsed_auth.csv", help="Output CSV path")
    args = parser.parse_args()

    parse_log_file(args.input, args.output)
```

### Run it

```bash
cd ~/sdp
python3 src/log_parser.py --input data/raw/sample_auth.log --output data/processed/parsed_auth.csv
```

### ✅ Verify

```bash
# Check the output CSV
head -10 data/processed/parsed_auth.csv

# Count parsed records
wc -l data/processed/parsed_auth.csv

# Check the distribution of event types
cut -d',' -f4 data/processed/parsed_auth.csv | sort | uniq -c | sort -rn
```

Expected output:
```
  700 accepted_login
  150 failed_login
  100 invalid_user_login
   30 breakin_attempt
   20 session_opened
```

---

## Step 3: Explore the Parsed Data

### What to do
Load the parsed CSV into a Pandas DataFrame and explore the data to understand patterns.

### How to do it

Create a notebook or script `src/data_explorer.py`:

```python
"""
Data Explorer — Loads parsed CSV and provides basic statistics.

Usage:
    python src/data_explorer.py
"""

import pandas as pd

# Load the parsed data
df = pd.read_csv("data/processed/parsed_auth.csv")

print("=" * 60)
print("DATA OVERVIEW")
print("=" * 60)

# Basic info
print(f"\nTotal records: {len(df)}")
print(f"Columns: {list(df.columns)}")

# Event type distribution
print(f"\n--- Event Type Distribution ---")
print(df["event_type"].value_counts().to_string())

# Label distribution (normal vs abnormal)
print(f"\n--- Label Distribution ---")
print(df["label"].value_counts().to_string())

# Unique source IPs
print(f"\n--- Unique Source IPs ---")
print(df["source_ip"].value_counts().to_string())

# Unique usernames
print(f"\n--- Unique Usernames ---")
print(df["username"].value_counts().to_string())

# Sample records
print(f"\n--- Sample Records ---")
print(df.head(10).to_string())
```

### Run it

```bash
python3 src/data_explorer.py
```

---

## Step 4: Feature Engineering

### What to do
Transform the parsed log data into numerical features that machine learning models can understand.

### Key features to extract

| Feature | Description | How to Calculate |
|---------|-------------|-----------------|
| `failed_login_count` | Number of failed logins per IP per time window | Count `event_type == 'failed_login'` |
| `invalid_user_count` | Number of invalid user attempts per IP | Count `event_type == 'invalid_user_login'` |
| `success_login_count` | Successful logins per IP | Count `event_type == 'accepted_login'` |
| `fail_to_success_ratio` | Ratio of failed to successful logins | `failed / (successful + 1)` |
| `unique_users_attempted` | Number of different usernames tried per IP | `nunique()` on username |
| `events_per_minute` | Event frequency in a time window | Count / window_size |
| `breakin_attempts` | Break-in attempt count | Count `event_type == 'breakin_attempt'` |
| `hour_of_day` | Hour when events occurred | Extract from timestamp |
| `is_night` | Whether event occurred between 11 PM – 5 AM | 1 if night, 0 if day |

### How to do it

Create `src/feature_extractor.py`:

```python
"""
Feature Extractor — Converts parsed log CSV into ML-ready feature vectors.

Features are computed per source_ip within configurable time windows.

Usage:
    python src/feature_extractor.py --input data/processed/parsed_auth.csv --output data/processed/features.csv
"""

import pandas as pd
import numpy as np
import argparse
from datetime import datetime


def parse_log_timestamp(ts_str, year=2026):
    """Convert log timestamp (e.g., 'Mar 21 08:30:15') to datetime."""
    try:
        return datetime.strptime(f"{year} {ts_str}", "%Y %b %d %H:%M:%S")
    except ValueError:
        return None


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
        record = {
            "source_ip": ip,
            "time_window": window,
            "total_events": len(group),

            # Event type counts
            "failed_login_count": len(group[group["event_type"] == "failed_login"]),
            "invalid_user_count": len(group[group["event_type"] == "invalid_user_login"]),
            "success_login_count": len(group[group["event_type"] == "accepted_login"]),
            "breakin_attempts": len(group[group["event_type"] == "breakin_attempt"]),
            "session_opened_count": len(group[group["event_type"] == "session_opened"]),
            "sudo_count": len(group[group["event_type"] == "sudo_command"]),

            # Derived features
            "unique_users_attempted": group["username"].nunique(),
            "fail_to_success_ratio": (
                len(group[group["event_type"] == "failed_login"])
                / (len(group[group["event_type"] == "accepted_login"]) + 1)
            ),

            # Time-based features
            "hour_of_day": window.hour,
            "is_night": 1 if window.hour >= 23 or window.hour <= 5 else 0,

            # Events per minute (frequency)
            "events_per_minute": round(len(group) / window_minutes, 4),

            # Label — mark as abnormal if there are significant attack indicators
            "label": determine_label(group),
        }

        feature_records.append(record)

    # Create feature DataFrame
    features_df = pd.DataFrame(feature_records)

    # Save to CSV
    features_df.to_csv(output_path, index=False)

    print(f"\n{'='*60}")
    print(f"Feature Extraction Complete!")
    print(f"{'='*60}")
    print(f"  Input:           {input_path}")
    print(f"  Output:          {output_path}")
    print(f"  Time Window:     {window_minutes} minutes")
    print(f"  Total Samples:   {len(features_df)}")
    print(f"  Normal Samples:  {len(features_df[features_df['label'] == 'normal'])}")
    print(f"  Abnormal Samples: {len(features_df[features_df['label'] == 'abnormal'])}")
    print(f"{'='*60}")

    return features_df


def determine_label(group):
    """
    Determine if a group of events (per IP per time window) is normal or abnormal.

    Heuristic rules:
    - If there are any break-in attempts → abnormal
    - If failed logins > 5 in one window → abnormal
    - If invalid user attempts > 3 → abnormal
    - Otherwise → normal
    """
    if len(group[group["event_type"] == "breakin_attempt"]) > 0:
        return "abnormal"
    if len(group[group["event_type"] == "failed_login"]) > 5:
        return "abnormal"
    if len(group[group["event_type"] == "invalid_user_login"]) > 3:
        return "abnormal"
    return "normal"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract ML features from parsed log data")
    parser.add_argument("--input", default="data/processed/parsed_auth.csv", help="Parsed CSV path")
    parser.add_argument("--output", default="data/processed/features.csv", help="Feature CSV path")
    parser.add_argument("--window", type=int, default=60, help="Time window in minutes")
    args = parser.parse_args()

    features_df = extract_features(args.input, args.output, args.window)

    # Print sample features
    print("\n--- Sample Feature Vectors ---")
    print(features_df.head(10).to_string())
```

### Run it

```bash
cd ~/sdp
python3 src/feature_extractor.py \
  --input data/processed/parsed_auth.csv \
  --output data/processed/features.csv \
  --window 60
```

### ✅ Verify

```bash
# Preview the features
head -15 data/processed/features.csv

# Check label distribution
cut -d',' -f15 data/processed/features.csv | sort | uniq -c

# Check number of features
head -1 data/processed/features.csv | tr ',' '\n' | wc -l
```

---

## Step 5: Visualize the Features

### What to do
Create visualizations to understand the feature distributions and patterns in the data.

### How to do it

Create `src/visualizer.py`:

```python
"""
Visualizer — Creates plots for feature analysis and model results.

Usage:
    python src/visualizer.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configure plot style
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["font.size"] = 12

OUTPUT_DIR = "results/figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def plot_label_distribution(df):
    """Plot the distribution of normal vs abnormal labels."""
    fig, ax = plt.subplots()
    colors = ["#2ecc71", "#e74c3c"]
    df["label"].value_counts().plot(kind="bar", color=colors, ax=ax, edgecolor="black")
    ax.set_title("Label Distribution (Normal vs Abnormal)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Label")
    ax.set_ylabel("Count")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/label_distribution.png", dpi=150)
    print(f"Saved: {OUTPUT_DIR}/label_distribution.png")
    plt.close()


def plot_event_heatmap(df):
    """Heatmap of event types per hour of day."""
    pivot_data = df.groupby(["hour_of_day", "label"]).size().unstack(fill_value=0)
    fig, ax = plt.subplots()
    sns.heatmap(pivot_data, annot=True, fmt="d", cmap="YlOrRd", ax=ax)
    ax.set_title("Events by Hour of Day", fontsize=14, fontweight="bold")
    ax.set_ylabel("Hour of Day")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/event_heatmap.png", dpi=150)
    print(f"Saved: {OUTPUT_DIR}/event_heatmap.png")
    plt.close()


def plot_feature_comparison(df):
    """Box plots comparing key features between normal and abnormal."""
    features_to_plot = [
        "failed_login_count",
        "invalid_user_count",
        "fail_to_success_ratio",
        "unique_users_attempted",
        "events_per_minute",
    ]

    fig, axes = plt.subplots(1, len(features_to_plot), figsize=(20, 5))
    for i, feature in enumerate(features_to_plot):
        sns.boxplot(data=df, x="label", y=feature, ax=axes[i],
                    palette={"normal": "#2ecc71", "abnormal": "#e74c3c"})
        axes[i].set_title(feature, fontsize=10)

    plt.suptitle("Feature Comparison: Normal vs Abnormal", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/feature_comparison.png", dpi=150)
    print(f"Saved: {OUTPUT_DIR}/feature_comparison.png")
    plt.close()


def plot_correlation_matrix(df):
    """Correlation matrix of numerical features."""
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    corr = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Feature Correlation Matrix", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/correlation_matrix.png", dpi=150)
    print(f"Saved: {OUTPUT_DIR}/correlation_matrix.png")
    plt.close()


if __name__ == "__main__":
    df = pd.read_csv("data/processed/features.csv")

    print("Generating visualizations...\n")
    plot_label_distribution(df)
    plot_event_heatmap(df)
    plot_feature_comparison(df)
    plot_correlation_matrix(df)
    print("\nAll visualizations saved to results/figures/")
```

### Run it

```bash
python3 src/visualizer.py
```

### ✅ Verify

```bash
ls -la results/figures/
# Should show:
#   label_distribution.png
#   event_heatmap.png
#   feature_comparison.png
#   correlation_matrix.png
```

---

## 📋 Phase 2 Checklist

- [ ] Studied raw log format and identified patterns
- [ ] Built `log_parser.py` with regex patterns for all event types
- [ ] Parsed raw logs into structured CSV (`parsed_auth.csv`)
- [ ] Explored parsed data — verified event type and label distribution
- [ ] Built `feature_extractor.py` with time-window-based features
- [ ] Generated feature CSV (`features.csv`) with labeled samples
- [ ] Created visualizations (label distribution, heatmap, feature comparison, correlation matrix)
- [ ] Verified normal vs abnormal label balance in the dataset

---

## 📊 What You Should Have at the End of Phase 2

| File | Description |
|------|-------------|
| `data/processed/parsed_auth.csv` | Structured log records with fields and labels |
| `data/processed/features.csv` | ML-ready feature vectors per IP per time window |
| `results/figures/*.png` | Visualization plots |
| `src/log_parser.py` | Working log parser |
| `src/feature_extractor.py` | Working feature extractor |
| `src/visualizer.py` | Visualization scripts |

---

**⬅️ Previous: [Phase 1 — Setup & Data Collection](./PHASE_1_SETUP_AND_DATA_COLLECTION.md)**

**➡️ Next: Phase 3 — Model Development *(coming soon)***
