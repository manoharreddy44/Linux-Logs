# 🤖 Phase 3 — Model Development & Training

> **Goal:** Implement and train multiple ML models to detect anomalies in Linux server logs. Compare rule-based, supervised, and unsupervised approaches.
>
> **Duration:** Week 5–7
>
> **Prerequisites:** [Phase 2](./PHASE_2_PARSING_AND_FEATURES.md) completed — `data/processed/features.csv` exists with 800+ labeled feature vectors.

---

## Step 1: Load and Prepare the Dataset

### What to do
Load the feature CSV, split into training and test sets, and prepare for ML model training.

### How to do it

All models will use this shared data preparation flow:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load features
df = pd.read_csv("data/processed/features.csv")

# Select numeric feature columns (exclude metadata)
feature_cols = [
    "total_events", "failed_login_count", "invalid_user_count",
    "success_login_count", "breakin_attempts", "session_opened_count",
    "sudo_count", "unique_users_attempted", "fail_to_success_ratio",
    "invalid_to_total_ratio", "attack_event_count", "hour_of_day",
    "is_night", "is_weekend", "events_per_minute",
]

X = df[feature_cols]
y = df["label"]  # "normal" or "abnormal"

# Encode labels: normal=0, abnormal=1
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split: 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)
```

### ✅ Verify

```bash
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 -c "
import pandas as pd
df = pd.read_csv('data/processed/features.csv')
print(f'Total samples: {len(df)}')
print(f'Label distribution: {df[\"label\"].value_counts().to_dict()}')
print(f'Feature columns: {len(df.columns) - 3} numeric features')
print('✅ Data ready for model training')
"
```

---

## Step 2: Implement Rule-Based Baseline

### What to do
Create a simple heuristic-based detector as a baseline to compare ML models against.

### How to do it

Create `src/models/baseline.py`:

**Rules:**
- If `breakin_attempts > 0` → abnormal
- If `failed_login_count > 3` → abnormal
- If `invalid_user_count > 2` → abnormal
- If `fail_to_success_ratio > 2.0` → abnormal
- Otherwise → normal

**Run:**
```bash
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/models/baseline.py
```

### Expected output
- Precision, recall, F1-score, confusion matrix
- This serves as the **minimum bar** — ML models should beat this

---

## Step 3: Implement Isolation Forest (Unsupervised)

### What to do
Train an Isolation Forest model for anomaly detection. This model doesn't need labels — it learns the concept of "normal" and flags outliers.

### How to do it

Create `src/models/isolation_forest.py`:

**Key parameters:**
- `n_estimators=100` — number of trees
- `contamination=0.2` — expected proportion of anomalies (~20%)
- `random_state=42` — reproducibility

**How it works:**
1. Isolation Forest randomly selects a feature and split value
2. Anomalies are isolated in fewer splits (shorter path length)
3. Normal points require more splits to isolate

**Run:**
```bash
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/models/isolation_forest.py
```

---

## Step 4: Implement PCA Anomaly Detection (Unsupervised)

### What to do
Use Principal Component Analysis to reduce dimensionality and detect anomalies based on reconstruction error.

### How to do it

Create `src/models/pca_detector.py`:

**How it works:**
1. Fit PCA on training data, keeping `n_components` that explain ~95% variance
2. Transform data to principal components and back (reconstruct)
3. High reconstruction error → likely anomaly
4. Set threshold at the 95th percentile of training errors

**Run:**
```bash
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/models/pca_detector.py
```

---

## Step 5: Implement Decision Tree Classifier (Supervised)

### What to do
Train a Decision Tree on labeled data. This is a supervised model that learns decision rules from the training labels.

### How to do it

Create `src/models/decision_tree.py`:

**Key parameters:**
- `max_depth=5` — limit tree depth to avoid overfitting
- `min_samples_split=5` — minimum samples to split a node
- `random_state=42` — reproducibility

**Advantages:**
- Interpretable — you can see the exact rules
- Fast to train and predict
- Produces a visual decision tree

**Run:**
```bash
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/models/decision_tree.py
```

---

## Step 6: Create Model Evaluator

### What to do
Build a unified evaluation script that runs all models, compares performance, and generates a comparison report.

### How to do it

Create `src/evaluator.py`:

**Metrics compared:**

| Metric | What it measures |
|--------|-----------------|
| **Accuracy** | Overall correct predictions |
| **Precision** | Of all predicted anomalies, how many were actually anomalies |
| **Recall** | Of all actual anomalies, how many were detected |
| **F1-Score** | Harmonic mean of precision and recall |

**Outputs:**
- Comparison table (all models side-by-side)
- Confusion matrices for each model
- ROC curves (where applicable)
- Saved to `results/reports/model_comparison.csv`

**Run:**
```bash
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/evaluator.py
```

---

## 📋 Phase 3 Checklist

- [ ] Data loaded and split (80/20 train/test, stratified)
- [ ] Rule-based baseline implemented and evaluated
- [ ] Isolation Forest trained and evaluated
- [ ] PCA anomaly detector trained and evaluated
- [ ] Decision Tree classifier trained and evaluated
- [ ] Model evaluator created with comparison report
- [ ] All results saved to `results/`
- [ ] Performance comparison table generated

---

## 📊 Expected Results Summary

| Model | Type | Expected Strength |
|-------|------|------------------|
| **Rule-based Baseline** | Heuristic | High recall, lower precision (catches obvious attacks) |
| **Isolation Forest** | Unsupervised | Good at finding unknown/novel anomalies |
| **PCA Detector** | Unsupervised | Good at detecting deviations from normal patterns |
| **Decision Tree** | Supervised | Highest accuracy on known attack patterns |

---

**⬅️ Previous: [Phase 2 — Parsing & Features](./PHASE_2_PARSING_AND_FEATURES.md)**

**➡️ Next: Phase 4 — Evaluation & Visualization *(coming next)***
