"""
Visualizer — Creates plots for feature analysis and model results.

Usage:
    docker compose exec sdp-ubuntu /opt/venv/bin/python3 /app/src/visualizer.py
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for Docker
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Configure plot style
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["font.size"] = 12

OUTPUT_DIR = "results/figures"


def plot_label_distribution(df):
    """Plot the distribution of normal vs abnormal labels."""
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["#2ecc71", "#e74c3c"]
    counts = df["label"].value_counts()
    counts.plot(kind="bar", color=colors[:len(counts)], ax=ax, edgecolor="black", width=0.5)
    ax.set_title("Label Distribution (Normal vs Abnormal)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Label")
    ax.set_ylabel("Count")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

    # Add count labels on bars
    for i, (idx, val) in enumerate(counts.items()):
        ax.text(i, val + 0.5, str(val), ha="center", fontweight="bold", fontsize=12)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/label_distribution.png", dpi=150)
    print(f"  ✅ Saved: {OUTPUT_DIR}/label_distribution.png")
    plt.close()


def plot_event_heatmap(df):
    """Heatmap of events per hour of day by label."""
    pivot_data = df.groupby(["hour_of_day", "label"]).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot_data, annot=True, fmt="d", cmap="YlOrRd", ax=ax, linewidths=0.5)
    ax.set_title("Events by Hour of Day × Label", fontsize=14, fontweight="bold")
    ax.set_ylabel("Hour of Day")
    ax.set_xlabel("Label")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/event_heatmap.png", dpi=150)
    print(f"  ✅ Saved: {OUTPUT_DIR}/event_heatmap.png")
    plt.close()


def plot_feature_comparison(df):
    """Box plots comparing key features between normal and abnormal."""
    features_to_plot = [
        "failed_login_count",
        "invalid_user_count",
        "fail_to_success_ratio",
        "unique_users_attempted",
        "events_per_minute",
    ]

    # Filter to only features that exist
    features_to_plot = [f for f in features_to_plot if f in df.columns]

    fig, axes = plt.subplots(1, len(features_to_plot), figsize=(4 * len(features_to_plot), 5))
    if len(features_to_plot) == 1:
        axes = [axes]

    for i, feature in enumerate(features_to_plot):
        sns.boxplot(
            data=df, x="label", y=feature, ax=axes[i],
            palette={"normal": "#2ecc71", "abnormal": "#e74c3c"},
            hue="label", legend=False
        )
        axes[i].set_title(feature.replace("_", " ").title(), fontsize=10)
        axes[i].set_xlabel("")

    plt.suptitle("Feature Comparison: Normal vs Abnormal", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/feature_comparison.png", dpi=150, bbox_inches="tight")
    print(f"  ✅ Saved: {OUTPUT_DIR}/feature_comparison.png")
    plt.close()


def plot_correlation_matrix(df):
    """Correlation matrix of numerical features."""
    numeric_cols = [
        "total_events", "failed_login_count", "invalid_user_count",
        "success_login_count", "breakin_attempts", "session_opened_count",
        "sudo_count", "unique_users_attempted", "fail_to_success_ratio",
        "invalid_to_total_ratio", "attack_event_count", "events_per_minute",
    ]
    # Filter to existing columns
    numeric_cols = [c for c in numeric_cols if c in df.columns]

    corr = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax,
                square=True, linewidths=0.5)
    ax.set_title("Feature Correlation Matrix", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/correlation_matrix.png", dpi=150)
    print(f"  ✅ Saved: {OUTPUT_DIR}/correlation_matrix.png")
    plt.close()


def plot_ip_attack_distribution(df):
    """Bar chart of attack events per source IP."""
    ip_attacks = df.groupby("source_ip")["attack_event_count"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["#e74c3c" if v > ip_attacks.median() else "#3498db" for v in ip_attacks.values]
    ip_attacks.plot(kind="bar", ax=ax, color=colors, edgecolor="black")
    ax.set_title("Attack Events per Source IP", fontsize=14, fontweight="bold")
    ax.set_xlabel("Source IP")
    ax.set_ylabel("Total Attack Events")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

    for i, val in enumerate(ip_attacks.values):
        ax.text(i, val + 0.5, str(int(val)), ha="center", fontsize=10)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/ip_attack_distribution.png", dpi=150)
    print(f"  ✅ Saved: {OUTPUT_DIR}/ip_attack_distribution.png")
    plt.close()


def plot_time_series(df):
    """Time series of events per time window."""
    df_sorted = df.copy()
    df_sorted["time_window"] = pd.to_datetime(df_sorted["time_window"])
    time_grouped = df_sorted.groupby("time_window").agg({
        "total_events": "sum",
        "attack_event_count": "sum",
        "success_login_count": "sum",
    }).reset_index()

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(time_grouped["time_window"], time_grouped["total_events"],
            label="Total Events", color="#3498db", linewidth=1.5)
    ax.plot(time_grouped["time_window"], time_grouped["attack_event_count"],
            label="Attack Events", color="#e74c3c", linewidth=1.5)
    ax.plot(time_grouped["time_window"], time_grouped["success_login_count"],
            label="Successful Logins", color="#2ecc71", linewidth=1.5)
    ax.set_title("Event Timeline", fontsize=14, fontweight="bold")
    ax.set_xlabel("Time")
    ax.set_ylabel("Event Count")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/event_timeline.png", dpi=150)
    print(f"  ✅ Saved: {OUTPUT_DIR}/event_timeline.png")
    plt.close()


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/processed/features.csv"

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(csv_path)

    print(f"\n{'='*50}")
    print(f"Generating Visualizations")
    print(f"{'='*50}")
    print(f"  Data: {csv_path} ({len(df)} samples)\n")

    plot_label_distribution(df)
    plot_event_heatmap(df)
    plot_feature_comparison(df)
    plot_correlation_matrix(df)
    plot_ip_attack_distribution(df)
    plot_time_series(df)

    print(f"\n{'='*50}")
    print(f"All visualizations saved to {OUTPUT_DIR}/")
    print(f"{'='*50}")
