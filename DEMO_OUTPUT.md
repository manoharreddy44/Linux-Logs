> **Project:** Detection of Abnormal Behavior in Linux Servers Using Machine Learning
> 

> **Run Date:** 21 March 2026
> 

> **Environment:** Docker → Ubuntu 24.04.4 LTS on macOS (Apple Silicon)
> 

---

### Step 1: Docker Environment ✅

```
PRETTY_NAME="Ubuntu 24.04.4 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.4 LTS (Noble Numbat)"
```

---

### Step 2: Library Versions ✅

```
pandas=3.0.1
numpy=2.4.3
sklearn=1.8.0
matplotlib=3.10.8
seaborn=0.13.2
```

---

### Step 3: Generate Sample Logs ✅

```
Generated 2000 log entries → data/raw/sample_auth.log
Done! Sample log file created.
```

---

### Step 4: Raw Log Preview ✅

```
Mar 01 00:06:04 server sshd[6876]: Accepted password for ravi from 192.168.1.52 port 57667 ssh2
Mar 01 00:07:09 server sshd[4507]: Accepted password for manohar from 192.168.1.52 port 50202 ssh2
Mar 01 00:18:57 server sshd[4879]: Accepted password for rahul from 192.168.1.50 port 45665 ssh2
Mar 01 00:22:49 server sshd[6238]: Accepted password for ravi from 192.168.1.52 port 64267 ssh2
Mar 01 00:23:00 server sshd[5153]: Accepted password for rahul from 192.168.1.52 port 63779 ssh2
...
Total lines: 2000
```

---

### Step 5: Parse Logs ✅

```
==================================================
Parsing Complete!
==================================================
Input:   data/raw/sample_auth.log
Output:  data/processed/parsed_auth.csv
Parsed:  2000 entries
Skipped: 0 entries (no pattern match)
==================================================
```

---

### Step 6: Data Explorer ✅

```
============================================================
DATA OVERVIEW
============================================================
Total records: 2000
Columns: ['timestamp', 'hostname', 'pid', 'event_type', 'username',
          'source_ip', 'port', 'label', 'raw_line']
```

**Event Type Distribution:**

| Event Type | Count | Percentage |
| --- | --- | --- |
| accepted_login | 495 | 24.8% |
| sudo_command | 471 | 23.5% |
| session_opened | 459 | 22.9% |
| breakin_attempt | 209 | 10.4% |
| invalid_user_login | 185 | 9.2% |
| failed_login | 181 | 9.0% |

**Label Distribution:**

| Label | Count | Percentage |
| --- | --- | --- |
| normal | 1425 | 71.2% |
| abnormal | 394 | 19.7% |
| suspicious | 181 | 9.0% |

**Source IP Distribution:**

| IP | Count | Type |
| --- | --- | --- |
| unknown (local events) | 930 | 46.5% |
| 10.0.0.100 | 199 | 10.0% — attack IP |
| 10.0.0.101 | 191 | 9.6%  — attack IP |
| 172.16.0.200 | 185 | 9.2%  — attack IP |
| 192.168.1.50 | 174 | 8.7%  — normal IP |
| 192.168.1.52 | 170 | 8.5%  — normal IP |
| 192.168.1.51 | 151 | 7.5%  — normal IP |

**Username Distribution:**

| Username | Count | Percentage |
| --- | --- | --- |
| ravi | 483 | 24.1% |
| rahul | 472 | 23.6% |
| manohar | 470 | 23.5% |
| unknown | 209 | 10.4% |
| admin | 85 | 4.2% |
| user | 74 | 3.7% |
| test | 72 | 3.6% |
| guest | 72 | 3.6% |
| root | 63 | 3.1% |

---

### Step 7: Feature Extraction ✅

```
============================================================
Feature Extraction Complete!
============================================================
Input:          data/processed/parsed_auth.csv
Output:         data/processed/features.csv
Time Window:    60 minutes
Total Samples:  815
Normal Samples: 645
Abnormal Samples: 170
Features:       18 columns
============================================================
```

**Feature Statistics:**

| Feature | Min | Max | Mean |
| --- | --- | --- | --- |
| total_events | 1 | 11 | 2.45 |
| failed_login_count | 0 | 5 | 0.22 |
| invalid_user_count | 0 | 5 | 0.23 |
| success_login_count | 0 | 5 | 0.61 |
| breakin_attempts | 0 | 4 | 0.26 |
| session_opened_count | 0 | 6 | 0.56 |
| sudo_count | 0 | 7 | 0.58 |
| unique_users_attempted | 1 | 4 | 1.68 |
| fail_to_success_ratio | 0.0 | 5.0 | 0.22 |
| invalid_to_total_ratio | 0.0 | 0.83 | 0.08 |
| attack_event_count | 0 | 5 | 0.71 |
| events_per_minute | 0.017 | 0.183 | 0.04 |

---

### Step 8: Model Evaluation — All 4 Models ✅

### Model 1: Rule-Based Baseline

```
Accuracy: 0.9951

Classification Report:
              precision  recall  f1-score  support
normal         1.00       0.99    1.00      645
abnormal       0.98       1.00    0.99      170

Confusion Matrix:
  TN= 641   FP= 4
  FN= 0     TP= 170
```

### Model 2: Isolation Forest

```
Contamination (actual abnormal ratio): 0.2086
Accuracy: 0.6933

Classification Report:
              precision  recall  f1-score  support
normal         0.81       0.80    0.81      129
abnormal       0.26       0.26    0.26      34

Confusion Matrix:
  TN= 103   FP= 26
  FN= 24    TP= 10
```

### Model 3: PCA Anomaly Detector

```
PCA components: 8 (explains 95.73% variance)
Anomaly threshold: 0.192879 (95th percentile)
Accuracy: 0.7239

Classification Report:
              precision  recall  f1-score  support
normal         0.79       0.91    0.85      129
abnormal       0.00       0.00    0.00      34

Confusion Matrix:
  TN= 118   FP= 11
  FN= 34    TP= 0
```

### Model 4: Decision Tree Classifier

```
Accuracy: 1.0000

Classification Report:
              precision  recall  f1-score  support
normal         1.00       1.00    1.00      129
abnormal       1.00       1.00    1.00      34

Confusion Matrix:
  TN= 129   FP= 0
  FN= 0     TP= 34

Top Feature Importances:
  breakin_attempts  1.0000  ██████████████████████████████████████████████████

Decision Tree Rules:
  |--- breakin_attempts <= 0.47
  |   |--- class: 0
  |--- breakin_attempts > 0.47
  |   |--- class: 1
```

### 🏆 Model Comparison Summary

| Model | Accuracy | Precision | Recall | F1-Score |
| --- | --- | --- | --- | --- |
| Rule-Based Baseline | 0.9951 | 0.9770 | 1.0000 | 0.9884 |
| Isolation Forest | 0.6933 | 0.2632 | 0.2632 | 0.2632 |
| PCA Anomaly Detector | 0.7239 | 0.0000 | 0.0000 | 0.0000 |
| **Decision Tree** 🏆 | **1.0000** | **1.0000** | **1.0000** | **1.0000** |

**Best Model: Decision Tree (F1 = 1.0000)**

---

### Step 9: Attack Scenario Simulation ✅

6 scenarios tested:

| Scenario | Expected | Baseline | Isolation Forest | PCA | Decision Tree |
| --- | --- | --- | --- | --- | --- |
| Brute Force SSH Attack | abnormal | ✅ abnormal | ✅ abnormal | ✅ abnormal | ✅ abnormal |
| Credential Stuffing | abnormal | ✅ abnormal | ✅ abnormal | ✅ abnormal | ❌ normal |
| Break-in Attempt | abnormal | ✅ abnormal | ✅ abnormal | ✅ abnormal | ✅ abnormal |
| Normal Work Activity | normal | ✅ normal | ❌ abnormal | ❌ abnormal | ✅ normal |
| Night-time Attack | abnormal | ✅ abnormal | ✅ abnormal | ✅ abnormal | ✅ abnormal |
| Privilege Escalation | normal | ✅ normal | ❌ abnormal | ❌ abnormal | ✅ normal |

**Scenario Accuracy:**

| Model | Score |
| --- | --- |
| **Rule-Based Baseline** 🏆 | **6/6 (100%)** |
| Decision Tree | 5/6 (83%) |
| Isolation Forest | 4/6 (67%) |
| PCA Detector | 4/6 (67%) |

---

### Step 10: Advanced Visualizations ✅

```
✅ Saved: results/figures/roc_curves.png
✅ Saved: results/figures/precision_recall_curves.png
✅ Saved: results/figures/feature_importance.png
✅ Saved: results/figures/scenario_heatmap.png
✅ Saved: results/figures/pca_2d_scatter.png
✅ Saved: results/figures/auc_comparison.png
```

---

### Step 11: Final Report ✅

```
==================================================
Final Report Generated!
==================================================
Output:   results/reports/final_report.md
Sections: 7
==================================================
```

---

### Step 12: Output Files Summary ✅

### Data Files

| File | Size |
| --- | --- |
| `data/processed/parsed_auth.csv` | 329 KB |
| `data/processed/features.csv` | 66 KB |

### Visualizations (15 total)

| File | Size |
| --- | --- |
| `correlation_matrix.png` | 293 KB |
| `event_timeline.png` | 264 KB |
| `decision_tree.png` | 173 KB |
| `feature_comparison.png` | 116 KB |
| `pca_2d_scatter.png` | 100 KB |
| `confusion_matrices.png` | 88 KB |
| `feature_importance.png` | 86 KB |
| `roc_curves.png` | 81 KB |
| `event_heatmap.png` | 79 KB |
| `model_comparison.png` | 78 KB |
| `precision_recall_curves.png` | 78 KB |
| `scenario_heatmap.png` | 76 KB |
| `ip_attack_distribution.png` | 61 KB |
| `auc_comparison.png` | 43 KB |
| `label_distribution.png` | 36 KB |

### Reports

| File | Description |
| --- | --- |
| `results/reports/final_report.md` | 7-section evaluation report |
| `results/reports/model_comparison.csv` | Metrics for all 4 models |
| `results/reports/scenario_results.csv` | Attack scenario results |

### Saved Models

| File | Size |
| --- | --- |
| `isolation_forest.joblib` | 1.3 MB |
| `pca_detector.joblib` | 2.3 KB |
| `decision_tree.joblib` | 1.9 KB |
| `scaler.joblib` | 0.9 KB |

---

## ✅ FULL PIPELINE COMPLETE

**Total execution: 12 steps, 0 errors, 0 skips.**