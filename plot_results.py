import os
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# CONFIG
# =========================
CSV_FILE = "compare_results_fixed.csv"   # change path if needed
OUTPUT_DIR = "figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(CSV_FILE)

# Make labels like "Baseline (6 wires)"
df["method_label"] = df["method"].str.title() + " (" + df["n_wires"].astype(str) + " wires)"

# Fixed order for plotting
order = [
    "Baseline (6 wires)",
    "Coevolution (6 wires)",
    "Baseline (8 wires)",
    "Coevolution (8 wires)",
]

# =========================
# GRAPH 1: Success rate
# =========================
success = (
    df.groupby(["method", "n_wires"])["found_valid"]
    .mean()
    .reset_index()
)
success["success_rate"] = success["found_valid"] * 100
success["method_label"] = success["method"].str.title() + " (" + success["n_wires"].astype(str) + " wires)"
success = success.set_index("method_label").loc[order].reset_index()

plt.figure(figsize=(8, 5))
plt.bar(success["method_label"], success["success_rate"])
plt.ylabel("Success rate (%)")
plt.title("Success Rate by Method and Problem Size")
plt.ylim(0, 110)

for i, v in enumerate(success["success_rate"]):
    plt.text(i, v + 2, f"{v:.1f}%", ha="center")

plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "graph1_success_rate.png"), dpi=300)
plt.show()

# =========================
# GRAPH 2: Generation first found perfect
# Uses only successful runs
# =========================
gen_df = df[df["generation_found"].notna()].copy()
gen_df["method_label"] = gen_df["method"].str.title() + " (" + gen_df["n_wires"].astype(str) + " wires)"

# mean + std for error bars
gen_summary = (
    gen_df.groupby("method_label")["generation_found"]
    .agg(["mean", "std"])
    .reindex(order)
    .reset_index()
)

plt.figure(figsize=(8, 5))
plt.bar(
    gen_summary["method_label"],
    gen_summary["mean"],
    yerr=gen_summary["std"],
    capsize=5
)
plt.ylabel("Generation first found perfect")
plt.title("Mean Generation to First Perfect Network")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "graph2_generation_found.png"), dpi=300)
plt.show()

# Optional boxplot version instead of mean+std
plt.figure(figsize=(8, 5))
gen_data = [gen_df[gen_df["method_label"] == label]["generation_found"] for label in order]
plt.boxplot(gen_data, labels=order)
plt.ylabel("Generation first found perfect")
plt.title("Distribution of Generation to First Perfect Network")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "graph2_generation_found_boxplot.png"), dpi=300)
plt.show()

# =========================
# GRAPH 3: Final length
# =========================
length_summary = (
    df.groupby("method_label")["best_length"]
    .agg(["mean", "std"])
    .reindex(order)
    .reset_index()
)

plt.figure(figsize=(8, 5))
plt.bar(
    length_summary["method_label"],
    length_summary["mean"],
    yerr=length_summary["std"],
    capsize=5
)
plt.ylabel("Best network length")
plt.title("Mean Best Network Length by Method")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "graph3_best_length.png"), dpi=300)
plt.show()

# Optional boxplot for final length
plt.figure(figsize=(8, 5))
length_data = [df[df["method_label"] == label]["best_length"] for label in order]
plt.boxplot(length_data, labels=order)
plt.ylabel("Best network length")
plt.title("Distribution of Best Network Length")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "graph3_best_length_boxplot.png"), dpi=300)
plt.show()

# =========================
# OPTIONAL GRAPH 4: Runtime
# =========================
runtime_summary = (
    df.groupby("method_label")["time_seconds"]
    .agg(["mean", "std"])
    .reindex(order)
    .reset_index()
)

plt.figure(figsize=(8, 5))
plt.bar(
    runtime_summary["method_label"],
    runtime_summary["mean"],
    yerr=runtime_summary["std"],
    capsize=5
)
plt.ylabel("Runtime (seconds)")
plt.title("Mean Runtime by Method")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "graph4_runtime.png"), dpi=300)
plt.show()