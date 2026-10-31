# SC2001 Project 3: Dynamic Programming

Course project for SC2001 (Algorithm Design and Analysis).

Solves the unbounded knapsack problem with bottom-up dynamic programming:
a knapsack of capacity `C` and `n` types of objects, where type `i` has
weight `w[i]` and profit `p[i]`, with unlimited copies of each type. Find
the largest total profit that fits in the knapsack.

## Recursive definition

`P(C)` is the maximum profit with capacity `C`:

```
P(C) = 0                                       if w[i] > C for every i
P(C) = max { p[i] + P(C - w[i]) : w[i] <= C }  otherwise
```

i.e. try every object type that fits as one object in the knapsack, pack
the remaining capacity `C - w[i]` optimally, and keep the best.

Since every type has unlimited copies, a subproblem only needs the
capacity, so the table is one-dimensional, like the coin change problem in
the lecture, unlike the two-dimensional table of 0/1 knapsack.

## Structure

| File | Description |
| ---- | ----------- |
| `knapsack/knapsack_dp.py` | Parts (3) and (4): the bottom-up algorithm, and the runs of P(16) and P(12) |
| `knapsack/subproblem_graph.py` | Part (2): finds the subproblem graph of P(15) and draws it |
| `results/plots/subproblem_graph_P15.png` | The subproblem graph of P(15) drawn by the script above |
| `knapsack/knapsack_topdown.py` | Top-down DP (recursion + dictionary), for comparison |
| `knapsack/knapsack_recursive.py` | Plain recursion without a dictionary, for comparison |
| `knapsack/knapsack_dp_count.py`, `knapsack/counter.py` | Copy of `knapsack_dp.py` that also counts comparisons between profit values |
| `experiments/generate_items.py` | `n` random object types, weights and profits in 1 to 100 |
| `experiments/run_experiments.py` | Runs the experiments and writes the CSVs to `results/` |
| `experiments/plot_results.py` | Plots the CSVs against the theoretical curves into `results/plots/` |

Comparisons are counted with the `_count` copy and time is measured on the
original file, so the counting code does not slow down the timing, as in
Lab2.

## Running

```
python knapsack/knapsack_dp.py          # prints the table P[0..C] for (4a) and (4b)
python knapsack/subproblem_graph.py     # needs matplotlib
python knapsack/knapsack_topdown.py     # each checks itself against
python knapsack/knapsack_recursive.py   # the bottom-up DP on (4a) and (4b)
python experiments/run_experiments.py   # about half a minute
python experiments/plot_results.py      # needs matplotlib, numpy, pandas
```

## Results

| Part | Weights | Profits | Answer | One optimal packing |
| ---- | ------- | ------- | ------ | ------------------- |
| (4a) | 4, 5, 8 | 7, 6, 9 | P(16) = 28 | 4 objects of type 0 |
| (4b) | 5, 6, 7 | 7, 6, 9 | P(12) = 16 | 1 of type 0, 1 of type 2 |

The subproblem graph of P(15) has 10 vertices
`{15, 11, 10, 7, 6, 5, 3, 2, 1, 0}` and 15 edges. Several vertices, such as
P(2), are reached from more than one vertex: a plain recursive function would
compute them again each time, while the DP computes each one once.

## Complexity

- Time: `Θ(nC)`. `C` capacities, each tries `n` types in constant time.
- The bottom-up DP makes exactly `Σ max(0, C - w[i] + 1)` comparisons
  between profit values (type `i` is compared for every capacity from
  `w[i]` to `C`), about `nC` when `C` is much larger than the weights. The
  count depends only on `C` and the weights, so there is no separate best,
  worst or average case.
- Space: `Θ(C)` for the one-dimensional table.
- This is pseudo-polynomial: polynomial in the value of `C`, but `C` takes
  only `log C` bits to write, so the time is exponential in the input size.
- Top-down DP is also `O(nC)`, but only solves the subproblems reachable
  from `C`.
- Plain recursion is exponential in `C`: it makes
  `T(C) = 1 + Σ T(C - w[i])` calls (over all `w[i] <= C`).

## Experiments

| Experiment | Objects | Comparisons | Time | CSV |
| ---------- | ------- | ----------- | ---- | --- |
| 1 | n = 10, C from 10,000 to 100,000 | bottom-up | bottom-up, top-down | `varying_c.csv` |
| 2 | C = 10,000, n from 10 to 100 | bottom-up | bottom-up, top-down | `varying_n.csv` |
| 3 | Objects of part (2), C from 0 to 80 | - | plain recursion, top-down, bottom-up | `recursive_vs_dp.csv` |

Random objects use seed 42. Time is the fastest of 3 runs (50 runs for the
DP in experiment 3, which takes only microseconds). Every run also checks
that all versions give the same answer.

## Findings

- The comparisons of the bottom-up DP equal `Σ max(0, C - w[i] + 1)`
  exactly at every point, between 99.5% and 99.96% of `nC`.
- Both DP versions grow linearly in `C` and in `n`: the ratio of empirical
  time to `c · nC` stays near 1, matching `Θ(nC)`.
- Top-down is about 2 to 3 times slower than bottom-up, from the cost of
  the recursive calls and the dictionary.
- Plain recursion matches its exact number of calls `T(C)`, which grows by
  about 1.22 times for each unit of `C`. At `C = 80` it makes 12,562,962
  calls and takes about 3 s, while bottom-up solves 81 subproblems in
  about 20 µs, over 100,000 times faster.
