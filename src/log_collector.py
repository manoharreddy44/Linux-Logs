"""
Automated log collector.
Copies latest log entries and appends them to the raw data directory.
Run this via cron for continuous collection.

Usage:
    python3 src/log_collector.py
"""

import shutil
import os
from datetime import datetime

# Configuration
LOG_SOURCES = {
    "auth": "/var/log/auth.log",
    "syslog": "/var/log/syslog",
}
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")


def collect_logs():
    """Copy current log files to the data directory with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for name, source_path in LOG_SOURCES.items():
        if os.path.exists(source_path):
            dest_path = os.path.join(OUTPUT_DIR, f"{name}_{timestamp}.log")
            shutil.copy2(source_path, dest_path)
            print(f"[{timestamp}] Collected {source_path} → {dest_path}")
        else:
            print(f"[{timestamp}] WARNING: {source_path} not found, skipping.")


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    collect_logs()
    print("Log collection complete.")
