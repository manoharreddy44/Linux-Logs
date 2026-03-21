"""
Model Evaluator — Runs all models and generates a comparative report.

Usage:
    docker compose exec -w /app sdp-ubuntu /opt/venv/bin/python3 src/evaluator.py
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score,
    precision_score, recall_score, f1_score,
)
import os
import sys

# Add parent to path
sys.path.insert(0, os.path.dirname(__file__))

from models.baseline import run_baseline
from models.isolation_forest import run_isolation_forest
from models.pca_detector import run_pca_detector
from models.decision_tree import run_decision_tree


def plot_confusion_matrices(results_list, output_path):
    """Plot confusion matrices for all models side by side."""
    n_models = len(results_list)
    fig, axes = plt.subplots(1, n_models, figsize=(5 * n_models, 4))

    if n_models == 1:
        axes = [axes]

    for i, result in enumerate(results_list):
        cm = confusion_matrix(result["y_true"], result["y_pred"])
        sns.heatmap(
            cm, annot=True, fmt="d", cmap="Blues", ax=axes[i],
            xticklabels=["Normal", "Abnormal"],
            yticklabels=["Normal", "Abnormal"],
        )
        axes[i].set_title(result["model"], fontsize=11, fontweight="bold")
        axes[i].set_xlabel("Predicted")
        axes[i].set_ylabel("Actual")

    plt.suptitle("Confusion Matrices — All Models", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"  ✅ Saved: {output_path}")
    plt.close()


def plot_metric_comparison(comparison_df, output_path):
    """Bar chart comparing all models across metrics."""
    metrics = ["accuracy", "precision", "recall", "f1_score"]
    models = comparison_df["model"].values

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(models))
    width = 0.2

    colors = ["#3498db", "#2ecc71", "#e74c3c", "#f39c12"]

    for i, metric in enumerate(metrics):
        values = comparison_df[metric].values
        bars = ax.bar(x + i * width, values, width, label=metric.replace("_", " ").title(),
                      color=colors[i], edgecolor="black", linewidth=0.5)
        # Add value labels
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f"{val:.2f}", ha="center", va="bottom", fontsize=8)

    ax.set_xlabel("Model")
    ax.set_ylabel("Score")
    ax.set_title("Model Performance Comparison", fontsize=14, fontweight="bold")
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(models, rotation=15, ha="right")
    ax.set_ylim(0, 1.15)
    ax.legend(loc="upper left")
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"  ✅ Saved: {output_path}")
    plt.close()


def run_all_models():
    """Run all models and generate comparison report."""

    print(f"\n{'='*60}")
    print(f"RUNNING ALL MODELS")
    print(f"{'='*60}")

    results_list = []

    # 1. Rule-Based Baseline
    print(f"\n{'─'*40}")
    print(f"[1/4] Rule-Based Baseline")
    print(f"{'─'*40}")
    results_list.append(run_baseline())

    # 2. Isolation Forest
    print(f"\n{'─'*40}")
    print(f"[2/4] Isolation Forest")
    print(f"{'─'*40}")
    results_list.append(run_isolation_forest())

    # 3. PCA Anomaly Detector
    print(f"\n{'─'*40}")
    print(f"[3/4] PCA Anomaly Detector")
    print(f"{'─'*40}")
    results_list.append(run_pca_detector())

    # 4. Decision Tree
    print(f"\n{'─'*40}")
    print(f"[4/4] Decision Tree Classifier")
    print(f"{'─'*40}")
    results_list.append(run_decision_tree())

    # Build comparison table
    print(f"\n\n{'='*60}")
    print(f"MODEL COMPARISON SUMMARY")
    print(f"{'='*60}\n")

    comparison_data = []
    for result in results_list:
        y_true = result["y_true"]
        y_pred = result["y_pred"]

        comparison_data.append({
            "model": result["model"],
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1_score": f1_score(y_true, y_pred, zero_division=0),
        })

    comparison_df = pd.DataFrame(comparison_data)

    # Print comparison table
    print(comparison_df.to_string(index=False, float_format="%.4f"))

    # Find best model
    best_idx = comparison_df["f1_score"].idxmax()
    best_model = comparison_df.loc[best_idx, "model"]
    best_f1 = comparison_df.loc[best_idx, "f1_score"]
    print(f"\n🏆 Best Model (by F1-Score): {best_model} ({best_f1:.4f})")

    # Save comparison CSV
    os.makedirs("results/reports", exist_ok=True)
    comparison_df.to_csv("results/reports/model_comparison.csv", index=False)
    print(f"\n  ✅ Saved: results/reports/model_comparison.csv")

    # Generate plots
    os.makedirs("results/figures", exist_ok=True)
    plot_confusion_matrices(results_list, "results/figures/confusion_matrices.png")
    plot_metric_comparison(comparison_df, "results/figures/model_comparison.png")

    print(f"\n{'='*60}")
    print(f"ALL MODELS EVALUATED SUCCESSFULLY")
    print(f"{'='*60}")

    return comparison_df, results_list


if __name__ == "__main__":
    run_all_models()
