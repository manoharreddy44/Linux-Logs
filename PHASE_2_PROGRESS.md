# 📓 Phase 2 — Implementation Progress Log

> **Project:** Detection of Abnormal Behavior in Linux Servers Using Machine Learning
>
> **Date:** 21 March 2026
>
> **Implemented by:** Rahul Kumar (22BCE7182)

---

## Summary

Phase 2 has been completed successfully. The log parser extracted all 2000 entries with zero
skips. Feature engineering produced 828 ML-ready samples with 18 features each. Six
visualizations were generated for data analysis.

---

## Step-by-Step Implementation Log

### Step 1: Create Log Parser ✅

**File:** `src/log_parser.py`

**What was done:**
- Built regex-based parser with 6 distinct patterns for auth.log events
- Each pattern extracts: timestamp, hostname, PID, username, source IP, port
- Auto-labels events as normal/suspicious/abnormal

**Patterns implemented:**

| Pattern | Event Type | Label |
|---------|-----------|-------|
| `Accepted password for <user> from <ip>` | `accepted_login` | normal |
| `Failed password for <user> from <ip>` | `failed_login` | suspicious |
| `Failed password for invalid user <user>` | `invalid_user_login` | abnormal |
| `POSSIBLE BREAK-IN ATTEMPT from <ip>` | `breakin_attempt` | abnormal |
| `pam_unix(sshd:session): session opened` | `session_opened` | normal |
| `sudo: <user> : ... COMMAND=<cmd>` | `sudo_command` | normal |

**Command:**
```bash
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/log_parser.py \
    --input data/raw/sample_auth.log \
    --output data/processed/parsed_auth.csv
```

**Result:** ✅ No errors
```
Parsed:  2000 entries
Skipped: 0 entries (no pattern match)
```

---

### Step 2: Explore Parsed Data ✅

**File:** `src/data_explorer.py`

**Command:**
```bash
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/data_explorer.py
```

**Result:** ✅ No errors

**Event type distribution:**

| Event Type | Count | Percentage |
|-----------|-------|------------|
| session_opened | 470 | 23.5% |
| accepted_login | 466 | 23.3% |
| sudo_command | 446 | 22.3% |
| breakin_attempt | 221 | 11.1% |
| invalid_user_login | 208 | 10.4% |
| failed_login | 189 | 9.4% |

**Label distribution:**

| Label | Count | Percentage |
|-------|-------|------------|
| normal | 1382 | 69.1% |
| abnormal | 429 | 21.4% |
| suspicious | 189 | 9.4% |

**Source IP distribution:**

| IP | Count | Type |
|----|-------|------|
| unknown (local events) | 916 | 45.8% — sudo/session (no IP) |
| 10.0.0.101 | 213 | 10.7% — attack IP |
| 172.16.0.200 | 209 | 10.4% — attack IP |
| 10.0.0.100 | 196 | 9.8% — attack IP |
| 192.168.1.50 | 162 | 8.1% — normal IP |
| 192.168.1.51 | 153 | 7.6% — normal IP |
| 192.168.1.52 | 151 | 7.5% — normal IP |

---

### Step 3: Feature Engineering ✅

**File:** `src/feature_extractor.py`

**What was done:**
- Groups parsed logs by **source_ip** and **1-hour time windows**
- Computes 15 numerical features + label per group
- Uses heuristic rules for labeling (breakin attempts, failed count > 5, etc.)

**Features extracted (18 columns total):**

| Feature | Min | Max | Mean | Description |
|---------|-----|-----|------|-------------|
| total_events | 1 | 11 | 2.42 | Events in window |
| failed_login_count | 0 | 4 | 0.23 | Failed SSH logins |
| invalid_user_count | 0 | 5 | 0.25 | Invalid user attempts |
| success_login_count | 0 | 4 | 0.56 | Successful logins |
| breakin_attempts | 0 | 4 | 0.27 | Break-in alerts |
| session_opened_count | 0 | 9 | 0.57 | Sessions opened |
| sudo_count | 0 | 7 | 0.54 | Sudo commands |
| unique_users_attempted | 1 | 4 | 1.67 | Distinct usernames |
| fail_to_success_ratio | 0.0 | 4.0 | 0.23 | Failed/success ratio |
| invalid_to_total_ratio | 0.0 | 0.83 | 0.09 | Invalid/total ratio |
| attack_event_count | 0 | 5 | 0.75 | Combined attack events |
| hour_of_day | 0 | 23 | 11.42 | Hour of day |
| is_night | 0 | 1 | 0.30 | Night hours flag |
| is_weekend | 0 | 1 | 0.29 | Weekend flag |
| events_per_minute | 0.017 | 0.183 | 0.04 | Event frequency |

**Command:**
```bash
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/feature_extractor.py \
    --input data/processed/parsed_auth.csv \
    --output data/processed/features.csv \
    --window 60
```

**Result:** ✅ No errors
```
Total Samples:    828
Normal Samples:   649
Abnormal Samples: 179
Features:         18 columns
```

---

### Step 4: Generate Visualizations ✅

**File:** `src/visualizer.py`

**Command:**
```bash
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/visualizer.py data/processed/features.csv
```

**Result:** ✅ No errors — 6 charts generated

| Chart | File | Description |
|-------|------|-------------|
| Label Distribution | `results/figures/label_distribution.png` | Normal vs abnormal bar chart |
| Event Heatmap | `results/figures/event_heatmap.png` | Events by hour × label |
| Feature Comparison | `results/figures/feature_comparison.png` | Box plots per label |
| Correlation Matrix | `results/figures/correlation_matrix.png` | Feature correlations |
| IP Attack Distribution | `results/figures/ip_attack_distribution.png` | Attacks per source IP |
| Event Timeline | `results/figures/event_timeline.png` | Time series of events |

**Note:** Used `matplotlib.use("Agg")` backend for headless rendering in Docker (no display needed).

---

## Errors Summary

| # | Error | Fix |
|---|-------|-----|
| — | None | Phase 2 ran with zero errors |

---

## Output Files

| File | Location | Size | Records |
|------|----------|------|---------|
| Parsed CSV | `data/processed/parsed_auth.csv` | 2001 lines | 2000 entries |
| Feature CSV | `data/processed/features.csv` | 829 lines | 828 samples |
| Label Distribution | `results/figures/label_distribution.png` | 36 KB | — |
| Event Heatmap | `results/figures/event_heatmap.png` | 82 KB | — |
| Feature Comparison | `results/figures/feature_comparison.png` | 106 KB | — |
| Correlation Matrix | `results/figures/correlation_matrix.png` | 298 KB | — |
| IP Attack Distribution | `results/figures/ip_attack_distribution.png` | 62 KB | — |
| Event Timeline | `results/figures/event_timeline.png` | 272 KB | — |

---

## Docker Commands Used

```bash
# Parse logs
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/log_parser.py \
    --input data/raw/sample_auth.log --output data/processed/parsed_auth.csv

# Explore data
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/data_explorer.py

# Extract features
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/feature_extractor.py \
    --input data/processed/parsed_auth.csv --output data/processed/features.csv --window 60

# Generate visualizations
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/visualizer.py data/processed/features.csv
```

---

## Phase 2 Checklist — COMPLETED ✅

- [x] Studied raw log format and identified 6 patterns
- [x] Built `log_parser.py` with regex patterns for all event types
- [x] Parsed raw logs into structured CSV — 2000/2000, 0 skipped
- [x] Explored parsed data — verified event type and label distribution
- [x] Built `feature_extractor.py` with 15 features per IP/time-window
- [x] Generated feature CSV — 828 samples, 18 columns, 649 normal / 179 abnormal
- [x] Created 6 visualizations (label dist, heatmap, comparison, correlation, IP attacks, timeline)
- [x] Verified all output files exist and are valid

---

**⬅️ Previous: [Phase 1 — Progress](./PHASE_1_PROGRESS.md)**

**➡️ Next: Phase 3 — Model Development *(coming next)*
