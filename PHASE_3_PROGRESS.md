# 📓 Phase 3 — Implementation Progress Log

> **Project:** Detection of Abnormal Behavior in Linux Servers Using Machine Learning
>
> **Date:** 21 March 2026
>
> **Implemented by:** Rahul Kumar (22BCE7182)

---

## Summary

Phase 3 has been completed. Four models were implemented, trained, and evaluated:
- **Decision Tree** achieved perfect F1=1.00 (best model)
- **Rule-Based Baseline** achieved F1=0.99 (strong heuristic)
- **Isolation Forest** achieved F1=0.22 (unsupervised — struggles with synthetic data)
- **PCA Detector** achieved F1=0.00 (reconstruction error not discriminative for this dataset)

---

## Step-by-Step Implementation Log

### Step 1: Verify Data is Ready ✅

**Command:**
```bash
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 -c "
import pandas as pd
df = pd.read_csv('data/processed/features.csv')
print(f'Total samples: {len(df)}')
print(f'Labels: {df[\"label\"].value_counts().to_dict()}')
"
```

**Result:**
```
Total samples: 819
Labels: {'normal': 649, 'abnormal': 170}
```

Normal-to-abnormal ratio: **79.2% / 20.8%**

---

### Step 2: Rule-Based Baseline ✅

**File:** `src/models/baseline.py`

**Rules implemented:**
1. `breakin_attempts > 0` → abnormal
2. `failed_login_count > 3` → abnormal
3. `invalid_user_count > 2` → abnormal
4. `fail_to_success_ratio > 2.0` → abnormal
5. `attack_event_count > 3` → abnormal

**Results:**

| Metric | Score |
|--------|-------|
| **Accuracy** | 0.9951 |
| **Precision** | 0.9770 |
| **Recall** | 1.0000 |
| **F1-Score** | 0.9884 |

**Confusion Matrix:**
```
TN=645  FP=4
FN=0    TP=170
```

**Analysis:** Excellent baseline — catches 100% of anomalies (perfect recall) with only 4 false positives. This is because the labeling heuristics in the feature extractor are similar to the baseline rules.

---

### Step 3: Isolation Forest ✅

**File:** `src/models/isolation_forest.py`

**Configuration:**
- `n_estimators=100`
- `contamination=0.2076` (auto-calculated from data)
- `random_state=42`

**Results:**

| Metric | Score |
|--------|-------|
| **Accuracy** | 0.6951 |
| **Precision** | 0.2333 |
| **Recall** | 0.2059 |
| **F1-Score** | 0.2188 |

**Confusion Matrix:**
```
TN=107  FP=23
FN=27   TP=7
```

**Analysis:** Poor performance on this dataset. Isolation Forest is designed for detecting truly unusual patterns in high-dimensional data. With synthetic, evenly-distributed data, it struggles to find meaningful isolation boundaries. Would perform better with real-world log data containing genuine anomalous patterns.

---

### Step 4: PCA Anomaly Detector ✅

**File:** `src/models/pca_detector.py`

**Configuration:**
- `n_components=0.95` → selected **8 components** (explains 95.96% variance)
- Threshold set at 95th percentile of training reconstruction errors

**Results:**

| Metric | Score |
|--------|-------|
| **Accuracy** | 0.7256 |
| **Precision** | 0.0000 |
| **Recall** | 0.0000 |
| **F1-Score** | 0.0000 |

**Confusion Matrix:**
```
TN=119  FP=11
FN=34   TP=0
```

**Analysis:** PCA detected zero true anomalies. This is because anomalies in our dataset are not structurally different from normal data in terms of reconstruction error — they're defined by specific feature thresholds (e.g., breakin_attempts > 0), not by being fundamentally different in feature space. PCA works better when anomalies produce genuinely unusual feature combinations.

---

### Step 5: Decision Tree Classifier ✅

**File:** `src/models/decision_tree.py`

**Configuration:**
- `max_depth=5`
- `min_samples_split=5`
- `min_samples_leaf=3`
- `random_state=42`

**Results:**

| Metric | Score |
|--------|-------|
| **Accuracy** | 1.0000 |
| **Precision** | 1.0000 |
| **Recall** | 1.0000 |
| **F1-Score** | 1.0000 |

**Confusion Matrix:**
```
TN=130  FP=0
FN=0    TP=34
```

**Top Feature Importances:**

| Feature | Importance |
|---------|-----------|
| breakin_attempts | 1.0000 |
| All others | 0.0000 |

**Decision Tree Rule (learned):**
```
IF breakin_attempts > 0.47 → abnormal
ELSE → normal
```

**Analysis:** Perfect classification. The Decision Tree learned that `breakin_attempts` is the single most discriminative feature. This makes sense because in our labeling heuristic, any break-in attempt is always labeled abnormal. With real-world data, the tree would learn more complex multi-feature rules.

---

### Step 6: Model Comparison ✅

**Command:**
```bash
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/evaluator.py
```

**Result:** ✅ No errors

**Comparison Table:**

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| **Rule-Based Baseline** | 0.9951 | 0.9770 | 1.0000 | 0.9884 |
| **Isolation Forest** | 0.6951 | 0.2333 | 0.2059 | 0.2188 |
| **PCA Anomaly Detector** | 0.7256 | 0.0000 | 0.0000 | 0.0000 |
| **Decision Tree** | **1.0000** | **1.0000** | **1.0000** | **1.0000** |

**🏆 Best Model:** Decision Tree (F1-Score: 1.0000)

---

## Errors Summary

| # | Error | Fix |
|---|-------|-----|
| — | None | Phase 3 ran with zero errors |

---

## Output Files

| File | Location | Description |
|------|----------|-------------|
| Model Comparison CSV | `results/reports/model_comparison.csv` | Metrics for all 4 models |
| Confusion Matrices | `results/figures/confusion_matrices.png` | Side-by-side comparison |
| Metric Comparison | `results/figures/model_comparison.png` | Bar chart of all metrics |
| Decision Tree Plot | `results/figures/decision_tree.png` | Visual tree structure |
| Isolation Forest Model | `results/models/isolation_forest.joblib` | Saved model |
| PCA Model | `results/models/pca_detector.joblib` | Saved model |
| Decision Tree Model | `results/models/decision_tree.joblib` | Saved model |
| Scaler | `results/models/scaler.joblib` | Feature scaler |

---

## Key Takeaways

1. **Supervised models outperform unsupervised** on this labeled dataset — Decision Tree achieves perfect classification.
2. **Rule-based baseline is surprisingly strong** because the labeling heuristics are well-defined.
3. **Unsupervised models (Isolation Forest, PCA)** struggle because the synthetic data doesn't have the complex, subtle patterns that real-world anomalies would exhibit.
4. **For production use:** a hybrid approach combining supervised (for known threats) and unsupervised (for novel threats) would be ideal.
5. **Feature importance** confirms that `breakin_attempts` is the most discriminative feature for this dataset.

---

## Docker Commands Used

```bash
# Run individual models
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/models/baseline.py
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/models/isolation_forest.py
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/models/pca_detector.py
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/models/decision_tree.py

# Run all models with comparison
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/evaluator.py
```

---

## Phase 3 Checklist — COMPLETED ✅

- [x] Data loaded and verified (819 samples, 649 normal, 170 abnormal)
- [x] Rule-based baseline implemented → F1=0.9884
- [x] Isolation Forest trained → F1=0.2188
- [x] PCA anomaly detector trained → F1=0.0000
- [x] Decision Tree classifier trained → F1=1.0000 (🏆 best)
- [x] Model evaluator created with comparison report
- [x] All results saved (models, figures, reports)
- [x] Confusion matrices and comparison chart generated

---

**⬅️ Previous: [Phase 2 — Progress](./PHASE_2_PROGRESS.md)**

**➡️ Next: Phase 4 — Final Evaluation & Report *(coming next)***
