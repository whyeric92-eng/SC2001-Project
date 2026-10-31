def knapsack_recursive(C, w, p):
    """Plain recursion, no dictionary, for comparison with the DP.

    Follows the recursive definition directly:
      P(c) = max of p[i] + P(c - w[i]) over all i with w[i] <= c,
             or 0 if no object fits.
    The same subproblem is solved again every time it is reached.
    """
    best = 0
    for i in range(len(w)):
        if w[i] <= C:
            best = max(best, p[i] + knapsack_recursive(C - w[i], w, p))
    return best

# Time complexity: exponential in C.
# Let T(c) be the number of calls made for capacity c. Then
#   T(c) = 1 + sum of T(c - w[i]) over all i with w[i] <= c.
# E.g. with w = [1, 2] this is the Fibonacci recurrence, Theta(1.618^c).


if __name__ == "__main__":
    # Correctness check: compare with the bottom-up DP on part (4).
    from knapsack_dp import knapsack_dp

    for C, w, p in [(16, [4, 5, 8], [7, 6, 9]), (12, [5, 6, 7], [7, 6, 9])]:
        rec = knapsack_recursive(C, w, p)
        dp = knapsack_dp(C, w, p)[0][C]
        print(f"P({C}), w = {w}, p = {p}: recursive = {rec}, bottom-up = {dp}")
