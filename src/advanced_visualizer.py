"""
Advanced Visualizer — Generates publication-quality charts for Phase 4 report.

Charts: ROC curves, precision-recall, feature importance, scenario heatmap,
decision boundary.

Usage:
    docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/advanced_visualizer.py
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_curve, auc, precision_recall_curve,
    average_precision_score, confusion_matrix,
)
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from models.baseline import rule_based_predict

sns.set_style("whitegrid")
plt.rcParams["font.size"] = 11
OUTPUT_DIR = "results/figures"

FEATURE_COLS = [
    "total_events", "failed_login_count", "invalid_user_count",
    "success_login_count", "breakin_attempts", "session_opened_count",
    "sudo_count", "unique_users_attempted", "fail_to_success_ratio",
    "invalid_to_total_ratio", "attack_event_count", "hour_of_day",
    "is_night", "is_weekend", "events_per_minute",
]


def prepare_data(features_path="data/processed/features.csv"):
    """Load and prepare data, train models."""
    df = pd.read_csv(features_path)
    X = df[FEATURE_COLS].values
    y = (df["label"] == "abnormal").astype(int).values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train models
    dt = DecisionTreeClassifier(max_depth=5, min_samples_split=5, min_samples_leaf=3, random_state=42)
    dt.fit(X_train, y_train)

    iso = IsolationForest(n_estimators=100, contamination=y.mean(), random_state=42, n_jobs=-1)
    iso.fit(X_train)

    pca = PCA(n_components=0.95, random_state=42)
    pca.fit(X_train)
    train_errors = np.mean((X_train - pca.inverse_transform(pca.transform(X_train))) ** 2, axis=1)
    pca_threshold = np.percentile(train_errors, 95)

    return df, X_train, X_test, y_train, y_test, scaler, dt, iso, pca, pca_threshold


def plot_roc_curves(X_test, y_test, dt, iso, pca, pca_threshold):
    """Plot ROC curves for all ML models."""
    fig, ax = plt.subplots(figsize=(8, 6))

    # Decision Tree
    dt_proba = dt.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, dt_proba)
    roc_auc = auc(fpr, tpr)
    ax.plot(fpr, tpr, color="#2ecc71", linewidth=2, label=f"Decision Tree (AUC = {roc_auc:.3f})")

    # Isolation Forest — use decision_function as score
    iso_scores = -iso.decision_function(X_test)  # negate so higher = more anomalous
    fpr_iso, tpr_iso, _ = roc_curve(y_test, iso_scores)
    roc_auc_iso = auc(fpr_iso, tpr_iso)
    ax.plot(fpr_iso, tpr_iso, color="#e74c3c", linewidth=2, label=f"Isolation Forest (AUC = {roc_auc_iso:.3f})")

    # PCA — use reconstruction error as score
    pca_errors = np.mean((X_test - pca.inverse_transform(pca.transform(X_test))) ** 2, axis=1)
    fpr_pca, tpr_pca, _ = roc_curve(y_test, pca_errors)
    roc_auc_pca = auc(fpr_pca, tpr_pca)
    ax.plot(fpr_pca, tpr_pca, color="#3498db", linewidth=2, label=f"PCA Detector (AUC = {roc_auc_pca:.3f})")

    # Random baseline
    ax.plot([0, 1], [0, 1], "k--", alpha=0.4, label="Random (AUC = 0.500)")

    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curves — Model Comparison", fontsize=14, fontweight="bold")
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/roc_curves.png", dpi=150)
    print(f"  ✅ Saved: {OUTPUT_DIR}/roc_curves.png")
    plt.close()

    return {"Decision Tree": roc_auc, "Isolation Forest": roc_auc_iso, "PCA Detector": roc_auc_pca}


def plot_precision_recall_curves(X_test, y_test, dt, iso, pca):
    """Plot precision-recall curves."""
    fig, ax = plt.subplots(figsize=(8, 6))

    # Decision Tree
    dt_proba = dt.predict_proba(X_test)[:, 1]
    prec, rec, _ = precision_recall_curve(y_test, dt_proba)
    ap = average_precision_score(y_test, dt_proba)
    ax.plot(rec, prec, color="#2ecc71", linewidth=2, label=f"Decision Tree (AP = {ap:.3f})")

    # Isolation Forest
    iso_scores = -iso.decision_function(X_test)
    prec_iso, rec_iso, _ = precision_recall_curve(y_test, iso_scores)
    ap_iso = average_precision_score(y_test, iso_scores)
    ax.plot(rec_iso, prec_iso, color="#e74c3c", linewidth=2, label=f"Isolation Forest (AP = {ap_iso:.3f})")

    # PCA
    pca_errors = np.mean((X_test - pca.inverse_transform(pca.transform(X_test))) ** 2, axis=1)
    prec_pca, rec_pca, _ = precision_recall_curve(y_test, pca_errors)
    ap_pca = average_precision_score(y_test, pca_errors)
    ax.plot(rec_pca, prec_pca, color="#3498db", linewidth=2, label=f"PCA Detector (AP = {ap_pca:.3f})")

    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Precision-Recall Curves — Model Comparison", fontsize=14, fontweight="bold")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/precision_recall_curves.png", dpi=150)
    print(f"  ✅ Saved: {OUTPUT_DIR}/precision_recall_curves.png")
    plt.close()


def plot_feature_importance(dt):
    """Plot feature importance from Decision Tree."""
    importances = dt.feature_importances_
    indices = np.argsort(importances)[::-1]

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ["#e74c3c" if imp > 0.1 else "#3498db" for imp in importances[indices]]
    ax.barh(
        range(len(FEATURE_COLS)),
        importances[indices],
        color=colors, edgecolor="black", linewidth=0.5
    )
    ax.set_yticks(range(len(FEATURE_COLS)))
    ax.set_yticklabels([FEATURE_COLS[i].replace("_", " ").title() for i in indices])
    ax.set_xlabel("Importance Score")
    ax.set_title("Feature Importance — Decision Tree", fontsize=14, fontweight="bold")
    ax.invert_yaxis()

    # Add values
    for i, v in enumerate(importances[indices]):
        if v > 0.01:
            ax.text(v + 0.005, i, f"{v:.3f}", va="center", fontsize=9)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/feature_importance.png", dpi=150)
    print(f"  ✅ Saved: {OUTPUT_DIR}/feature_importance.png")
    plt.close()


def plot_scenario_heatmap():
    """Heatmap showing model predictions per attack scenario."""
    results_path = "results/reports/scenario_results.csv"
    if not os.path.exists(results_path):
        print(f"  ⚠️ Skipping scenario heatmap — run attack_simulator.py first")
        return

    df = pd.read_csv(results_path)
    model_cols = ["baseline", "isolation_forest", "pca_detector", "decision_tree"]

    # Create correctness matrix: 1=correct, 0=wrong
    matrix = []
    for _, row in df.iterrows():
        row_vals = [1 if row[m] == row["expected"] else 0 for m in model_cols]
        matrix.append(row_vals)

    matrix_df = pd.DataFrame(
        matrix,
        index=df["scenario"],
        columns=["Rule-Based\nBaseline", "Isolation\nForest", "PCA\nDetector", "Decision\nTree"]
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    cmap = sns.color_palette(["#e74c3c", "#2ecc71"])
    sns.heatmap(
        matrix_df, annot=True, fmt="d", cmap=cmap, ax=ax,
        linewidths=1, cbar_kws={"label": "Correct (1) / Wrong (0)"},
        vmin=0, vmax=1,
    )
    ax.set_title("Attack Scenario Results — Per Model", fontsize=14, fontweight="bold")
    ax.set_ylabel("Scenario")

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/scenario_heatmap.png", dpi=150)
    print(f"  ✅ Saved: {OUTPUT_DIR}/scenario_heatmap.png")
    plt.close()


def plot_pca_2d_scatter(X_scaled, y, pca_fitted):
    """2D scatter plot using first 2 PCA components."""
    X_pca = pca_fitted.transform(X_scaled)[:, :2]

    fig, ax = plt.subplots(figsize=(9, 6))
    colors = ["#2ecc71" if label == 0 else "#e74c3c" for label in y]
    scatter = ax.scatter(
        X_pca[:, 0], X_pca[:, 1], c=colors,
        alpha=0.6, edgecolors="black", linewidth=0.3, s=40
    )

    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#2ecc71', markersize=10, label='Normal'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#e74c3c', markersize=10, label='Abnormal'),
    ]
    ax.legend(handles=legend_elements, loc="upper right")

    ax.set_xlabel(f"PC1 ({pca_fitted.explained_variance_ratio_[0]:.1%} variance)")
    ax.set_ylabel(f"PC2 ({pca_fitted.explained_variance_ratio_[1]:.1%} variance)")
    ax.set_title("PCA 2D Projection — Normal vs Abnormal", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/pca_2d_scatter.png", dpi=150)
    print(f"  ✅ Saved: {OUTPUT_DIR}/pca_2d_scatter.png")
    plt.close()


def plot_auc_comparison(auc_scores):
    """Bar chart comparing AUC scores."""
    fig, ax = plt.subplots(figsize=(8, 5))
    models = list(auc_scores.keys())
    scores = list(auc_scores.values())
    colors = ["#2ecc71", "#e74c3c", "#3498db"]

    bars = ax.bar(models, scores, color=colors, edgecolor="black", width=0.5)
    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5, label="Random baseline")

    for bar, score in zip(bars, scores):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f"{score:.3f}", ha="center", fontweight="bold", fontsize=12)

    ax.set_ylabel("AUC Score")
    ax.set_title("AUC-ROC Comparison", fontsize=14, fontweight="bold")
    ax.set_ylim(0, 1.15)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/auc_comparison.png", dpi=150)
    print(f"  ✅ Saved: {OUTPUT_DIR}/auc_comparison.png")
    plt.close()


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"\n{'='*50}")
    print(f"Generating Advanced Visualizations")
    print(f"{'='*50}\n")

    df, X_train, X_test, y_train, y_test, scaler, dt, iso, pca, pca_threshold = prepare_data()
    X_all = scaler.transform(df[FEATURE_COLS].values)
    y_all = (df["label"] == "abnormal").astype(int).values

    # 1. ROC Curves
    auc_scores = plot_roc_curves(X_test, y_test, dt, iso, pca, pca_threshold)

    # 2. Precision-Recall Curves
    plot_precision_recall_curves(X_test, y_test, dt, iso, pca)

    # 3. Feature Importance
    plot_feature_importance(dt)

    # 4. Scenario Heatmap
    plot_scenario_heatmap()

    # 5. PCA 2D Scatter
    plot_pca_2d_scatter(X_all, y_all, pca)

    # 6. AUC Comparison
    plot_auc_comparison(auc_scores)

    print(f"\n{'='*50}")
    print(f"All advanced visualizations saved to {OUTPUT_DIR}/")
    print(f"{'='*50}")
