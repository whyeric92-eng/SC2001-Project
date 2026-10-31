import sys


def knapsack_topdown(C, w, p):
    """Top-down dynamic programming: the same recursion as
    knapsack_recursive, but each solution is stored in a dictionary and
    never recomputed (lecture slides, pages 10-14).

    Only the subproblems reachable from C are solved, i.e. the vertices
    of the subproblem graph.
    """
    # The recursion goes up to C / min(w) levels deep.
    sys.setrecursionlimit(max(1000, C + 100))
    soln = {}

    def P(c):
        if c in soln:                     # solved before: retrieve it
            return soln[c]
        best = 0
        for i in range(len(w)):
            if w[i] <= c:
                best = max(best, p[i] + P(c - w[i]))
        soln[c] = best                    # store before returning
        return best

    return P(C)

# Time complexity: O(nC).
# At most C + 1 subproblems are solved, each once, and each tries n
# types in constant time (the recursive calls on solved subproblems
# just retrieve the stored solution).


if __name__ == "__main__":
    # Correctness check: compare with the bottom-up DP on part (4).
    from knapsack_dp import knapsack_dp

    for C, w, p in [(16, [4, 5, 8], [7, 6, 9]), (12, [5, 6, 7], [7, 6, 9])]:
        td = knapsack_topdown(C, w, p)
        dp = knapsack_dp(C, w, p)[0][C]
        print(f"P({C}), w = {w}, p = {p}: top-down = {td}, bottom-up = {dp}")
