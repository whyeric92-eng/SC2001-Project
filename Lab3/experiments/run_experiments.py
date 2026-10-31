"""Counts the comparisons of the bottom-up DP and times all the knapsack
algorithms for different C and n, and saves the results to CSV.
"""
import csv, time, sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "knapsack"))
sys.path.insert(0, os.path.dirname(__file__))

import counter
from knapsack_dp import knapsack_dp
from knapsack_dp_count import knapsack_dp_count
from knapsack_topdown import knapsack_topdown
from knapsack_recursive import knapsack_recursive
from generate_items import generate_items

SEED = 42
REPEATS = 3
# The DP takes only microseconds in experiment 3, so it is timed more
# often there to remove noise.
REPEATS_FAST = 50
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")

# Objects of part (2), used for experiment 3.
W2, P2 = [4, 5, 8], [7, 6, 9]


def timing(algorithm, C, w, p, repeats=REPEATS):
    """Fastest of repeats runs, in seconds, to reduce noise.

    Uses perf_counter: process_time only ticks every ~16 ms on Windows.
    Also returns the answer, to check all versions agree.
    """
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        answer = algorithm(C, w, p)
        best = min(best, time.perf_counter() - start)
    return best, answer


def counting(algorithm, C, w, p):
    """Number of profit comparisons in one run, and the answer.
    The same input always gives the same count."""
    counter.reset_counter()
    answer = algorithm(C, w, p)
    return counter.comparisons, answer


def bottom_up(C, w, p):
    return knapsack_dp(C, w, p)[0][C]


def bottom_up_count(C, w, p):
    return knapsack_dp_count(C, w, p)[0][C]


def save(name, header, rows):
    path = os.path.join(RESULTS_DIR, name)
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print("  saved", os.path.normpath(path))


DP_HEADER = ["C", "n", "bottomup_comparisons", "bottomup_time",
             "topdown_time"]


def measure_dp(C, w, p):
    """Counts the comparisons of the bottom-up DP and times both DP
    versions on one input, and checks they give the same answer.

    Comparisons are counted with knapsack_dp_count. Time is measured on
    knapsack_dp, without counting, so the counting does not slow it down.
    """
    k_bu, a1 = counting(bottom_up_count, C, w, p)
    t_bu, a2 = timing(bottom_up, C, w, p)
    t_td, a3 = timing(knapsack_topdown, C, w, p)
    assert a1 == a2 == a3
    return [C, len(w), k_bu, t_bu, t_td]


def experiment_1():
    """Fixed n = 10, C from 10,000 to 100,000."""
    print("Experiment 1: n = 10, varying C")
    w, p = generate_items(10, seed=SEED)
    rows = []
    for C in range(10_000, 100_001, 10_000):
        rows.append(measure_dp(C, w, p))
        print(f"  C = {C:>6}: bottom-up {rows[-1][2]} comparisons, "
              f"{rows[-1][3]:.4f}s")
    save("varying_c.csv", DP_HEADER, rows)


def experiment_2():
    """Fixed C = 10,000, n from 10 to 100. Each n gets its own random
    objects."""
    print("Experiment 2: C = 10,000, varying n")
    C = 10_000
    rows = []
    for n in range(10, 101, 10):
        w, p = generate_items(n, seed=SEED)
        rows.append(measure_dp(C, w, p))
        print(f"  n = {n:>3}: bottom-up {rows[-1][2]} comparisons, "
              f"{rows[-1][3]:.4f}s")
    save("varying_n.csv", DP_HEADER, rows)


def recursive_calls(C, w):
    """Exact number of calls the plain recursion makes for P(C):
    T(c) = 1 + sum of T(c - w[i]) over all i with w[i] <= c."""
    T = [0] * (C + 1)
    for c in range(C + 1):
        T[c] = 1 + sum(T[c - x] for x in w if x <= c)
    return T[C]


def experiment_3():
    """Objects of part (2), C from 0 to 80: time of the plain recursion
    against both DP versions. The recursion takes a few seconds at
    C = 80."""
    print("Experiment 3: objects of part (2), recursion vs DP")
    n = len(W2)
    rows = []
    for C in range(0, 81, 5):
        t_rec, r = timing(knapsack_recursive, C, W2, P2)
        t_td, b = timing(knapsack_topdown, C, W2, P2, REPEATS_FAST)
        t_bu, a = timing(bottom_up, C, W2, P2, REPEATS_FAST)
        assert r == a == b
        rows.append([C, n, recursive_calls(C, W2), t_rec, t_td, t_bu])
        print(f"  C = {C:>2}: recursive {t_rec:.4f}s, "
              f"top-down {t_td:.6f}s, bottom-up {t_bu:.6f}s")
    save("recursive_vs_dp.csv",
         ["C", "n", "recursive_calls", "recursive_time",
          "topdown_time", "bottomup_time"], rows)


if __name__ == "__main__":
    os.makedirs(RESULTS_DIR, exist_ok=True)
    experiment_1()
    experiment_2()
    experiment_3()
