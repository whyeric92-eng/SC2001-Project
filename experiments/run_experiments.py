import csv, time, sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sorting"))
sys.path.insert(0, os.path.dirname(__file__))

import counter
from hybrid_sort import hybrid_sort
from merge_sort import merge_sort
from generate_data import generate_data, SIZES, X

SEED = 42
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


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


def experiment_d(n, optimal_S):
    base_data = generate_data(n, X, seed=SEED)

    arr1 = base_data.copy()
    counter.reset_counter()
    start = time.process_time()
    hybrid_sort(arr1, optimal_S)
    hybrid_time = time.process_time() - start
    hybrid_comparisons = counter.comparisons

    arr2 = base_data.copy()
    counter.reset_counter()
    start = time.process_time()
    merge_sort(arr2)
    merge_time = time.process_time() - start
    merge_comparisons = counter.comparisons

    return {
        "hybrid": (hybrid_comparisons, hybrid_time),
        "merge": (merge_comparisons, merge_time),
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

    print("Running (c)-i: fixed S, varying n...")
    c1_results = experiment_c1(S_fixed=10)
    save_csv("c1_fixed_S_varying_n.csv", ["n", "comparisons"], c1_results)

    print("Running (c)-ii: fixed n, varying S...")
    c2_results = experiment_c2(n_fixed=200_000, S_values=S_VALUES)
    save_csv("c2_fixed_n_varying_S.csv", ["S", "comparisons"], c2_results)

    print("Running (c)-iii: optimal S per n...")
    c3_n_values = [10_000, 100_000, 1_000_000]
    c3_results = experiment_c3(n_values=c3_n_values, S_values=S_VALUES)
    save_csv("c3_optimal_S_per_n.csv", ["n", "best_S", "min_comparisons"], c3_results)

    print("Running CPU-time sweep at n=10,000,000 to find optimal S for (d)...")
    D_S_CANDIDATES = [1, 5, 10, 20, 50, 100]
    time_sweep_results = experiment_time_sweep(n=10_000_000, S_values=D_S_CANDIDATES, repeats=1)
    save_csv("time_sweep_10M.csv", ["S", "min_cpu_time_seconds"], time_sweep_results)

    optimal_S, optimal_time = min(time_sweep_results, key=lambda r: r[1])
    print(f"Optimal S by CPU time at n=10,000,000: S={optimal_S} (time={optimal_time:.3f}s)")

    print("Running (d): hybrid vs merge sort on n=10,000,000...")
    d_result = experiment_d(n=10_000_000, optimal_S=optimal_S)
    d_rows = [
        ("hybrid", d_result["hybrid"][0], d_result["hybrid"][1]),
        ("merge", d_result["merge"][0], d_result["merge"][1]),
    ]
    save_csv("d_hybrid_vs_merge.csv", ["algorithm", "comparisons", "cpu_time_seconds"], d_rows)

    print("All experiments complete. Results saved to:", RESULTS_DIR)