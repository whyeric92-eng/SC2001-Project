import csv, time, sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sorting"))
sys.path.insert(0, os.path.dirname(__file__))

import counter
from hybrid_sort import hybrid_sort
from merge_sort import merge_sort
from generate_data import (
    generate_data, generate_sorted, generate_reverse_sorted,
    generate_almost_sorted, SIZES, X,
)

SEED = 42
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")

# Maps a human-readable label to the generator function that should be used
# to build the dataset for that label. Add/remove entries here to control
# which dataset types get run.
DATASET_TYPES = {
    "random": generate_data,
    "sorted": generate_sorted,
    "reverse_sorted": generate_reverse_sorted,
    "almost_sorted": generate_almost_sorted,
}


# NOTE: every experiment_* function below calls generate_data(...) directly.
# They are UNCHANGED from the original version. Instead of editing each one
# to accept a "which generator" argument, the __main__ block at the bottom
# reassigns the *global* name `generate_data` to point at a different
# function before each dataset-type pass. Because Python looks up global
# names at call time (not when the function was defined), every
# experiment_* function automatically picks up whichever generator
# `generate_data` currently points to -- no per-function edits needed.

def experiment_c1(S_fixed):
    results = []
    for n in SIZES:
        arr = generate_data(n, X, seed=SEED)
        counter.reset_counter()
        hybrid_sort(arr, S_fixed)
        results.append((n, counter.comparisons))
    return results


def experiment_c2(n_fixed, S_values):
    base_data = generate_data(n_fixed, X, seed=SEED)
    results = []
    for S in S_values:
        arr = base_data.copy()
        counter.reset_counter()
        hybrid_sort(arr, S)
        results.append((S, counter.comparisons))
    return results


def experiment_c3(n_values, S_values):
    results = []
    for n in n_values:
        min_comparisons = float('inf')
        best_S = 0
        temps = experiment_c2(n, S_values)
        for temp in temps:
            if temp[1] < min_comparisons:
                min_comparisons = temp[1]
                best_S = temp[0]
        results.append((n, best_S, min_comparisons))
    return results


def experiment_d(n, optimal_S, repeats=3):
    base_data = generate_data(n, X, seed=SEED)

    hybrid_times = []
    for _ in range(repeats):
        arr1 = base_data.copy()
        counter.reset_counter()
        start = time.process_time()
        hybrid_sort(arr1, optimal_S)
        hybrid_times.append(time.process_time() - start)
    hybrid_comparisons = counter.comparisons

    merge_times = []
    for _ in range(repeats):
        arr2 = base_data.copy()
        counter.reset_counter()
        start = time.process_time()
        merge_sort(arr2)
        merge_times.append(time.process_time() - start)
    merge_comparisons = counter.comparisons

    return {
        "hybrid": (hybrid_comparisons, min(hybrid_times)),
        "merge": (merge_comparisons, min(merge_times)),
    }


def experiment_time_sweep(n, S_values, repeats=1):
    base_data = generate_data(n, X, seed=SEED)
    results = []
    for S in S_values:
        times = []
        for _ in range(repeats):
            arr = base_data.copy()
            start = time.process_time()
            hybrid_sort(arr, S)
            times.append(time.process_time() - start)
        results.append((S, min(times)))
    return results


def save_csv(filename, header, rows):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


if __name__ == "__main__":
    S_VALUES = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1000, 2000]
    D_S_CANDIDATES = [1, 3, 5, 7, 10, 13, 16, 20, 50]

    # Run the full experiment suite once per dataset type. Output CSV
    # filenames are suffixed with the label (e.g. "..._sorted.csv") so
    # results from different dataset types don't overwrite each other.
    for label, gen in DATASET_TYPES.items():
        # Redirect the global `generate_data` name to this pass's generator.
        # Every experiment_* function above calls generate_data(...) and
        # will now use `gen` for the rest of this loop iteration.
        globals()["generate_data"] = gen

        print(f"\n=== Dataset type: {label} ===")

        print("Running (c)-i: fixed S, varying n...")
        c1_results = experiment_c1(S_fixed=10)
        save_csv(f"c1_fixed_S_varying_n_{label}.csv", ["n", "comparisons"], c1_results)

        print("Running (c)-ii: fixed n, varying S...")
        c2_results = experiment_c2(n_fixed=200_000, S_values=S_VALUES)
        save_csv(f"c2_fixed_n_varying_S_{label}.csv", ["S", "comparisons"], c2_results)

        print("Running (c)-iii: optimal S per n...")
        c3_n_values = [10_000, 100_000, 1_000_000]
        c3_results = experiment_c3(n_values=c3_n_values, S_values=S_VALUES)
        save_csv(f"c3_optimal_S_per_n_{label}.csv", ["n", "best_S", "min_comparisons"], c3_results)

        print("Running CPU-time sweep at n=10,000,000 to find optimal S for (d)...")
        time_sweep_results = experiment_time_sweep(n=10_000_000, S_values=D_S_CANDIDATES, repeats=3)
        save_csv(f"time_sweep_10M_{label}.csv", ["S", "min_cpu_time_seconds"], time_sweep_results)

        optimal_S, optimal_time = min(time_sweep_results, key=lambda r: r[1])
        print(f"Optimal S by CPU time [{label}]: S={optimal_S} (time={optimal_time:.3f}s)")

        print("Running (d): hybrid vs merge sort on n=10,000,000...")
        d_result = experiment_d(n=10_000_000, optimal_S=optimal_S)
        d_rows = [
            ("hybrid", d_result["hybrid"][0], d_result["hybrid"][1]),
            ("merge", d_result["merge"][0], d_result["merge"][1]),
        ]
        save_csv(f"d_hybrid_vs_merge_{label}.csv", ["algorithm", "comparisons", "cpu_time_seconds"], d_rows)

    print("\nAll experiments complete for all dataset types. Results saved to:", RESULTS_DIR)