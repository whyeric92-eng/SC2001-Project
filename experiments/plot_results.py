import csv
import os
import math
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")

# Must match the DATASET_TYPES keys used in run_experiments.py, since the
# CSV filenames are suffixed with these labels.
DATASET_LABELS = ["random", "sorted", "reverse_sorted", "almost_sorted"]


def read_csv(filename, ncols=2):
    """Read a CSV with a header row, returning `ncols` parallel float lists.
    Returns None if the file doesn't exist (so a missing dataset/label
    combination is skipped instead of crashing the whole run)."""
    path = os.path.join(RESULTS_DIR, filename)
    if not os.path.exists(path):
        print(f"  [skip] {filename} not found")
        return None
    cols = [[] for _ in range(ncols)]
    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            for i in range(ncols):
                cols[i].append(float(row[i]))
    return cols


def plot_c1_fixed_S_varying_n(label):
    data = read_csv(f"c1_fixed_S_varying_n_{label}.csv")
    if not data:
        return
    n_vals, comparisons = data

    plt.figure(figsize=(8, 6))
    plt.plot(n_vals, comparisons, marker="o", linestyle="-")
    plt.xlabel("n (array size)")
    plt.ylabel("Number of comparisons")
    plt.title(f"Hybrid Sort: Comparisons vs n (S fixed) [{label}]")
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.tight_layout()

    out_path = os.path.join(RESULTS_DIR, f"c1_fixed_S_varying_n_{label}.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved plot to {out_path}")


def plot_c2_fixed_n_varying_S(label):
    data = read_csv(f"c2_fixed_n_varying_S_{label}.csv")
    if not data:
        return
    S_vals, comparisons = data

    plt.figure(figsize=(8, 6))
    plt.plot(S_vals, comparisons, marker="o", linestyle="-", color="darkorange")
    plt.xlabel("S (threshold)")
    plt.ylabel("Number of comparisons")
    plt.title(f"Hybrid Sort: Comparisons vs S (n fixed) [{label}]")
    plt.xscale("log")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.tight_layout()

    out_path = os.path.join(RESULTS_DIR, f"c2_fixed_n_varying_S_{label}.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved plot to {out_path}")


def plot_c3_optimal_S_per_n(label):
    """(c)-iii: for each n, show the best S found and the comparisons it
    achieves. Two panels sharing the n-axis: best_S vs n, and
    min_comparisons vs n (with an n*log2(n) reference curve so the shape
    can be checked against theory)."""
    data = read_csv(f"c3_optimal_S_per_n_{label}.csv", ncols=3)
    if not data:
        return
    n_vals, best_S, min_comparisons = data

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(n_vals, best_S, marker="o", color="green")
    ax1.set_xlabel("n (array size)")
    ax1.set_ylabel("Optimal S")
    ax1.set_xscale("log")
    ax1.set_title(f"Optimal S vs n [{label}]")
    ax1.grid(True, which="both", linestyle="--", alpha=0.5)

    ax2.plot(n_vals, min_comparisons, marker="o", color="crimson", label="Empirical (best S)")
    # Reference curve c*n*log2(n), scaled to match the last data point,
    # to visually check the empirical trend against O(n log n).
    scale = min_comparisons[-1] / (n_vals[-1] * math.log2(n_vals[-1]))
    ref = [scale * n * math.log2(n) for n in n_vals]
    ax2.plot(n_vals, ref, linestyle="--", color="gray", label="c*n*log2(n) reference")
    ax2.set_xlabel("n (array size)")
    ax2.set_ylabel("Min comparisons")
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_title(f"Comparisons at Optimal S vs n [{label}]")
    ax2.legend()
    ax2.grid(True, which="both", linestyle="--", alpha=0.5)

    plt.tight_layout()
    out_path = os.path.join(RESULTS_DIR, f"c3_optimal_S_per_n_{label}.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved plot to {out_path}")


def plot_d_hybrid_vs_merge(label):
    """(d): bar chart comparing Hybrid Sort (at optimal S) vs plain Merge
    Sort on the n=10,000,000 dataset, for both comparisons and CPU time."""
    path = os.path.join(RESULTS_DIR, f"d_hybrid_vs_merge_{label}.csv")
    if not os.path.exists(path):
        print(f"  [skip] d_hybrid_vs_merge_{label}.csv not found")
        return
    rows = {}
    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for algo, comparisons, cpu_time in reader:
            rows[algo] = (float(comparisons), float(cpu_time))

    algos = list(rows.keys())
    comparisons = [rows[a][0] for a in algos]
    cpu_times = [rows[a][1] for a in algos]
    colors = ["darkorange" if a == "hybrid" else "steelblue" for a in algos]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    ax1.bar(algos, comparisons, color=colors)
    ax1.set_ylabel("Number of comparisons")
    ax1.set_title(f"Comparisons @ n=10M [{label}]")
    for i, v in enumerate(comparisons):
        ax1.text(i, v, f"{v:,.0f}", ha="center", va="bottom", fontsize=8)

    ax2.bar(algos, cpu_times, color=colors)
    ax2.set_ylabel("CPU time (s)")
    ax2.set_title(f"CPU Time @ n=10M [{label}]")
    for i, v in enumerate(cpu_times):
        ax2.text(i, v, f"{v:.2f}s", ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    out_path = os.path.join(RESULTS_DIR, f"d_hybrid_vs_merge_{label}.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved plot to {out_path}")


if __name__ == "__main__":
    os.makedirs(RESULTS_DIR, exist_ok=True)
    # Plot all four charts once per dataset type. Missing files (e.g. a
    # dataset type that wasn't run for a given experiment) are skipped.
    for label in DATASET_LABELS:
        plot_c1_fixed_S_varying_n(label)
        plot_c2_fixed_n_varying_S(label)
        plot_c3_optimal_S_per_n(label)
        plot_d_hybrid_vs_merge(label)