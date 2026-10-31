"""Plots theoretical vs empirical results of the knapsack algorithms.

Experiments 1 and 2 (theory: n * C), for comparisons (bottom-up DP only)
and time (bottom-up and top-down DP):
  * an overlay figure: empirical vs scaled theoretical, one panel per version
  * a ratio figure: empirical / theoretical for all versions together
  * a CSV with the plotted numbers

Experiment 3 (plain recursion vs DP, small C):
  * one figure, log scale: the time of all three versions, with the
    recursion against its exact number of calls T(C) as its theory

Theory only gives growth rates, so each theoretical curve is multiplied by one
constant c (geometric mean of empirical/theoretical). The ratio
empirical / (c * theoretical) should then stay flat near 1 if the empirical
behaviour matches the predicted complexity.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(HERE, "..", "results")
PLOT_DIR = os.path.join(RESULTS_DIR, "plots")

# (csv file, output name, x-axis column, title)
EXPERIMENTS = [
    ("varying_c.csv", "varying_c", "C", "Experiment 1: n = 10, varying C"),
    ("varying_n.csv", "varying_n", "n", "Experiment 2: C = 10,000, varying n"),
]

# (metric suffix in CSV, axis label, versions measured)
METRICS = [
    ("comparisons", "Number of comparisons", ["bottomup"]),
    ("time", "Time (seconds)", ["bottomup", "topdown"]),
]


def dp_theory(df):
    return df["n"] * df["C"]


# (name, csv column prefix, colour)
ALGOS = [
    ("Bottom-up DP", "bottomup", "tab:blue"),
    ("Top-down DP", "topdown", "tab:orange"),
]


def fit_constant(empirical, theory):
    """Geometric mean of empirical/theoretical over the positive points."""
    mask = (empirical > 0) & (theory > 0)
    return float(np.exp(np.mean(np.log(empirical[mask] / theory[mask]))))


def process_experiment(csv_name, out_name, x_col, title):
    df = pd.read_csv(os.path.join(RESULTS_DIR, csv_name))
    df = df.sort_values(x_col).reset_index(drop=True)
    x = df[x_col]
    theory = dp_theory(df)

    for metric, ylabel, measured in METRICS:
        algos = [a for a in ALGOS if a[1] in measured]
        out = df[["C", "n"]].copy()
        fig1, axes = plt.subplots(1, len(algos), figsize=(6 * len(algos), 4.5),
                                  squeeze=False)
        fig2, ax_ratio = plt.subplots(figsize=(7, 4.5))

        for ax, (name, prefix, colour) in zip(axes[0], algos):
            empirical = df[f"{prefix}_{metric}"]
            c = fit_constant(empirical, theory)
            scaled = c * theory
            ratio = empirical / scaled

            out[f"{prefix}_empirical"] = empirical
            out[f"{prefix}_theoretical_scaled"] = scaled
            out[f"{prefix}_ratio"] = ratio

            # Overlay: empirical vs scaled theoretical
            ax.plot(x, empirical, "o-", color=colour, label="Empirical")
            ax.plot(x, scaled, "s--", color="black", alpha=0.7,
                    label=r"Theoretical: $c \cdot nC$")
            ax.set_title(name)
            ax.set_xlabel(x_col)
            ax.set_ylabel(ylabel)
            ax.grid(alpha=0.3)
            ax.legend()

            # Ratio: all versions together
            ax_ratio.plot(x, ratio, "o-", color=colour, label=name)

        fig1.suptitle(f"{title}\nEmpirical vs theoretical ({metric})")
        fig1.tight_layout()
        fig1.savefig(os.path.join(PLOT_DIR, f"{out_name}_{metric}_overlay.png"), dpi=150)
        plt.close(fig1)

        ax_ratio.axhline(1.0, color="gray", linestyle=":")
        ax_ratio.set_ylim(0, 2)
        ax_ratio.set_title(f"{title}\nEmpirical / theoretical ({metric})")
        ax_ratio.set_xlabel(x_col)
        ax_ratio.set_ylabel("empirical / (c * theoretical)")
        ax_ratio.grid(alpha=0.3)
        ax_ratio.legend()
        fig2.tight_layout()
        fig2.savefig(os.path.join(PLOT_DIR, f"{out_name}_{metric}_ratio.png"), dpi=150)
        plt.close(fig2)

        out.to_csv(os.path.join(PLOT_DIR, f"{out_name}_{metric}_plot_data.csv"),
                   index=False)
        print(f"  saved {out_name} / {metric}")


def process_recursive_vs_dp():
    df = pd.read_csv(os.path.join(RESULTS_DIR, "recursive_vs_dp.csv"))
    df = df.sort_values("C").reset_index(drop=True)
    # C = 0 takes too little time to measure; leave it out of the log plot.
    df = df[df["C"] > 0].reset_index(drop=True)
    x = df["C"]

    rec = df["recursive_time"]
    rec_theory = df["recursive_calls"]
    rec_scaled = fit_constant(rec, rec_theory) * rec_theory

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, rec, "o-", color="tab:red", label="Plain recursion")
    ax.plot(x, rec_scaled, "s--", color="black", alpha=0.7,
            label=r"Theoretical: $c \cdot T(C)$, number of calls")
    ax.plot(x, df["topdown_time"], "o-", color="tab:orange",
            label="Top-down DP")
    ax.plot(x, df["bottomup_time"], "o-", color="tab:blue",
            label="Bottom-up DP")
    ax.set_yscale("log")
    ax.set_title("Experiment 3: objects of part (2) (w = 4, 5, 8)\n"
                 "Plain recursion vs dynamic programming (time, log scale)")
    ax.set_xlabel("C")
    ax.set_ylabel("Time (seconds)")
    ax.grid(alpha=0.3, which="both")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(PLOT_DIR, "recursive_vs_dp_time.png"), dpi=150)
    plt.close(fig)

    out = df[["C", "n", "recursive_calls"]].copy()
    out["recursive_empirical"] = rec
    out["recursive_theoretical_scaled"] = rec_scaled
    out["topdown_empirical"] = df["topdown_time"]
    out["bottomup_empirical"] = df["bottomup_time"]
    out.to_csv(os.path.join(PLOT_DIR, "recursive_vs_dp_time_plot_data.csv"),
               index=False)
    print("  saved recursive_vs_dp / time")


if __name__ == "__main__":
    os.makedirs(PLOT_DIR, exist_ok=True)
    for csv_name, out_name, x_col, title in EXPERIMENTS:
        print(f"{title}...")
        process_experiment(csv_name, out_name, x_col, title)
    print("Experiment 3: plain recursion vs DP...")
    process_recursive_vs_dp()
    print("Done. Plots and CSVs saved to:", PLOT_DIR)
