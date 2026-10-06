"""Plots theoretical vs empirical results for both Dijkstra implementations.

For each experiment and each metric (comparisons, time) it saves:
  * an overlay figure: empirical vs scaled theoretical, (a) matrix and (b) heap
  * a ratio figure: empirical / theoretical for both implementations together
  * a CSV with the plotted numbers

Theory:
  (a) adjacency matrix + array PQ : O(V^2)
  (b) adjacency lists  + heap PQ  : O((V + E) log V)

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
    ("fixed_v_varying_e.csv", "fixed_v_varying_e", "E",
     "Experiment 1: V = 1000, varying E"),
    ("sparse_varying_v.csv", "sparse_varying_v", "V",
     "Experiment 2: sparse graphs (E = 5V), varying V"),
    ("dense_varying_v.csv", "dense_varying_v", "V",
     "Experiment 3: dense graphs (E = V(V-1)/4), varying V"),
]

# (metric suffix in CSV, axis label)
METRICS = [
    ("comparisons", "Number of comparisons"),
    ("time", "Time (seconds)"),
]


def matrix_theory(df):
    return df["V"] ** 2


def heap_theory(df):
    return (df["V"] + df["E"]) * np.log2(df["V"])


# (name, csv column prefix, theory function, theory label, colour)
ALGOS = [
    ("(a) Matrix + array", "matrix", matrix_theory, r"$c \cdot V^2$", "tab:blue"),
    ("(b) Adj. lists + heap", "heap", heap_theory,
     r"$c \cdot (V+E)\log V$", "tab:orange"),
]


def fit_constant(empirical, theory):
    """Geometric mean of empirical/theoretical over the positive points."""
    mask = (empirical > 0) & (theory > 0)
    return float(np.exp(np.mean(np.log(empirical[mask] / theory[mask]))))


def process_experiment(csv_name, out_name, x_col, title):
    path = os.path.join(RESULTS_DIR, csv_name)
    df = pd.read_csv(path).sort_values(x_col).reset_index(drop=True)
    x = df[x_col]

    for metric, ylabel in METRICS:
        out = df[["V", "E"]].copy()
        fig1, axes = plt.subplots(1, 2, figsize=(12, 4.5))
        fig2, ax_ratio = plt.subplots(figsize=(7, 4.5))

        for ax, (name, prefix, theory_fn, theory_label, colour) in zip(axes, ALGOS):
            empirical = df[f"{prefix}_{metric}"]
            theory = theory_fn(df)
            c = fit_constant(empirical, theory)
            scaled = c * theory
            ratio = empirical / scaled

            out[f"{prefix}_empirical"] = empirical
            out[f"{prefix}_theoretical_scaled"] = scaled
            out[f"{prefix}_ratio"] = ratio

            # Overlay: empirical vs scaled theoretical
            ax.plot(x, empirical, "o-", color=colour, label="Empirical")
            ax.plot(x, scaled, "s--", color="black", alpha=0.7,
                    label=f"Theoretical: {theory_label}")
            ax.set_title(name)
            ax.set_xlabel(x_col)
            ax.set_ylabel(ylabel)
            ax.grid(alpha=0.3)
            ax.legend()

            # Ratio: both algorithms together
            ax_ratio.plot(x, ratio, "o-", color=colour, label=name)

        fig1.suptitle(f"{title}\nEmpirical vs theoretical ({metric})")
        fig1.tight_layout()
        fig1.savefig(os.path.join(PLOT_DIR, f"{out_name}_{metric}_overlay.png"), dpi=150)
        plt.close(fig1)

        ax_ratio.axhline(1.0, color="gray", linestyle=":")
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


if __name__ == "__main__":
    os.makedirs(PLOT_DIR, exist_ok=True)
    for csv_name, out_name, x_col, title in EXPERIMENTS:
        print(f"{title}...")
        process_experiment(csv_name, out_name, x_col, title)
    print("Done. Plots and CSVs saved to:", PLOT_DIR)
