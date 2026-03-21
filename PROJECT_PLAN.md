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
| **Phase 1** | Environment setup & log collection | Week 1–2 | ⬜ Not Started |
| **Phase 2** | Log parsing & feature engineering | Week 3–4 | ⬜ Not Started |
| **Phase 3** | Model implementation & training | Week 5–7 | ⬜ Not Started |
| **Phase 4** | Evaluation, visualization & report | Week 8–9 | ⬜ Not Started |
| **Phase 5** | Documentation & final presentation | Week 10 | ⬜ Not Started |

### Task Breakdown

- [ ] **Phase 1 — Setup & Data Collection**
  - [ ] Set up Ubuntu 24.04 LTS VM / environment
  - [ ] Install Python 3.14+ and dependencies
  - [ ] Configure log collection from `/var/log/`
  - [ ] Set up Cron job for automated log collection
  - [ ] Collect sample auth.log and syslog data

- [ ] **Phase 2 — Parsing & Feature Engineering**
  - [ ] Build regex-based log parser
  - [ ] Extract structured fields (timestamp, type, state, etc.)
  - [ ] Implement time-window-based feature extraction
  - [ ] Generate state ratio vectors and message count vectors
  - [ ] Create labeled dataset (normal vs. abnormal)

- [ ] **Phase 3 — Model Development**
  - [ ] Implement rule-based baseline detector
  - [ ] Train Isolation Forest model
  - [ ] Implement PCA-based anomaly detection
  - [ ] Train Decision Tree classifier
  - [ ] Hyperparameter tuning for all models

- [ ] **Phase 4 — Evaluation & Visualization**
  - [ ] Compute precision, recall, F1-score for each model
  - [ ] Generate confusion matrices
  - [ ] Create comparative performance charts
  - [ ] Test under simulated attack scenarios
  - [ ] Document findings in evaluation report

- [ ] **Phase 5 — Documentation**
  - [ ] Write final project report
  - [ ] Prepare presentation slides
  - [ ] Code documentation and cleanup

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
