# SC2001 Project 2: The Dijkstra's Algorithm

Course project for SC2001 (Algorithm Design and Analysis).

Implements Dijkstra's single-source shortest path algorithm in two settings,
then studies how their number of comparisons and running time grow with
`|V|` and `|E|`, both theoretically and empirically:

- **(a)** adjacency matrix + array priority queue: `Θ(|V|²)`
- **(b)** array of adjacency lists + min-heap priority queue:
  `O((|V| + |E|) log |V|)`, i.e. `O(|E| log |V|)` for a connected graph

The heap only supports enqueue and dequeue (as in the lecture), so (b) uses
lazy deletion instead of decrease-key: when a distance drops, a new
`(dist, vertex)` pair is enqueued, and outdated pairs are skipped when they
are dequeued.

## Structure

| File | Description |
| ---- | ----------- |
| `dijkstra/dijkstra_matrix.py` | Part (a) |
| `dijkstra/min_heap.py` | Binary min-heap: `min_heapify`, `build_min_heap`, `enqueue`, `dequeue` |
| `dijkstra/dijkstra_heap.py` | Part (b) |
| `dijkstra/*_count.py`, `dijkstra/counter.py` | Copies of the three files above that also count comparisons between distance values |
| `experiments/generate_graph.py` | Random connected undirected graph with `n` vertices and `m` edges, as both a matrix and adjacency lists |
| `experiments/run_experiments.py` | Runs the experiments and writes the CSVs to `results/` |
| `experiments/plot_results.py` | Plots the CSVs against the theoretical curves into `results/plots/` |

Comparisons are counted with the `_count` copies and time is measured on the
original files, because the counting code itself takes time and would slow
the algorithm that compares more by more, distorting the comparison between
(a) and (b).

## Running

```
python dijkstra/dijkstra_matrix.py      # each checks itself on the
python dijkstra/dijkstra_heap.py        # example graph from the lecture
python experiments/run_experiments.py   # a few minutes
python experiments/plot_results.py      # needs matplotlib, numpy, pandas
```

## Experiments

| Experiment | Graphs | CSV |
| ---------- | ------ | --- |
| 1 | V = 1000, E from 999 (a tree) to 499,500 (complete graph) | `fixed_v_varying_e.csv` |
| 2 | Sparse, E = 5V, V from 100 to 2000 | `sparse_varying_v.csv` |
| 3 | Dense, E = V(V-1)/4, V from 100 to 2000 | `dense_varying_v.csv` |

Each data point uses one random graph (seed 42, edge weights 1 to 100,
source vertex 0). Time is the fastest of 3 runs.

## Findings

- (a) makes exactly `|V|(|V|-1)/2 + 2|E|` comparisons on a connected graph,
  and its time grows with `|V|²`, almost unaffected by `|E|`.
- (b) grows with `|E|`, but stays well below its worst-case bound, because
  most relaxations on random graphs do not improve a distance and so do not
  touch the heap.
- Sparse graphs: (b) is over 10 times faster at `|V| = 2000`.
- Very dense graphs: (a) is faster. At `|V| = 1000` the two cross at about
  `|E| = 300,000`, i.e. about 60% of all possible edges.
