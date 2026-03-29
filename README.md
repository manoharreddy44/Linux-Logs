<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Ubuntu-24.04_LTS-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" />
  <img src="https://img.shields.io/badge/scikit--learn-1.8-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

<h1 align="center">🛡️ Detection of Abnormal Behavior in Linux Servers<br/>Using Machine Learning</h1>

<p align="center">
  <b>An intelligent, ML-powered system that analyzes Linux server logs in real time to detect abnormal or suspicious activities — replacing traditional rule-based monitoring with adaptive, data-driven detection.</b>
</p>

<p align="center">
  <a href="#-key-results">Key Results</a> •
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-models--performance">Models</a> •
  <a href="#-project-structure">Structure</a> •
  <a href="#-team">Team</a>
</p>

---

## 📊 Key Results

<table>
  <tr>
    <td align="center"><b>🏆 Best F1-Score</b><br/><code>1.00</code></td>
    <td align="center"><b>📈 Best Accuracy</b><br/><code>100%</code></td>
    <td align="center"><b>🔍 Models Compared</b><br/><code>4</code></td>
    <td align="center"><b>📝 Log Entries</b><br/><code>2,000</code></td>
    <td align="center"><b>🧪 Features Extracted</b><br/><code>15</code></td>
    <td align="center"><b>⚔️ Attack Scenarios</b><br/><code>6</code></td>
  </tr>
</table>

| Model | Type | Accuracy | Precision | Recall | F1-Score |
|:------|:-----|:--------:|:---------:|:------:|:--------:|
| Decision Tree 🏆 | Supervised | **1.0000** | **1.0000** | **1.0000** | **1.0000** |
| Rule-Based Baseline | Heuristic | 0.9951 | 0.9770 | 1.0000 | 0.9884 |
| Isolation Forest | Unsupervised | 0.6951 | 0.2333 | 0.2059 | 0.2188 |
| PCA Anomaly Detector | Unsupervised | 0.7256 | 0.0000 | 0.0000 | 0.0000 |

---

## ✨ Features

- **🔄 End-to-End ML Pipeline** — From raw log ingestion to anomaly detection and reporting
- **🤖 4 ML Models** — Rule-based baseline, Isolation Forest, PCA Detector, and Decision Tree
- **📊 15 Visualizations** — ROC curves, confusion matrices, feature importance, attack heatmaps, and more
- **⚔️ Attack Simulation** — 6 realistic attack scenarios (brute force, credential stuffing, privilege escalation)
- **🐳 Docker Environment** — Fully reproducible Ubuntu 24.04 LTS environment
- **⏱️ Time-Window Features** — Behavioral pattern extraction over configurable time windows
- **📋 Auto-Labeling** — Heuristic-based labeling eliminates manual annotation
- **🔬 Cross-Validation** — K-Fold cross-validation for robust model evaluation

---

## 🔍 Problem Statement

Modern Linux servers generate **thousands of log entries per minute** — including auth logs, syslogs, and service logs. Traditional monitoring faces critical limitations:

| Challenge | Description |
|-----------|-------------|
| **Volume** | Massive log volumes make manual review impractical |
| **Complexity** | Rule-based systems cannot detect novel or sophisticated attack patterns |
| **Latency** | Delayed detection leads to extended exposure windows |
| **Adaptability** | Static rules fail to evolve with changing threat landscapes |

**This project solves these challenges** by applying machine learning to automatically identify suspicious behavior from server logs — both known attack patterns and novel, previously unseen threats.

---

## 🚀 Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/manoharreddy44/Linux-Logs.git
cd Linux-Logs
```

### 2. Build & Start the Docker Environment

```bash
docker-compose up -d --build
docker exec -it sdp-linux-env bash
```

### 3. Run the Full Pipeline

```bash
# Step 1: Generate sample logs
python3 src/generate_sample_logs.py

# Step 2: Parse raw logs
python3 src/log_parser.py

# Step 3: Explore data
python3 src/data_explorer.py

# Step 4: Extract features
python3 src/feature_extractor.py

# Step 5: Train & evaluate all models
python3 src/evaluator.py

# Step 6: Generate visualizations
python3 src/visualizer.py
python3 src/advanced_visualizer.py

# Step 7: Simulate attack scenarios
python3 src/attack_simulator.py

# Step 8: Generate final report
python3 src/report_generator.py
```

### Alternative: Run Without Docker

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the pipeline (same steps as above)
```

---

## 🏗️ Architecture

### System Pipeline

```
┌────────────┐    ┌──────────────┐    ┌───────────────────┐    ┌───────────────────┐    ┌─────────────────┐
│  Raw Logs  │    │  Log Parsing │    │    Feature         │    │    Anomaly         │    │  Visualization  │
│  (auth.log,│───▶│  (regex      │───▶│    Extraction      │───▶│    Detection       │───▶│  & Reporting    │
│   syslog)  │    │   patterns)  │    │    (time-windows)  │    │    (ML models)     │    │  (charts, PDF)  │
└────────────┘    └──────────────┘    └───────────────────┘    └───────────────────┘    └─────────────────┘
```

### Detailed Data Flow

| Stage | Input | Process | Output |
|:------|:------|:--------|:-------|
| **1. Log Parsing** | Raw log lines (`auth.log`) | Regex-based template matching (6 patterns) | Structured CSV (`timestamp`, `event_type`, `IP`, etc.) |
| **2. Feature Extraction** | Parsed CSV records | Time-window aggregation (60-min windows) | 15 numerical features per sample |
| **3. Model Training** | Feature vectors (819 samples) | Train 4 ML models (supervised + unsupervised) | Trained models (`.joblib` files) |
| **4. Detection** | New feature vectors | Model inference + threshold-based classification | Anomaly labels (normal / abnormal) |
| **5. Reporting** | Detection results | Metrics computation + visualization | Charts, confusion matrices, reports |

### Feedback Loop

```
Detection Results ──▶ Performance Analysis ──▶ Model Retraining ──▶ Improved Detection
```

---

## 🤖 Models & Performance

### Decision Tree (Best Model — F1: 1.00)

The Decision Tree achieved **perfect classification** by discovering a single, highly discriminative rule:

```
IF breakin_attempts > 0.47 → ABNORMAL
ELSE                       → NORMAL
```

**Why it works:** Supervised models excel when you have well-labeled training data and need to detect known attack patterns.

### Rule-Based Baseline (F1: 0.99)

A threshold-based heuristic detector that serves as the performance benchmark. Achieves near-perfect results by checking for known malicious indicators.

### Isolation Forest (F1: 0.22)

An unsupervised approach that isolates anomalies via random partitioning. Lower performance on synthetic data, but valuable for **detecting novel, unknown threats** in production where labeled data may not exist.

### PCA Anomaly Detector (F1: 0.00)

Detects anomalies via reconstruction error after dimensionality reduction. Best suited for environments where anomalies are **structurally different** from normal behavior.

### Attack Scenario Results

| Scenario | Expected | Baseline | Isolation Forest | PCA | Decision Tree |
|:---------|:---------|:--------:|:----------------:|:---:|:-------------:|
| Brute Force SSH | abnormal | ✅ | ✅ | ✅ | ✅ |
| Credential Stuffing | abnormal | ✅ | ✅ | ✅ | ❌ |
| Break-in Attempt | abnormal | ✅ | ✅ | ✅ | ✅ |
| Normal Work Activity | normal | ✅ | ❌ | ❌ | ✅ |
| Night-time Attack | abnormal | ✅ | ✅ | ✅ | ✅ |
| Privilege Escalation | normal | ✅ | ❌ | ❌ | ✅ |

> **Recommendation:** A **hybrid approach** combining supervised models for known threats with unsupervised models for novel attacks delivers the best real-world coverage.

---

## 🔧 Feature Engineering

15 features are extracted from raw logs using **time-window aggregation** (default: 60-minute windows):

| Feature | Description | Type |
|:--------|:------------|:-----|
| `total_events` | Total events in time window | Count |
| `failed_login_count` | Failed SSH login attempts | Count |
| `invalid_user_count` | Login attempts with invalid usernames | Count |
| `success_login_count` | Successful logins | Count |
| `breakin_attempts` | Break-in attempt alerts | Count |
| `session_opened_count` | New sessions opened | Count |
| `sudo_count` | Sudo command executions | Count |
| `unique_users_attempted` | Distinct usernames seen | Count |
| `unique_ips` | Distinct source IPs | Count |
| `fail_to_success_ratio` | Failed / successful login ratio | Ratio |
| `invalid_to_total_ratio` | Invalid user attempts / total events | Ratio |
| `attack_event_count` | Combined attack-related events | Count |
| `events_per_minute` | Event frequency in the window | Rate |
| `hour` | Hour of day (0–23) | Temporal |
| `is_night` | Whether event is during off-hours | Binary |

---

## 📁 Project Structure

```
Linux-Logs/
│
├── 📄 README.md                        # You are here
├── 📄 PROJECT_PLAN.md                  # Detailed project plan & timeline
├── 📄 KEY_INSIGHTS_AND_FINDINGS.md     # Research insights & analysis
├── 📄 DEMO_OUTPUT.md                   # Full pipeline demo output
├── 📄 REVIEW_PRESENTATION_GUIDE.md     # Presentation guide
├── 📄 RESEARCH_UPGRADE_PLAN.md         # Phase 5 research roadmap
│
├── 🐳 Dockerfile                       # Ubuntu 24.04 LTS environment
├── 🐳 docker-compose.yml              # Container orchestration
├── 🐳 docker-entrypoint.sh            # Container startup script
├── 📄 requirements.txt                 # Python dependencies
├── 📄 .gitignore
│
├── 📂 src/                             # Source code
│   ├── log_collector.py               #   Log collection & scheduling
│   ├── log_parser.py                  #   Regex-based log parsing (6 patterns)
│   ├── generate_sample_logs.py        #   Synthetic log generator (2000 entries)
│   ├── data_explorer.py               #   Dataset statistics & exploration
│   ├── feature_extractor.py           #   Time-window feature engineering
│   ├── evaluator.py                   #   Unified model evaluation
│   ├── cross_validator.py             #   K-Fold cross-validation
│   ├── attack_simulator.py            #   Attack scenario testing (6 scenarios)
│   ├── visualizer.py                  #   Basic visualization (9 charts)
│   ├── advanced_visualizer.py         #   Advanced plots (ROC, PR curves, etc.)
│   ├── report_generator.py            #   Final report generation
│   └── models/
│       ├── baseline.py                #   Rule-based heuristic detector
│       ├── isolation_forest.py        #   Isolation Forest (unsupervised)
│       ├── pca_detector.py            #   PCA anomaly detection (unsupervised)
│       ├── decision_tree.py           #   Decision Tree classifier (supervised)
│       ├── autoencoder.py             #   Autoencoder-based detector (deep learning)
│       ├── dnn_classifier.py          #   Deep Neural Network classifier
│       └── lstm_detector.py           #   LSTM sequence-based detector
│
├── 📂 data/
│   ├── raw/                           #   Raw log files (auth.log, syslog)
│   ├── processed/                     #   Parsed CSVs & feature matrices
│   └── sample/                        #   Sample/test datasets
│
├── 📂 results/
│   ├── figures/                       #   15 generated visualizations
│   │   ├── roc_curves.png
│   │   ├── confusion_matrices.png
│   │   ├── feature_importance.png
│   │   ├── precision_recall_curves.png
│   │   ├── model_comparison.png
│   │   ├── scenario_heatmap.png
│   │   ├── pca_2d_scatter.png
│   │   ├── decision_tree.png
│   │   ├── correlation_matrix.png
│   │   └── ... (15 total)
│   ├── models/                        #   Saved model files (.joblib)
│   └── reports/                       #   Evaluation reports & CSVs
│
└── 📂 notebooks/                      #   Jupyter notebooks (exploration)
```

---

## 📊 Generated Visualizations

The pipeline produces **15 publication-ready visualizations**:

| Visualization | Description |
|:-------------|:------------|
| `model_comparison.png` | Bar chart comparing all 4 models across metrics |
| `confusion_matrices.png` | Side-by-side confusion matrices |
| `roc_curves.png` | ROC curves with AUC scores |
| `precision_recall_curves.png` | Precision-Recall trade-off curves |
| `feature_importance.png` | Decision Tree feature importance ranking |
| `decision_tree.png` | Visual representation of learned decision rules |
| `pca_2d_scatter.png` | 2D PCA projection of normal vs. abnormal samples |
| `correlation_matrix.png` | Feature correlation heatmap |
| `scenario_heatmap.png` | Attack scenario detection heatmap |
| `event_timeline.png` | Temporal distribution of events |
| `event_heatmap.png` | Event frequency heatmap by hour |
| `label_distribution.png` | Dataset label distribution |
| `ip_attack_distribution.png` | Attack distribution by source IP |
| `feature_comparison.png` | Feature distributions: normal vs. abnormal |
| `auc_comparison.png` | AUC score comparison bar chart |

---

## 🛠️ Tech Stack

| Category | Technology |
|:---------|:-----------|
| **OS** | Ubuntu 24.04 LTS (Noble Numbat) |
| **Language** | Python 3.14+ |
| **Data Processing** | Pandas 3.0.1, NumPy 2.4.3 |
| **ML / Anomaly Detection** | Scikit-learn 1.8.0 |
| **Deep Learning** | TensorFlow 2.16+ |
| **Visualization** | Matplotlib 3.10.8, Seaborn 0.13.2 |
| **Containerization** | Docker, Docker Compose |
| **Log Sources** | `/var/log/auth.log`, `/var/log/syslog` |

---

## 📅 Project Timeline

| Phase | Task | Status |
|:------|:-----|:------:|
| **Phase 1** | Environment setup & log collection | ✅ Complete |
| **Phase 2** | Log parsing & feature engineering | ✅ Complete |
| **Phase 3** | Model implementation & training | ✅ Complete |
| **Phase 4** | Evaluation, visualization & reporting | ✅ Complete |
| **Phase 5A** | Research: Real-world data & K-Fold CV | 🔜 Planned |
| **Phase 5B** | Research: Model expansion (RF, XGBoost, SVM, MLP) | 🔜 Planned |
| **Phase 5C** | Research: IEEE paper writing | 🔜 Planned |

---

## 🔮 Roadmap

- [ ] Integrate **real-world datasets** (HDFS LogHub, production auth.log)
- [ ] Implement **Random Forest** and **XGBoost** classifiers
- [ ] Add **One-Class SVM** for unsupervised detection
- [ ] Train **MLP Neural Network** for deep learning comparison
- [ ] Implement **Stratified K-Fold Cross-Validation** (k=10)
- [ ] **Hyperparameter tuning** with GridSearchCV
- [ ] Feature ablation study & statistical significance testing
- [ ] **Real-time streaming detection** pipeline
- [ ] Alert system integration (email / Slack)
- [ ] IEEE-format research paper (8–10 pages)

---

## 👥 Team

| Name | Roll Number |
|:-----|:------------|
| **Aavula Ravi Kumar** | 22BCE20046 |
| **Manohar Reddy K** | 22BCE9601 |
| **Rahul Kumar** | 22BCE7182 |

---

## 📚 References

- Liu, F.T., Ting, K.M. and Zhou, Z.H. (2008). *Isolation Forest*. IEEE International Conference on Data Mining.
- He, S., Zhu, J., He, P. and Lyu, M.R. (2016). *Experience Report: System Log Analysis for Anomaly Detection*. IEEE ISSRE.
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [LogHub Datasets](https://github.com/logpai/loghub) — Real-world log data for research

---

## 📄 License

This project is developed as part of an academic Software Development Project (SDP).

---

<p align="center">
  <b>⭐ If you find this project useful, consider giving it a star!</b>
</p>
