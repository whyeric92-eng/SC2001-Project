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

## Running

```
python knapsack/knapsack_dp.py          # prints the table P[0..C] for (4a) and (4b)
python knapsack/subproblem_graph.py     # needs matplotlib
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
- Space: `Θ(C)` for the one-dimensional table.
- This is pseudo-polynomial: polynomial in the value of `C`, but `C` takes
  only `log C` bits to write, so the time is exponential in the input size.
