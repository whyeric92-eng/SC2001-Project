"""Same as knapsack_dp.py, plus counting of profit comparisons in
counter.comparisons. Used only to count comparisons: the timing uses
knapsack_dp.py, so the counting does not slow it down.
"""
import counter


def knapsack_dp_count(C, w, p):
    n = len(w)
    P = [0] * (C + 1)
    choice = [-1] * (C + 1)

    for c in range(1, C + 1):
        for i in range(n):
            if w[i] <= c:
                # One comparison: is type i better than the best so far?
                counter.comparisons += 1
                if p[i] + P[c - w[i]] > P[c]:
                    P[c] = p[i] + P[c - w[i]]
                    choice[c] = i

    return P, choice
