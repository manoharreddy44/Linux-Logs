# 📓 Phase 4 — Implementation Progress Log

> **Project:** Detection of Abnormal Behavior in Linux Servers Using Machine Learning
>
> **Date:** 21 March 2026
>
> **Implemented by:** Rahul Kumar (22BCE7182)

---

## Summary

Phase 4 completed. Attack scenarios tested against all models, advanced visualizations
generated, and final evaluation report produced. The Rule-Based Baseline achieved 100%
scenario accuracy, revealing that for simulated scenarios, heuristic rules can be
highly effective — while unsupervised models flagged more false positives.

---

## Step-by-Step Implementation Log

### Step 1: Attack Scenario Simulation ✅

**File:** `src/attack_simulator.py`

**6 scenarios tested:**

| Scenario | Expected | Baseline | Isolation Forest | PCA | Decision Tree |
|----------|----------|----------|-----------------|-----|---------------|
| Brute Force SSH Attack | abnormal | ✅ | ✅ | ✅ | ✅ |
| Credential Stuffing | abnormal | ✅ | ✅ | ✅ | ❌ |
| Break-in Attempt | abnormal | ✅ | ✅ | ✅ | ✅ |
| Normal Work Activity | normal | ✅ | ❌ | ❌ | ✅ |
| Night-time Attack | abnormal | ✅ | ✅ | ✅ | ✅ |
| Privilege Escalation | normal | ✅ | ❌ | ❌ | ✅ |

**Model accuracy across scenarios:**

| Model | Correct | Total | Accuracy |
|-------|---------|-------|----------|
| **Rule-Based Baseline** | **6** | **6** | **100%** |
| Decision Tree | 5 | 6 | 83% |
| Isolation Forest | 4 | 6 | 67% |
| PCA Detector | 4 | 6 | 67% |

**Key observations:**
- **Decision Tree missed Credential Stuffing** — it only learned `breakin_attempts` as the key feature during training, so it missed attacks without break-in alerts
- **Isolation Forest & PCA had false positives** — they flagged normal work activity and privilege escalation as abnormal because the feature values were outside their learned "normal" boundaries
- **Baseline was perfect** — the hand-crafted rules covered all scenario types

---

### Step 2: Advanced Visualizations ✅

**File:** `src/advanced_visualizer.py`

**6 charts generated:**

| Chart | File | Key Finding |
|-------|------|-------------|
| ROC Curves | `roc_curves.png` | Decision Tree AUC close to 1.0 |
| Precision-Recall Curves | `precision_recall_curves.png` | DT has best average precision |
| Feature Importance | `feature_importance.png` | `breakin_attempts` dominates |
| Scenario Heatmap | `scenario_heatmap.png` | Baseline has most green cells |
| PCA 2D Scatter | `pca_2d_scatter.png` | Normal/abnormal overlap in PCA space |
| AUC Comparison | `auc_comparison.png` | DT > IF > PCA in AUC scores |

**Result:** ✅ No errors — all 6 charts saved to `results/figures/`

---

### Step 3: Final Evaluation Report ✅

**File:** `src/report_generator.py`

**Output:** `results/reports/final_report.md`

**Report sections:**
1. Executive Summary
2. Dataset Overview
3. Model Performance Comparison
4. Attack Scenario Analysis
5. Visualizations Generated (15 charts total)
6. Recommendations
7. Conclusion

**Result:** ✅ No errors — report generated with 7 sections

---

## Errors Summary

| # | Error | Fix |
|---|-------|-----|
| — | None | Phase 4 ran with zero errors |

---

## All Output Files (Phase 4)

| File | Location |
|------|----------|
| Scenario Results CSV | `results/reports/scenario_results.csv` |
| Final Report | `results/reports/final_report.md` |
| ROC Curves | `results/figures/roc_curves.png` |
| Precision-Recall | `results/figures/precision_recall_curves.png` |
| Feature Importance | `results/figures/feature_importance.png` |
| Scenario Heatmap | `results/figures/scenario_heatmap.png` |
| PCA 2D Scatter | `results/figures/pca_2d_scatter.png` |
| AUC Comparison | `results/figures/auc_comparison.png` |

---

## Cumulative Visualization Count

| Phase | Charts | Running Total |
|-------|--------|---------------|
| Phase 2 | 6 | 6 |
| Phase 3 | 3 | 9 |
| Phase 4 | 6 | **15** |

---

## Phase 4 Checklist — COMPLETED ✅

- [x] Attack scenario simulator created and tested (6 scenarios)
- [x] Models evaluated on all 6 attack scenarios
- [x] Advanced visualizations generated (ROC, PR, feature importance, heatmap, PCA scatter, AUC)
- [x] Final evaluation report generated (`results/reports/final_report.md`)
- [x] All results saved to `results/`

---

## Docker Commands Used

```bash
# Run attack scenarios
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/attack_simulator.py

# Generate advanced visualizations
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/advanced_visualizer.py

# Generate final report
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/report_generator.py
```

---

**⬅️ Previous: [Phase 3 — Progress](./PHASE_3_PROGRESS.md)**

**➡️ Next: Phase 5 — Documentation & Presentation**
