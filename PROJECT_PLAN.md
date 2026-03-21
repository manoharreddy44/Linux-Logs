# 🛡️ Detection of Abnormal Behavior in Linux Servers Using Machine Learning

> A machine-learning-based system that analyzes Linux server logs in real time to detect abnormal or suspicious activities — replacing traditional rule-based monitoring with intelligent, adaptive detection.

---

## 📋 Table of Contents

1. [Team Members](#team-members)
2. [Problem Statement](#problem-statement)
3. [Objective](#objective)
4. [Proposed Solution](#proposed-solution)
5. [Methodology](#methodology)
6. [System Architecture](#system-architecture)
7. [Tech Stack](#tech-stack)
8. [Project Structure](#project-structure)
9. [Implementation Plan](#implementation-plan)
10. [Research Focus](#research-focus)
11. [Expected Outcomes](#expected-outcomes)
12. [Conclusion](#conclusion)
13. [References](#references)

---

## 👥 Team Members

| # | Name               | Roll Number  |
|---|---------------------|-------------|
| 1 | Aavula Ravi Kumar   | 22BCE20046  |
| 2 | Manohar Reddy K     | 22BCE9601   |
| 3 | Rahul Kumar         | 22BCE7182   |

---

## 🔍 Problem Statement

Modern Linux servers generate **large volumes of system logs** — including auth logs, syslogs, and service logs. Traditional approaches face critical limitations:

| Challenge | Description |
|-----------|-------------|
| **Volume** | Thousands of log entries per minute make manual review impractical |
| **Complexity** | Rule-based systems cannot detect novel or sophisticated attack patterns |
| **Latency** | Delayed detection leads to extended exposure windows |
| **Adaptability** | Static rules fail to evolve with changing threat landscapes |

**There is a need for an automated, intelligent system that can identify suspicious behavior from logs in real time.**

---

## 🎯 Objective

- Design and evaluate a **machine-learning-based system** that analyzes Linux system logs and **automatically detects abnormal or suspicious server activities**.
- Compare supervised and unsupervised ML approaches for log-based anomaly detection.
- Achieve real-time detection with minimal false positives.

---

## 💡 Proposed Solution

The system collects logs from Linux servers, preprocesses and converts them into structured features, and applies machine-learning models to classify **normal** and **abnormal** behavior.

Both **supervised** and **unsupervised** techniques are explored to detect known and unknown threats.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HIGH-LEVEL FLOW                              │
│                                                                     │
│   Linux Logs ──→ Preprocessing ──→ Feature Extraction ──→ ML Model │
│                                                          │         │
│                                                    ┌─────┴─────┐   │
│                                                    │           │   │
│                                                 Normal    Abnormal │
│                                                            (Alert) │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Methodology

### Phase 1 — Log Collection
- Collect logs from Linux servers: `auth.log`, `syslog`, service-specific logs
- Automate collection using **Cron scheduler**
- Store raw logs in structured CSV format

### Phase 2 — Log Parsing & Feature Extraction
- Parse raw log entries using regex-based message templates
- Extract structured fields: `timestamp`, `type`, `tid`, `state`
- Build **time-window-based features** (e.g., event counts per window)
- Generate **state ratio vectors** and **message count vectors**

### Phase 3 — Model Training & Detection
- Implement multiple ML approaches:

| Model | Type | Purpose |
|-------|------|---------|
| Rule-based Baseline | Heuristic | Benchmark for comparison |
| Isolation Forest | Unsupervised | Detect unknown/novel anomalies |
| PCA Anomaly Detection | Unsupervised | Dimensionality reduction + outlier detection |
| Decision Tree | Supervised | Classify known attack patterns |

- Train on labeled log datasets (normal vs. abnormal)
- Tune hyperparameters for optimal precision/recall trade-off

### Phase 4 — Evaluation & Visualization
- Evaluate models using **precision**, **recall**, and **F1-score**
- Visualize results with charts, decision boundaries, and confusion matrices
- Compare model performance across different attack scenarios

---

## 🏗️ System Architecture

### Pipeline Overview

```
┌────────────┐    ┌──────────────┐    ┌───────────────────┐    ┌───────────────────┐    ┌─────────────────┐
│ Source Code │    │  1. Log      │    │  2. Feature       │    │  3. Anomaly       │    │ 4. Visualization│
│ & Raw Logs │───→│  Parsing     │───→│  Creation         │───→│  Detection        │───→│ & Reporting     │
└────────────┘    └──────────────┘    └───────────────────┘    └───────────────────┘    └─────────────────┘
       │                 │                     │                        │                        │
  Raw console       Message            State ratio             PCA-based              Decision trees,
  logs             templates &          vectors &              anomaly                charts &
                   structured logs      count vectors          detection              dashboards
```

### Detailed Steps

| Step | Input | Process | Output |
|------|-------|---------|--------|
| **1. Log Parsing** | Raw log lines (e.g., `starting: xact 325 is PREPARING`) | Regex-based template matching | Structured records (`type=1, tid=325, state=PREPARING`) |
| **2. Feature Creation** | Structured log records | Time-window aggregation, state counting | Feature vectors (e.g., `325: 1 1 1 0 0 0 0 0 0`) |
| **3. Anomaly Detection** | Feature vectors | PCA + Isolation Forest / Decision Tree | Anomaly labels (normal/abnormal) |
| **4. Visualization** | Detection results | Plotting, confusion matrix generation | Charts, reports, alerts |

### Feedback Loop

```
Detection Results ──→ Feedback / Learning ──→ Model Retraining ──→ Improved Detection
```

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Operating System** | Ubuntu Linux 24.04 LTS (Noble Numbat) |
| **Language** | Python 3.14+ |
| **Data Processing** | Pandas 3.0.1, NumPy 2.4.3 |
| **ML / Anomaly Detection** | Scikit-learn 1.8.1 (Isolation Forest, PCA, Decision Tree) |
| **Visualization** | Matplotlib 3.10.8, Seaborn 0.13.2 |
| **Log Sources** | `/var/log/auth.log`, `/var/log/syslog`, nginx access logs (optional) |
| **Storage** | CSV files |
| **Scheduling** | Cron |

---

## 📁 Project Structure

```
sdp/
├── README.md                   # Project documentation
├── PROJECT_PLAN.md             # This file
├── project-overview.md         # Slide content reference
│
├── data/
│   ├── raw/                    # Raw log files (auth.log, syslog)
│   ├── processed/              # Parsed & cleaned CSVs
│   └── sample/                 # Sample/test datasets
│
├── src/
│   ├── log_collector.py        # Log collection & scheduling
│   ├── log_parser.py           # Log parsing & structuring
│   ├── feature_extractor.py    # Feature engineering
│   ├── models/
│   │   ├── isolation_forest.py # Isolation Forest model
│   │   ├── pca_detector.py     # PCA-based anomaly detector
│   │   ├── decision_tree.py    # Decision Tree classifier
│   │   └── baseline.py         # Rule-based baseline
│   ├── evaluator.py            # Model evaluation & metrics
│   └── visualizer.py           # Plotting & reporting
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_evaluation.ipynb
│
├── results/
│   ├── figures/                # Generated plots
│   └── reports/                # Evaluation reports
│
├── requirements.txt            # Python dependencies
└── .gitignore
```

---

## 📅 Implementation Plan

### Phase-wise Timeline

| Phase | Task | Duration | Status |
|-------|------|----------|--------|
| **Phase 1** | Environment setup & log collection | Week 1–2 | ✅ Completed |
| **Phase 2** | Log parsing & feature engineering | Week 3–4 | ✅ Completed |
| **Phase 3** | Model implementation & training | Week 5–7 | ✅ Completed |
| **Phase 4** | Evaluation, visualization & report | Week 8–9 | ✅ Completed |
| **Phase 5A** | Research: Real data & methodology | Week 10 | ⬜ Not Started |
| **Phase 5B** | Research: Model expansion & tuning | Week 11 | ⬜ Not Started |
| **Phase 5C** | Research: Analysis & paper writing | Week 12 | ⬜ Not Started |

### Task Breakdown

- [x] **Phase 1 — Setup & Data Collection**
  - [x] Set up Ubuntu 24.04 LTS via Docker
  - [x] Install Python 3.12+ and dependencies
  - [x] Configure log collection from `/var/log/`
  - [x] Create sample log generator (2000 entries)
  - [x] Collect sample auth.log data

- [x] **Phase 2 — Parsing & Feature Engineering**
  - [x] Build regex-based log parser (6 patterns)
  - [x] Extract structured fields (timestamp, event type, IP, etc.)
  - [x] Implement time-window-based feature extraction (15 features)
  - [x] Generate event count vectors and ratio features
  - [x] Create labeled dataset (819 samples: 649 normal, 170 abnormal)

- [x] **Phase 3 — Model Development**
  - [x] Implement rule-based baseline detector (F1=0.99)
  - [x] Train Isolation Forest model (F1=0.22)
  - [x] Implement PCA-based anomaly detection (F1=0.00)
  - [x] Train Decision Tree classifier (F1=1.00)
  - [x] Compare all models with unified evaluator

- [x] **Phase 4 — Evaluation & Visualization**
  - [x] Compute precision, recall, F1-score for each model
  - [x] Generate confusion matrices and ROC curves
  - [x] Create comparative performance charts (15 visualizations)
  - [x] Test under 6 simulated attack scenarios
  - [x] Generate final evaluation report

- [ ] **Phase 5A — Research: Real Data & Methodology**
  - [ ] Download HDFS dataset from LogHub (real-world logs)
  - [ ] Adapt log parser for HDFS log format
  - [ ] Implement Stratified K-Fold Cross Validation (k=10)
  - [ ] Add multi-class labeling (brute_force, credential_stuffing, etc.)
  - [ ] Compare synthetic vs. real data results

- [ ] **Phase 5B — Research: Model Expansion & Tuning**
  - [ ] Implement Random Forest classifier
  - [ ] Implement XGBoost (gradient boosting)
  - [ ] Implement One-Class SVM
  - [ ] Implement MLP Neural Network
  - [ ] Hyperparameter tuning with GridSearchCV for all models

- [ ] **Phase 5C — Research: Analysis & Paper Writing**
  - [ ] Run feature ablation study
  - [ ] Perform statistical significance testing (paired t-tests)
  - [ ] Write Literature Review / Related Work section
  - [ ] Write IEEE-format research paper (8–10 pages)
  - [ ] Prepare final review presentation

---

## 🔬 Research Focus

| Area | Description |
|------|-------------|
| **ML Technique Comparison** | Comparative analysis of Isolation Forest, PCA, Decision Trees, and rule-based methods for log-based anomaly detection |
| **False Positive Analysis** | Study of false positive rates, detection accuracy, and the precision-recall trade-off |
| **System Overhead** | Measure computational cost and latency of real-time detection |
| **Realistic Evaluation** | Test under realistic server workloads and simulated attack scenarios (brute force, privilege escalation, etc.) |

---

## ✅ Expected Outcomes

1. **A working anomaly detection system** that processes Linux server logs and flags suspicious behavior in real time.
2. **Comparative analysis** showing which ML model performs best for different types of attacks.
3. **Reduced false positives** compared to traditional rule-based monitoring.
4. **Visualizations and reports** that clearly communicate detection results.
5. **Reusable codebase** that can be extended to other log sources and server environments.

---

## 📝 Conclusion

A lightweight and effective system capable of detecting suspicious Linux server behavior with improved accuracy over traditional rule-based monitoring systems. By combining multiple ML approaches (supervised + unsupervised), the system can detect both **known attack patterns** and **novel, previously unseen threats**.

---

## 📚 References

> *To be added as the project progresses.*

- Scikit-learn Documentation — https://scikit-learn.org/
- Linux System Log Documentation
- Research papers on log-based anomaly detection
- Isolation Forest (Liu et al., 2008)
- PCA-based anomaly detection methods
