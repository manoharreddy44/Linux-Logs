"""
Log Parser — Parses raw auth.log entries into structured records.

Usage:
    docker compose exec sdp-ubuntu /opt/venv/bin/python3 /app/src/log_parser.py \
        --input data/raw/sample_auth.log \
        --output data/processed/parsed_auth.csv
"""

import re
import csv
import argparse
import os

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
            r"Failed password for (?!invalid user)(?P<username>\S+)\s+"
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

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

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
