# 🎤 Review Presentation Guide

> **Project:** Detection of Abnormal Behavior in Linux Servers Using Machine Learning
>
> **Team:** Aavula Ravi Kumar (22BCE20046) · Manohar Reddy K (22BCE9601) · Rahul Kumar (22BCE7182)

---

## 📅 Review Schedule

| Review | Date | What to Show |
|--------|------|-------------|
| **Review 1** (in 4 days) | ~25 March 2026 | Working pipeline, 4 models, results, future plan |
| **Final Review** (in ~1 month) | ~21 April 2026 | Full research: real data, 8 models, paper, presentation |

---

# 🟢 REVIEW 1 — What to Show (25 March 2026)

## Presentation Flow (15–20 minutes)

### Part 1: Problem Statement (2 min)

**Say this:**
> "Linux servers generate thousands of log entries per minute. Traditional rule-based monitoring cannot detect novel attacks. We built an ML-based system that automatically detects suspicious behavior from server logs."

**Show:**
- The problem statement from `PROJECT_PLAN.md`
- The system architecture diagram

---

### Part 2: Live Demo — Run the Pipeline (5 min)

Open a terminal and run these commands **one by one** while explaining:

```bash
# Step 1: Show the Docker environment
cd ~/Developer/01_active/sdp
docker compose ps
# "We're running Ubuntu 24.04 LTS inside Docker on Mac"

# Step 2: Show the libraries
docker compose exec sdp-ubuntu /opt/venv/bin/python3 -c "import pandas, numpy, sklearn; print('pandas=' + pandas.__version__); print('numpy=' + numpy.__version__); print('sklearn=' + sklearn.__version__)"
# "All ML libraries are installed — Pandas 3.0.1, NumPy 2.4.3, Scikit-learn 1.8.0"

# Step 3: Generate sample logs
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/generate_sample_logs.py
# "We generate 2000 synthetic auth.log entries — 70% normal, 30% attack patterns"

# Step 4: Show raw log data
docker compose exec -w /app sdp-ubuntu head -5 data/raw/sample_auth.log
# "These look exactly like real Linux auth.log entries"

# Step 5: Parse logs
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/log_parser.py
# "Our parser uses 6 regex patterns to extract structured data — 2000/2000 parsed, 0 skipped"

# Step 6: Extract features
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/feature_extractor.py
# "We group logs by IP + 1-hour window and compute 15 features per sample"

# Step 7: Run all models
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/evaluator.py
# "This runs all 4 models and compares them — watch the results..."

# Step 8: Run attack scenarios
docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/attack_simulator.py
# "We simulate 6 realistic attack scenarios and test each model"
```

**Tip:** Run Step 7 (evaluator) while explaining — it takes ~10 seconds and the output is impressive.

---

### Part 3: Show Results (3 min)

**Open these files to show the professor:**

1. **Model comparison table** — `results/reports/model_comparison.csv`
   > "Decision Tree achieved 100% F1, baseline got 99%. Unsupervised models struggled because synthetic data is too clean."

2. **Visualizations** — Open these images from `results/figures/`:
   - `model_comparison.png` — bar chart of all metrics
   - `confusion_matrices.png` — side-by-side confusion matrices
   - `roc_curves.png` — ROC-AUC curves
   - `scenario_heatmap.png` — attack scenario results
   - `decision_tree.png` — the learned tree rules

3. **Attack scenario results** — `results/reports/scenario_results.csv`
   > "Baseline scored 100% on scenarios, Decision Tree missed credential stuffing because it only learned breakin_attempts"

---

### Part 4: Explain Key Insights (3 min)

**Say these points:**

1. > "Supervised models (Decision Tree) excel at detecting **known attack patterns** — they learn exact rules from labeled data."

2. > "Unsupervised models (Isolation Forest, PCA) struggle with our synthetic data but are valuable for detecting **novel, unknown attacks** in real-world production."

3. > "The Rule-Based Baseline achieved 99% F1 — this proves that **well-designed heuristics can be surprisingly effective**, but they can't adapt to new threats."

4. > "We recommend a **hybrid approach**: supervised for known threats + unsupervised for novel threats."

---

### Part 5: Show Future Plan (2 min)

**Open `RESEARCH_UPGRADE_PLAN.md` and say:**

> "We've identified 8 areas for improvement to make this research-grade:"

1. > "Using **real production log datasets** (HDFS from LogHub) instead of only synthetic data"
2. > "Adding **4 more models** — Random Forest, XGBoost, One-Class SVM, MLP Neural Network"
3. > "Implementing **10-fold cross validation** for statistically rigorous results"
4. > "**Hyperparameter tuning** with GridSearchCV"
5. > "Writing a formal **IEEE-format research paper** with literature review"

> "We plan to complete this by the final review."

---

## 📁 Files to Keep Open During Demo

| File | Why |
|------|-----|
| Terminal | For live demo commands |
| `PROJECT_PLAN.md` | Problem statement, architecture, plan |
| `KEY_INSIGHTS_AND_FINDINGS.md` | Key talking points |
| `results/figures/model_comparison.png` | Visual comparison |
| `results/figures/confusion_matrices.png` | Confusion matrices |
| `results/figures/roc_curves.png` | ROC curves |
| `results/figures/scenario_heatmap.png` | Attack scenario results |
| `RESEARCH_UPGRADE_PLAN.md` | Future work plan |

---

## ❓ Expected Questions from Professor & Answers

### Q1: "Why does Decision Tree get 100%?"
> "Because our synthetic labels are based on simple heuristics — the tree learns the same rules. With real-world data, we expect 85–95% accuracy. We've documented this as a limitation and plan to fix it with the HDFS dataset."

### Q2: "Why did PCA fail?"
> "PCA detects anomalies via reconstruction error. In our data, anomalies aren't structurally different — they're defined by specific thresholds (like breakin_attempts > 0), so both normal and abnormal reconstruct similarly. PCA is better suited for detecting unusual patterns in time-series data."

### Q3: "Why not use real server logs?"
> "We started with synthetic data to validate our pipeline and methodology. In Phase 5, we'll use the HDFS dataset from LogHub — 11 million real log lines with human-annotated anomaly labels."

### Q4: "Why Docker instead of a VM?"
> "Docker is lighter, faster to set up, and fully reproducible. Our entire environment can be rebuilt with a single `docker compose build` command. It's also easier to share with team members."

### Q5: "What's the practical use?"
> "This can be deployed as a real-time monitor on any Linux server. It reads auth.log and syslog, extracts features per IP every hour, and flags suspicious IPs — like detecting SSH brute force attacks within minutes instead of hours."

### Q6: "How is this different from existing tools like Fail2Ban?"
> "Fail2Ban uses static rules (e.g., 5 failed logins = ban). Our system uses ML to detect complex patterns — credential stuffing with varied usernames, slow-and-low attacks spread over hours, or novel attack patterns that Fail2Ban's rules would miss."

---

# 🔵 FINAL REVIEW — What to Show (April 2026)

> This is what you should have ready **after implementing Phase 5A/5B/5C:**

| Item | Description |
|------|-------------|
| **Real dataset results** | HDFS data processed with same pipeline |
| **8 models compared** | Original 4 + Random Forest, XGBoost, SVM, MLP |
| **Cross-validation results** | 10-fold CV with mean ± std for each model |
| **Ablation study** | Which features matter |
| **IEEE research paper** | 8–10 page formatted paper |
| **Presentation slides** | 15–20 slide deck |
| **Live demo** | Full pipeline running on real data |

---

## 🏃 Quick Demo Cheat Sheet (Copy-Paste Commands)

```bash
# Start container
cd ~/Developer/01_active/sdp
docker compose up -d

# Full pipeline in 1 command
docker compose exec -w /app sdp-ubuntu bash -c "
  echo '=== 1. GENERATE LOGS ==='
  /opt/venv/bin/python3 src/generate_sample_logs.py
  echo ''
  echo '=== 2. PARSE LOGS ==='
  /opt/venv/bin/python3 src/log_parser.py
  echo ''
  echo '=== 3. EXTRACT FEATURES ==='
  /opt/venv/bin/python3 src/feature_extractor.py
  echo ''
  echo '=== 4. RUN ALL MODELS ==='
  /opt/venv/bin/python3 src/evaluator.py
  echo ''
  echo '=== 5. ATTACK SCENARIOS ==='
  /opt/venv/bin/python3 src/attack_simulator.py
  echo ''
  echo '=== 6. GENERATE VISUALIZATIONS ==='
  /opt/venv/bin/python3 src/advanced_visualizer.py
  echo ''
  echo '✅ FULL PIPELINE COMPLETE'
"
```

---

**Good luck with both reviews! 🚀**
