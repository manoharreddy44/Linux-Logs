# 📊 Phase 4 — Evaluation, Visualization & Final Report

> **Goal:** Conduct thorough evaluation of all models under different scenarios, create advanced visualizations, and produce a final evaluation report.
>
> **Duration:** Week 8–9
>
> **Prerequisites:** [Phase 3](./PHASE_3_MODEL_DEVELOPMENT.md) completed — all 4 models trained and baseline metrics available.

---

## Step 1: Simulate Attack Scenarios

### What to do
Test all models against specific, realistic attack scenarios to understand their behavior under different threat types.

### How to do it

Create `src/attack_simulator.py`:

**Simulated scenarios:**

| Scenario | Description | Expected Pattern |
|----------|-------------|-----------------|
| **Brute Force** | 50+ failed logins from one IP in 1 hour | High failed_login_count, high fail_to_success_ratio |
| **Credential Stuffing** | 20+ invalid username attempts from one IP | High invalid_user_count, many unique_users |
| **Break-in Attempt** | Direct break-in alerts + failed logins | High breakin_attempts |
| **Normal Burst** | Many successful logins during work hours | High success_login_count, low attack events |
| **Night Attack** | Failed logins during 1–5 AM | High failed count + is_night=1 |

**Run:**
```bash
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/attack_simulator.py
```

---

## Step 2: Generate Advanced Visualizations

### What to do
Create publication-quality charts for the evaluation report.

### Charts to generate

| Chart | Purpose |
|-------|---------|
| ROC Curves | Visualize trade-off between true/false positive rates |
| Precision-Recall Curves | Important for imbalanced datasets |
| Feature Importance Bar Chart | Which features matter most |
| Attack Scenario Heatmap | Model accuracy per attack type |
| Decision Boundary Plot | 2D visualization of classification regions |

**Run:**
```bash
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/advanced_visualizer.py
```

---

## Step 3: Generate Final Evaluation Report

### What to do
Create a comprehensive evaluation report summarizing all findings — model performance, scenario analysis, recommendations.

**Run:**
```bash
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/report_generator.py
```

---

## 📋 Phase 4 Checklist

- [ ] Attack scenario simulator created and tested
- [ ] Models evaluated on all 5 attack scenarios
- [ ] Advanced visualizations generated (ROC, PR curves, heatmaps)
- [ ] Final evaluation report generated
- [ ] All results saved to `results/`

---

**⬅️ Previous: [Phase 3 — Model Development](./PHASE_3_MODEL_DEVELOPMENT.md)**

**➡️ Next: Phase 5 — Documentation & Presentation *(coming next)***
