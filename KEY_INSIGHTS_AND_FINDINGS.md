# 🔑 Key Insights & Findings

> **Project:** Detection of Abnormal Behavior in Linux Servers Using Machine Learning
>
> **Team:** Aavula Ravi Kumar (22BCE20046) · Manohar Reddy K (22BCE9601) · Rahul Kumar (22BCE7182)
>
> **Date:** March 2026

---

## 1. Model Performance Summary

| Model | Type | Accuracy | Precision | Recall | F1-Score |
|-------|------|----------|-----------|--------|----------|
| Rule-Based Baseline | Heuristic | 0.9951 | 0.9770 | 1.0000 | 0.9884 |
| Isolation Forest | Unsupervised | 0.6951 | 0.2333 | 0.2059 | 0.2188 |
| PCA Anomaly Detector | Unsupervised | 0.7256 | 0.0000 | 0.0000 | 0.0000 |
| **Decision Tree** 🏆 | Supervised | **1.0000** | **1.0000** | **1.0000** | **1.0000** |

**Best model:** Decision Tree classifier (F1 = 1.00)

---

## 2. Why Supervised Models Outperformed Unsupervised

### Decision Tree — Perfect Score (F1 = 1.00)
The Decision Tree achieved perfect classification because it **directly learns from labeled data**. It discovered that a single feature — `breakin_attempts` — perfectly separates normal from abnormal traffic. The learned rule is:

```
IF breakin_attempts > 0 → ABNORMAL
ELSE → NORMAL
```

**Key point for review:** Supervised models excel when you have **well-labeled training data** and want to detect **known attack patterns**. They learn the exact boundaries between normal and malicious behavior.

### Why Isolation Forest Struggled (F1 = 0.22)
Isolation Forest works by **randomly partitioning feature space** — anomalies are isolated in fewer splits. It struggled because:

1. **Synthetic data lacks realistic complexity** — real attacks create subtle, multi-dimensional patterns. Our generated data has clean, well-separated features.
2. **Feature distribution overlap** — normal and abnormal samples overlap significantly in most features, making random isolation ineffective.
3. **Contamination parameter sensitivity** — even with auto-tuned contamination (20.76%), the model couldn't learn meaningful isolation boundaries.

**Key point for review:** Isolation Forest is better suited for **real-world production environments** where anomalies produce genuinely unusual patterns that haven't been seen before.

### Why PCA Detector Failed (F1 = 0.00)
PCA detects anomalies by measuring **reconstruction error** after projecting data to lower dimensions. It failed because:

1. **Anomalies are not structurally different** — in our dataset, "abnormal" means a specific feature exceeds a threshold (e.g., breakin_attempts > 0), not that the overall pattern is fundamentally different.
2. **8 components explain 96% variance** — both normal and abnormal data reconstructs well, producing similar errors.
3. **Threshold too high** — the 95th percentile threshold on training errors didn't capture the subtle differences.

**Key point for review:** PCA works best when anomalies are **rare, structurally different events** — like a sudden spike in an otherwise stable metric. It's less effective for categorical distinctions.

---

## 3. Supervised vs. Unsupervised — When to Use What

| Scenario | Best Approach | Why |
|----------|--------------|-----|
| Known attack patterns (brute force, break-in) | **Supervised** (Decision Tree) | Has labeled examples to learn from |
| Novel/unknown attacks | **Unsupervised** (Isolation Forest) | No labels needed, detects outliers |
| Drift detection (gradual behavior changes) | **Unsupervised** (PCA) | Captures structural deviations |
| Production deployment | **Hybrid** (both) | Supervised catches known threats, unsupervised catches novel ones |

**Our recommendation:** A **hybrid approach** combining supervised models for known threats with unsupervised models for novel, previously unseen attack patterns.

---

## 4. Feature Importance Analysis

The Decision Tree's feature importance reveals what matters most for anomaly detection:

| Rank | Feature | Importance | Interpretation |
|------|---------|-----------|----------------|
| 1 | `breakin_attempts` | 1.0000 | Direct indicator of malicious activity |
| 2 | `failed_login_count` | — | Brute-force SSH attack indicator |
| 3 | `invalid_user_count` | — | Credential stuffing / probing indicator |
| 4 | `fail_to_success_ratio` | — | High ratio = sustained attack |
| 5 | `events_per_minute` | — | Burst frequency detection |

**Key point for review:** Security-specific features (attack counts, failure ratios) are far more discriminative than generic features (hour of day, event frequency). Feature engineering is critical for log-based anomaly detection.

---

## 5. Dataset Characteristics & Limitations

### What We Used
- **2000 synthetic log entries** generated to simulate auth.log patterns
- **70% normal / 30% abnormal** split in raw logs
- **819 feature samples** after time-window aggregation (649 normal, 170 abnormal)
- **15 numerical features** per sample across 1-hour time windows

### Limitations of Synthetic Data

| Limitation | Impact | Mitigation |
|-----------|--------|------------|
| Patterns are well-separated | Inflates supervised model accuracy | Use real production logs for validation |
| No temporal correlation | Misses time-based attack sequences | Add sequence-based features |
| Fixed attack patterns | Doesn't test novel attack detection | Augment with real attack datasets |
| Uniform distribution | Unrealistic event frequency | Collect real /var/log data over weeks |

**Key point for review:** Results on synthetic data demonstrate the **feasibility and methodology**. Real-world deployment requires training on actual production server logs.

---

## 6. System Architecture — What Worked Well

```
Raw Logs → Parser → Feature Extraction → ML Models → Detection
  ↑                                                      |
  └──────── Feedback / Model Retraining ←───────────────┘
```

### Strengths of Our Approach
1. **Modular pipeline** — each stage (parsing, features, models) is independent and replaceable
2. **Docker-based environment** — fully reproducible on any machine
3. **Multiple model comparison** — systematic evaluation of 4 approaches
4. **Time-window features** — captures behavioral patterns, not just individual events
5. **Auto-labeling heuristics** — enables training without manual annotation

### What We'd Improve With More Time
1. Add **sequence-based features** (n-grams of event sequences)
2. Use **real production logs** from an active Linux server
3. Implement a **real-time detection pipeline** with streaming logs
4. Add **alerting system** (email/Slack notifications)
5. Train **Random Forest** and **XGBoost** for ensemble comparison

---

## 7. Practical Applications

This system can be deployed to detect:

| Attack Type | Detection Method | Confidence |
|-------------|-----------------|------------|
| **SSH Brute Force** | High failed_login_count per IP | High ✅ |
| **Credential Stuffing** | Many invalid_user attempts | High ✅ |
| **Break-in Attempts** | Direct breakin_attempt alerts | High ✅ |
| **Privilege Escalation** | Unusual sudo patterns | Medium ⚠️ |
| **Zero-day Exploits** | Isolation Forest (anomaly) | Low-Medium ⚠️ |
| **Data Exfiltration** | Unusual session duration/frequency | Needs extension |

---

## 8. Conclusion

> A lightweight, Docker-based ML system capable of detecting suspicious Linux server behavior
> with **99.5%+ accuracy** using supervised learning. The comparative analysis demonstrates that
> **supervised models (Decision Tree) outperform unsupervised approaches** on labeled log data,
> while unsupervised models retain value for detecting novel, unknown threats in production.

### Key Numbers to Remember

| Metric | Value |
|--------|-------|
| Log entries processed | 2,000 |
| Feature vectors generated | 819 |
| Features per sample | 15 |
| Best model accuracy | **100%** |
| Best model F1-Score | **1.00** |
| False positives (best) | **0** |
| Models compared | 4 |

---

## 9. References

- Liu, F.T., Ting, K.M. and Zhou, Z.H. (2008). *Isolation Forest*. IEEE International Conference on Data Mining.
- Scikit-learn 1.8.0 Documentation — https://scikit-learn.org/
- Ubuntu 24.04 LTS System Logging — `rsyslog`, `auth.log`, `syslog`
- He, S., Zhu, J., He, P. and Lyu, M.R. (2016). *Experience Report: System Log Analysis for Anomaly Detection*. IEEE ISSRE.
