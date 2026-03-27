# 📄 Final Evaluation Report

> **Project:** Detection of Abnormal Behavior in Linux Servers Using Machine Learning
>
> **Generated:** 27 March 2026, 02:26
>
> **Team:** Aavula Ravi Kumar (22BCE20046) · Manohar Reddy K (22BCE9601) · Rahul Kumar (22BCE7182)

---

## 1. Executive Summary

This report presents the evaluation of four anomaly detection models tested against
Linux server log data. The system processed **822 feature samples**
(650 normal, 172 abnormal) generated from 2000 synthetic auth.log entries.

**Best performing model:** Decision Tree (F1-Score: 1.0000)

---

## 2. Dataset Overview

| Metric | Value |
|--------|-------|
| Raw log entries | 2,000 |
| Feature samples | 822 |
| Normal samples | 650 (79.1%) |
| Abnormal samples | 172 (20.9%) |
| Features per sample | 15 |
| Time window | 60 minutes |
| Source IPs | 7 |

---

## 3. Model Performance Comparison

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| Rule-Based Baseline | 0.9927 | 0.9663 | 1.0000 | 0.9829 |
| Isolation Forest | 0.7455 | 0.4146 | 0.4857 | 0.4474 |
| PCA Anomaly Detector | 0.7697 | 0.2000 | 0.0286 | 0.0500 |
| Decision Tree 🏆 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

### Key Findings

1. **Decision Tree** achieved the highest F1-score of 1.0000
2. **Rule-Based Baseline** achieved near-perfect performance (F1=0.99), proving that well-defined heuristics can be highly effective
3. **Unsupervised models** (Isolation Forest, PCA) underperformed because synthetic data lacks the complex patterns that real anomalies produce
4. The **trade-off** between supervised and unsupervised approaches highlights the need for a hybrid detection system

---

## 4. Attack Scenario Analysis

| Scenario | Expected | Baseline | Isolation Forest | PCA | Decision Tree |
|----------|----------|----------|-----------------|-----|---------------|
| Brute Force SSH Attack | abnormal | abnormal ✅ | abnormal ✅ | abnormal ✅ | abnormal ✅ |
| Credential Stuffing | abnormal | abnormal ✅ | abnormal ✅ | abnormal ✅ | normal ❌ |
| Break-in Attempt | abnormal | abnormal ✅ | abnormal ✅ | abnormal ✅ | abnormal ✅ |
| Normal Work Activity | normal | normal ✅ | abnormal ❌ | abnormal ❌ | normal ✅ |
| Night-time Attack | abnormal | abnormal ✅ | abnormal ✅ | abnormal ✅ | abnormal ✅ |
| Privilege Escalation | normal | normal ✅ | abnormal ❌ | abnormal ❌ | normal ✅ |

### Scenario Accuracy

| Model | Correct | Total | Accuracy |
|-------|---------|-------|----------|
| Rule-Based Baseline | 6 | 6 | 100% |
| Isolation Forest | 4 | 6 | 67% |
| PCA Detector | 4 | 6 | 67% |
| Decision Tree | 5 | 6 | 83% |

---

## 5. Visualizations Generated

| Chart | File | Description |
|-------|------|-------------|
| Label Distribution | `label_distribution.png` | Normal vs abnormal bar chart |
| Event Heatmap | `event_heatmap.png` | Events by hour × label |
| Feature Comparison | `feature_comparison.png` | Box plots per label |
| Correlation Matrix | `correlation_matrix.png` | Feature correlations |
| IP Attack Distribution | `ip_attack_distribution.png` | Attacks per source IP |
| Event Timeline | `event_timeline.png` | Time series of events |
| Model Comparison | `model_comparison.png` | Bar chart of all metrics |
| Confusion Matrices | `confusion_matrices.png` | All models side-by-side |
| Decision Tree | `decision_tree.png` | Visual tree structure |
| ROC Curves | `roc_curves.png` | AUC-ROC comparison |
| Precision-Recall | `precision_recall_curves.png` | PR curves for all models |
| Feature Importance | `feature_importance.png` | Decision Tree importances |
| Scenario Heatmap | `scenario_heatmap.png` | Correctness per scenario |
| PCA Scatter | `pca_2d_scatter.png` | 2D projection of data |
| AUC Comparison | `auc_comparison.png` | AUC scores bar chart |

All visualizations are in `results/figures/`.

---

## 6. Recommendations

### For Deployment
1. Use **Decision Tree** for detecting known attack patterns in real time
2. Deploy **Isolation Forest** alongside for detecting novel threats
3. Implement a **feedback loop** for continuous model retraining
4. Set up **alerting** for abnormal detections (email, Slack, PagerDuty)

### For Future Work
1. Train on **real production server logs** (not synthetic)
2. Add **sequence-based features** (n-grams of event sequences)
3. Explore **Random Forest** and **XGBoost** for ensemble learning
4. Implement **real-time streaming** with Apache Kafka or similar
5. Add **more log sources**: nginx, application logs, kernel logs

---

## 7. Conclusion

The project successfully demonstrates that **machine learning can effectively detect
abnormal behavior in Linux server logs**. The supervised Decision Tree classifier achieved
perfect classification on our dataset, while the comparative analysis provides insights into
when supervised vs. unsupervised approaches are most appropriate.

The modular, Docker-based architecture ensures reproducibility and easy deployment
to production environments.

---

*Report generated automatically by `src/report_generator.py`*
