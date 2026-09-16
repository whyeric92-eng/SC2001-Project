import csv
import os
import math
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")

# Must match the DATASET_TYPES keys used in run_experiments.py, since the
# CSV filenames are suffixed with these labels.
DATASET_LABELS = ["random", "sorted", "reverse_sorted", "almost_sorted"]

# ---- experiment parameters, mirrored from run_experiments.py so the
# theoretical overlay curves are computed for the same fixed values that
# were actually used when the data was generated. Update these here if
# they ever change over there. ----
C1_S_FIXED = 10
C2_N_FIXED = 200_000
D_N_FIXED = 10_000_000

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


def theoretical_hybrid_comparisons(n, S):
    """Rough average-case comparison count for the hybrid algorithm:
    merge-sort comparisons down to block size S (~ n*log2(n/S)) plus
    insertion-sort comparisons within each block (~S/4 per element on
    average for random data, n/S blocks -> n*S/4 total).

    This is an approximation (constants aren't exact), intended as a
    SHAPE check against the empirical curve, not an exact prediction.
    """
    if S >= n:
        return n * S / 4  # single insertion-sort call, no merging happens
    return n * math.log2(n / S) + n * S / 4


def annotate_bars(ax, values, fmt):
    for i, v in enumerate(values):
        ax.text(i, v, fmt.format(v), ha="center", va="bottom", fontsize=8)
        
# ---------------------------------------------------------------------
# (c)-i: fixed S, varying n  ->  log-log, WITH a fitted c*n*log2(n)
# reference curve overlaid. A bare log-log line can't distinguish
# n*log(n) from e.g. n^1.1 -- the overlay is the actual visual test.
# S is fixed here, so the hybrid is still asymptotically Theta(n log n)
# (the S-dependent terms only affect the constant/lower-order part).
# ---------------------------------------------------------------------
def plot_c1_fixed_S_varying_n(label, S_fixed=CI_S_FIXED):
    data = read_csv(f"c1_fixed_S_varying_n_{label}.csv")
    if not data:
        return
    n_vals, comparisons = data

    scale = comparisons[-1] / (n_vals[-1] * math.log2(n_vals[-1]))
    ref = [scale * n * math.log2(n) for n in n_vals]
    ratio = [e / r for e, r in zip(comparisons, ref)]

    # Top panel: empirical vs theoretical overlay, log-log.
    # Bottom panel: empirical/theoretical ratio, sharing the same x-axis --
    # a flat line at 1.0 is the actual visual confirmation of n*log2(n)
    # growth; a sloped or drifting line (invisible on the log-log panel
    # alone) would reveal a systematic mismatch in growth rate or constant.
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(8, 7), sharex=True,
        gridspec_kw={"height_ratios": [3, 1], "hspace": 0.08},
    )

    ax1.plot(n_vals, comparisons, marker="o", linestyle="-",
              label=f"Empirical (hybrid, S={int(S_fixed)})")
    ax1.plot(n_vals, ref, linestyle="--", color="gray",
              label="c\u00b7n\u00b7log\u2082(n) reference (fitted)")
    ax1.set_ylabel("Number of key comparisons (log scale)")
    ax1.set_title(f"Hybrid Sort: Comparisons vs n, S={int(S_fixed)} fixed [{label}]")
    ax1.set_yscale("log")
    ax1.legend()
    ax1.grid(True, which="both", linestyle="--", alpha=0.5)

    ax2.plot(n_vals, ratio, marker="o", color="black")
    ax2.axhline(1.0, linestyle="--", color="gray")
    ax2.set_xlabel("n (array size, log scale)")
    ax2.set_ylabel("Empirical /\nTheoretical")
    ax2.set_xscale("log")
    ax2.grid(True, which="both", linestyle="--", alpha=0.5)
    
    plt.tight_layout()

    out_path = os.path.join(RESULTS_DIR, f"c1_fixed_S_varying_n_{label}.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved plot to {out_path}")

# ---------------------------------------------------------------------
# (c)-ii: fixed n, varying S over [1, 2000] -> log-x (S spans three
# decades) but LINEAR-y, because the dominant term for large S is
# linear in S (n*S/4), and linear-y shows that true straight-line
# shape instead of a log-y compressing it into a fake "plateau".
# The exact theoretical curve for this n is overlaid for comparison.
# ---------------------------------------------------------------------
def plot_c2_fixed_n_varying_S(label, n_fixed=C2_N_FIXED):
    data = read_csv(f"c2_fixed_n_varying_S_{label}.csv")
    if not data:
        return
    S_vals, comparisons = data

    ref = [theoretical_hybrid_comparisons(n_fixed, S) for S in S_vals]
    ratio = [e / r for e, r in zip(comparisons, ref)]

    # Same overlay + ratio-panel pattern as c1. Here the ratio panel is
    # arguably even more useful: the approximate S^2/4 insertion-sort
    # constant is more likely to drift from the empirical value than the
    # merge-sort n*log2(n) term does, and the ratio panel shows exactly
    # where (small S vs large S) any such drift shows up.
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(8, 7), sharex=True,
        gridspec_kw={"height_ratios": [3, 1], "hspace": 0.08},
    )

    ax1.plot(S_vals, comparisons, marker="o", linestyle="-", color="darkorange",
              label="Empirical")
    ax1.plot(S_vals, ref, linestyle="--", color="gray",
              label="Theory: n\u00b7log\u2082(n/S) + n\u00b7S/4")
    ax1.set_ylabel("Number of key comparisons")
    ax1.set_title(f"Hybrid Sort: Comparisons vs S, n={n_fixed:,} fixed [{label}]")
    ax1.legend()
    ax1.grid(True, which="both", linestyle="--", alpha=0.5)

    ax2.plot(S_vals, ratio, marker="o", color="black")
    ax2.axhline(1.0, linestyle="--", color="gray")
    ax2.set_xlabel("S (threshold, log scale)")
    ax2.set_ylabel("Empirical /\nTheoretical")
    ax2.set_xscale("log")
    ax2.grid(True, which="both", linestyle="--", alpha=0.5)
    
    plt.tight_layout()

    out_path = os.path.join(RESULTS_DIR, f"c2_fixed_n_varying_S_{label}.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved plot to {out_path}")

# ---------------------------------------------------------------------
# (c)-iii: comparison-optimal S per n. Kept for completeness (it's part
# of the required analysis), but explicitly labelled "by comparison
# count", since this is analytically expected to flatten at S=1 for
# every n -- insertion sort's ~S^2/4 comparisons per block are never
# fewer than continuing to merge (~S*log2(S)). The CPU-time-based
# optimum, which actually varies, is in plot_balanced_S_sweep below.
# ---------------------------------------------------------------------
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
    ax1.set_xlabel("n (array size, log scale)")
    ax1.set_ylabel("Comparison-optimal S")
    ax1.set_xscale("log")
    ax1.set_title(f"Optimal S by comparison count vs n [{label}]")
    ax1.grid(True, which="both", linestyle="--", alpha=0.5)

    # Reference curve c*n*log2(n), scaled to match the last data point,
    # to visually check the empirical trend against O(n log n).
    scale = min_comparisons[-1] / (n_vals[-1] * math.log2(n_vals[-1]))
    ref = [scale * n * math.log2(n) for n in n_vals]
    ax2.plot(n_vals, min_comparisons, marker="o", color="crimson", label="Empirical (best S)")
    ax2.plot(n_vals, ref, linestyle="--", color="gray", label="c*n*log2(n) reference")
    ax2.set_xlabel("n (array size)")
    ax2.set_ylabel("Min comparisons (log scale)")
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

# ---------------------------------------------------------------------
# NEW: balanced-S sweep at n=10M. Comparisons and CPU time are plotted
# as "% above the best value on that metric" -- this puts both metrics
# on the SAME normalized y-axis, so the trade-off is directly readable
# without a twin-axis. Linear-x because S only ranges 1..50 here
# (narrow -- log-x would just compress the region we care about).
# This is the plot that actually justifies the S used in part (d).
# ---------------------------------------------------------------------
def plot_balanced_S_sweep(label, n_fixed=D_N_FIXED):
    data = read_csv(f"balanced_S_sweep_10M_{label}.csv", ncols=8)
    if not data:
        return
    (S_vals, comparisons, cpu_times, comp_ratio, time_ratio,
     comp_pct, time_pct, combined_score) = data

    best_idx = min(range(len(S_vals)), key=lambda i: combined_score[i])
    best_S = S_vals[best_idx]

    plt.figure(figsize=(8, 6))
    plt.plot(S_vals, comp_pct, marker="o", color="purple",
             label="Comparisons (% above best)")
    plt.plot(S_vals, time_pct, marker="o", color="teal",
             label="CPU time (% above best)")
    plt.axvline(best_S, linestyle=":", color="black", alpha=0.7)
    ymax = max(max(comp_pct), max(time_pct))
    plt.text(best_S, ymax * 0.92, f"  chosen S={int(best_S)}", fontsize=9)
    plt.xlabel("S (threshold)")
    plt.ylabel("% above best value on that metric (lower is better)")
    plt.title(f"Hybrid Sort: Comparisons vs CPU-Time Trade-off by S, "
              f"n={n_fixed:,} [{label}]")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    out_path = os.path.join(RESULTS_DIR, f"balanced_S_sweep_10M_{label}.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved plot to {out_path}")

# ---------------------------------------------------------------------
# (d): hybrid (at balanced-optimal S) vs plain merge sort, n=10M.
# Linear bar chart -- single-value comparison, log scale adds nothing
# and can visually shrink a real difference.
# ---------------------------------------------------------------------
def plot_d_hybrid_vs_merge(label):
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
    annotate_bars(ax1, comparisons, "{:,.0f}")

    ax2.bar(algos, cpu_times, color=colors)
    ax2.set_ylabel("CPU time (s)")
    ax2.set_title(f"CPU Time @ n=10M [{label}]")
    annotate_bars(ax2, cpu_times, "{:.2f}s")

    plt.tight_layout()
    out_path = os.path.join(RESULTS_DIR, f"d_hybrid_vs_merge_{label}.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved plot to {out_path}")


if __name__ == "__main__":
    os.makedirs(RESULTS_DIR, exist_ok=True)
    # Plot all five charts once per dataset type. Missing files (e.g. a
    # dataset type that wasn't run for a given experiment) are skipped.
    for label in DATASET_LABELS:
        plot_c1_fixed_S_varying_n(label)
        plot_c2_fixed_n_varying_S(label)
        plot_c3_optimal_S_per_n(label)
        plot_d_hybrid_vs_merge(label)
