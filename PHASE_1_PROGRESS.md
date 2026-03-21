# 📓 Phase 1 — Implementation Progress Log

> **Project:** Detection of Abnormal Behavior in Linux Servers Using Machine Learning
>
> **Date:** 21 March 2026
>
> **Implemented by:** Rahul Kumar (22BCE7182)

---

## Summary

Phase 1 has been completed successfully. A Docker-based Ubuntu 24.04 LTS environment is running
with Python 3.12.3 and all required ML libraries. 2000 sample log entries have been generated
for training.

---

## Step-by-Step Implementation Log

### Step 1: Create Docker Configuration Files ✅

**What was done:**
- Created `Dockerfile` — Ubuntu 24.04 LTS base image with Python, SSH, rsyslog, cron
- Created `docker-compose.yml` — container orchestration with volume mounts
- Created `docker-entrypoint.sh` — starts rsyslog, cron, SSH on container boot
- Created `requirements.txt` — Python dependencies

**Files created:**

| File | Purpose |
|------|---------|
| `Dockerfile` | Ubuntu 24.04 image with all system packages |
| `docker-compose.yml` | Container config with volume mounts |
| `docker-entrypoint.sh` | Startup script for log services |
| `requirements.txt` | Python ML library dependencies |

---

### Step 2: Build Docker Container ✅

**Command:**
```bash
docker compose build
```

**⚠️ Error #1 — scikit-learn version not found**

```
ERROR: Could not find a version that satisfies the requirement scikit-learn>=1.8.1
ERROR: No matching distribution found for scikit-learn>=1.8.1
```

**Root Cause:**
Ubuntu 24.04 ships with **Python 3.12.3**. The `scikit-learn 1.8.1` release does not have
a pre-built wheel for Python 3.12 on `aarch64` (Apple Silicon / ARM64). The latest available
compatible version is `scikit-learn 1.8.0`.

**Fix:**
Changed `requirements.txt`:
```diff
- scikit-learn>=1.8.1
+ scikit-learn>=1.8.0
```

Also relaxed matplotlib:
```diff
- matplotlib>=3.10.8
+ matplotlib>=3.10.0
```

**Result:** Build succeeded after fix.

---

### Step 3: Start Docker Container ✅

**Command:**
```bash
docker compose up -d
```

**Output:**
```
✔ Network sdp_default      Created
✔ Container sdp-linux-env  Started
```

**Verification:**
```bash
docker compose exec sdp-ubuntu cat /etc/os-release
```
```
PRETTY_NAME="Ubuntu 24.04.4 LTS"
VERSION="24.04.4 LTS (Noble Numbat)"
```

---

### Step 4: Verify Python Libraries ✅

**⚠️ Error #2 — Python libraries not found in container**

```
ModuleNotFoundError: No module named 'pandas'
```

**Root Cause:**
The `Dockerfile` creates a virtual environment at `/app/venv`, but `docker-compose.yml`
mounts the host project directory to `/app`, which **overwrites** the venv created during
the build step.

**Fix:**
1. Changed venv location from `/app/venv` to `/opt/venv` in the `Dockerfile`
2. Installed dependencies in `/opt/venv` inside the running container
3. Updated `ENV PATH` to `/opt/venv/bin:$PATH`

```diff
- RUN python3 -m venv /app/venv && \
-     /app/venv/bin/pip install --upgrade pip && \
-     /app/venv/bin/pip install -r requirements.txt
- ENV PATH="/app/venv/bin:$PATH"
+ RUN python3 -m venv /opt/venv && \
+     /opt/venv/bin/pip install --upgrade pip && \
+     /opt/venv/bin/pip install -r requirements.txt
+ ENV PATH="/opt/venv/bin:$PATH"
```

**Verified library versions:**

| Library | Version |
|---------|---------|
| Python | 3.12.3 |
| pandas | 3.0.1 |
| numpy | 2.4.3 |
| scikit-learn | 1.8.0 |
| matplotlib | 3.10.8 |
| seaborn | 0.13.2 |

---

### Step 5: Create Project Directory Structure ✅

**Command:**
```bash
mkdir -p data/raw data/processed data/sample src/models notebooks results/figures results/reports
```

**Structure created:**
```
sdp/
├── Dockerfile
├── docker-compose.yml
├── docker-entrypoint.sh
├── requirements.txt
├── .gitignore
├── PROJECT_PLAN.md
├── PHASE_1_SETUP_AND_DATA_COLLECTION.md
├── PHASE_2_PARSING_AND_FEATURES.md
├── data/
│   ├── raw/              ← sample_auth.log (2000 entries)
│   ├── processed/        ← (for Phase 2)
│   └── sample/
├── src/
│   ├── __init__.py
│   ├── generate_sample_logs.py
│   ├── log_collector.py
│   └── models/
│       └── __init__.py
├── notebooks/
└── results/
    ├── figures/
    └── reports/
```

---

### Step 6: Generate Sample Log Data ✅

**Command:**
```bash
docker compose exec sdp-ubuntu /opt/venv/bin/python3 /app/src/generate_sample_logs.py
```

**Output:**
```
Generated 2000 log entries → data/raw/sample_auth.log
Done! Sample log file created.
```

**Data statistics:**

| Metric | Count |
|--------|-------|
| **Total log entries** | 2000 |
| Accepted (successful login) | 466 |
| Failed password attempts | 397 |
| Break-in attempts | 221 |
| Session opened | ~460 |
| Sudo commands | ~456 |

**Sample data (first 5 lines):**
```
Mar 01 00:07:48 server sshd[9482]: pam_unix(sshd:session): session opened for user ravi
Mar 01 00:09:47 server sshd[2301]: pam_unix(sshd:session): session opened for user rahul
Mar 01 00:09:48 server sshd[3699]: Failed password for invalid user test from 172.16.0.200 port 46352 ssh2
Mar 01 00:10:29 server sudo: rahul : TTY=pts/0 ; PWD=/home/rahul ; USER=root ; COMMAND=/bin/ls
Mar 01 00:13:50 server sshd[3172]: Failed password for invalid user test from 10.0.0.100 port 51916 ssh2
```

---

### Step 7: Test Log Collector Script ✅

**Command:**
```bash
docker compose exec sdp-ubuntu /opt/venv/bin/python3 /app/src/log_collector.py
```

**Output:**
```
[20260321_034438] WARNING: /var/log/auth.log not found, skipping.
[20260321_034438] WARNING: /var/log/syslog not found, skipping.
Log collection complete.
```

**Note:** Real system logs (`/var/log/auth.log`, `/var/log/syslog`) are not generated inside
the Docker container because `rsyslog` doesn't fully operate in containers.
This is expected — we use **sample-generated logs** as our primary data source for training.

---

## Errors Summary

| # | Error | Root Cause | Fix |
|---|-------|-----------|-----|
| 1 | `scikit-learn>=1.8.1` not found | No wheel for Python 3.12 on ARM64 | Changed to `>=1.8.0` |
| 2 | `ModuleNotFoundError: No module named 'pandas'` | Volume mount overwrites `/app/venv` | Moved venv to `/opt/venv` |

---

## Environment Details

| Component | Version / Detail |
|-----------|-----------------|
| **Host OS** | macOS (Apple Silicon) |
| **Docker** | Docker Desktop |
| **Container OS** | Ubuntu 24.04.4 LTS (Noble Numbat) |
| **Python** | 3.12.3 |
| **pandas** | 3.0.1 |
| **numpy** | 2.4.3 |
| **scikit-learn** | 1.8.0 |
| **matplotlib** | 3.10.8 |
| **seaborn** | 0.13.2 |
| **scipy** | 1.17.1 |
| **pillow** | 12.1.1 |

---

## Docker Commands Quick Reference

```bash
# Build the container
docker compose build

# Start the container
docker compose up -d

# Enter the container shell
docker compose exec sdp-ubuntu bash

# Run a Python script inside container
docker compose exec sdp-ubuntu /opt/venv/bin/python3 /app/src/generate_sample_logs.py

# Stop the container
docker compose down

# Rebuild from scratch
docker compose build --no-cache
```

---

## Phase 1 Checklist — COMPLETED ✅

- [x] Docker Desktop installed and running
- [x] Dockerfile and docker-compose.yml created
- [x] Ubuntu 24.04 LTS container built and running
- [x] Python 3.12.3 available inside the container
- [x] Virtual environment with all dependencies (Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn)
- [x] Understood key Linux log files (auth.log, syslog)
- [x] Project directory structure created
- [x] Sample log file generated (2000 entries, 70% normal / 30% abnormal)
- [x] Log collector script working (tested, skips missing files gracefully)

---

**➡️ Next: [Phase 2 — Log Parsing & Feature Engineering](./PHASE_2_PARSING_AND_FEATURES.md)**
