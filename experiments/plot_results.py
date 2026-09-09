import csv
import os
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def read_csv(filename):
    path = os.path.join(RESULTS_DIR, filename)
    xs, ys = [], []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            xs.append(float(row[0]))
            ys.append(float(row[1]))
    return xs, ys


def plot_c1_fixed_S_varying_n():
    n_vals, comparisons = read_csv("c1_fixed_S_varying_n.csv")

    plt.figure(figsize=(8, 6))
    plt.plot(n_vals, comparisons, marker="o", linestyle="-")
    plt.xlabel("n (array size)")
    plt.ylabel("Number of comparisons")
    plt.title("Hybrid Sort: Comparisons vs n (S fixed)")
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.tight_layout()

    out_path = os.path.join(RESULTS_DIR, "c1_fixed_S_varying_n.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved plot to {out_path}")


def plot_c2_fixed_n_varying_S():
    S_vals, comparisons = read_csv("c2_fixed_n_varying_S.csv")

    plt.figure(figsize=(8, 6))
    plt.plot(S_vals, comparisons, marker="o", linestyle="-", color="darkorange")
    plt.xlabel("S (threshold)")
    plt.ylabel("Number of comparisons")
    plt.title("Hybrid Sort: Comparisons vs S (n fixed)")
    plt.xscale("log")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.tight_layout()

    out_path = os.path.join(RESULTS_DIR, "c2_fixed_n_varying_S.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved plot to {out_path}")


if __name__ == "__main__":
    os.makedirs(RESULTS_DIR, exist_ok=True)
    plot_c1_fixed_S_varying_n()
    plot_c2_fixed_n_varying_S()
