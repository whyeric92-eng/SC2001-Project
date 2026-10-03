"""Times both Dijkstra implementations on random graphs of different
|V| and |E|, and saves the results to CSV.
"""
import csv, time, sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "dijkstra"))
sys.path.insert(0, os.path.dirname(__file__))

from dijkstra_matrix import dijkstra_matrix
from dijkstra_heap import dijkstra_heap
from generate_graph import generate_graph

SEED = 42
REPEATS = 3
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")

HEADER = ["V", "E", "matrix_time", "heap_time"]


def timing(algorithm, graph):
    """Time in seconds of one run of algorithm on graph, from source 0.

    Uses perf_counter: process_time only ticks every ~16 ms on Windows,
    which rounds most runs here down to 0.
    """
    start = time.perf_counter()
    algorithm(graph, 0)
    return time.perf_counter() - start


def measure_graph(n, m):
    """Generate one graph and time both implementations on it. Each is
    run REPEATS times and the fastest run is kept, to reduce noise."""
    matrix, adj = generate_graph(n, m, seed=SEED)

    matrix_times = []
    heap_times = []
    for _ in range(REPEATS):
        matrix_times.append(timing(dijkstra_matrix, matrix))
        heap_times.append(timing(dijkstra_heap, adj))

    return [n, m, min(matrix_times), min(heap_times)]


def experiment_fixed_v(n, m_values):
    """Fixed |V|, varying |E|: from sparse to dense."""
    results = []
    for m in m_values:
        print(f"  V={n}, E={m}")
        results.append(measure_graph(n, m))
    return results


def experiment_fixed_density(n_values, edges_for):
    """Varying |V|, with |E| = edges_for(|V|) for each |V|."""
    results = []
    for n in n_values:
        m = edges_for(n)
        print(f"  V={n}, E={m}")
        results.append(measure_graph(n, m))
    return results


def save_csv(filename, rows):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        writer.writerows(rows)


def sparse_edges(n):
    # Average degree about 10.
    return 5 * n


def dense_edges(n):
    # Half of all possible pairs are edges.
    return n * (n - 1) // 4


if __name__ == "__main__":
    # Experiment 1: fixed |V|, |E| from a tree up to the complete graph.
    FIXED_V = 1000
    M_VALUES = [999, 2_000, 5_000, 10_000, 20_000, 50_000,
                100_000, 200_000, 300_000, 400_000, 499_500]

    # Experiments 2 and 3: varying |V| at a fixed density.
    N_VALUES = [100, 200, 400, 600, 800, 1_000, 1_500, 2_000]

    print("Experiment 1: fixed V, varying E...")
    save_csv("fixed_v_varying_e.csv", experiment_fixed_v(FIXED_V, M_VALUES))

    print("Experiment 2: sparse graphs (E = 5V), varying V...")
    save_csv("sparse_varying_v.csv", experiment_fixed_density(N_VALUES, sparse_edges))

    print("Experiment 3: dense graphs (E = V(V-1)/4), varying V...")
    save_csv("dense_varying_v.csv", experiment_fixed_density(N_VALUES, dense_edges))

    print("All experiments complete. Results saved to:", RESULTS_DIR)
