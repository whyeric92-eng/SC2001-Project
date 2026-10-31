def knapsack_dp(C, w, p):
    """Bottom-up dynamic programming for the unbounded knapsack problem.

    There are n = len(w) types of objects. An object of type i has
    weight w[i] and profit p[i], and there are unlimited copies of each
    type. Returns (P, choice):

      P[c]      the maximum profit with a knapsack of capacity c,
                for every c = 0..C (P[C] is the answer)
      choice[c] the type i of one object in an optimal packing for
                capacity c, or -1 if no object fits (P[c] = 0)

    Recursive definition:
      P(c) = max of p[i] + P(c - w[i]) over all i with w[i] <= c,
             or 0 if no object fits.
    """
    n = len(w)

    # Dictionary: a one-dimensional array, since every subproblem is
    # identified by a single capacity value.
    P = [0] * (C + 1)
    choice = [-1] * (C + 1)

    # P(c) only depends on P(c - w[i]) with smaller indices, so filling
    # the array from index 0 upwards always has those values ready.
    for c in range(1, C + 1):
        for i in range(n):
            # Try putting one object of type i in first; the rest of the
            # knapsack (capacity c - w[i]) is packed optimally.
            if w[i] <= c and p[i] + P[c - w[i]] > P[c]:
                P[c] = p[i] + P[c - w[i]]
                choice[c] = i

    return P, choice

# Time complexity: Theta(nC).
#   - The outer loop runs C times, the inner loop n times,
#     and each iteration takes constant time.
# Space complexity: Theta(C) for the arrays P and choice.
# This is pseudo-polynomial: polynomial in the value of C,
# not in the size of the input (C needs only log C bits).


def optimal_objects(C, w, choice):
    """Follows choice back from capacity C to list how many objects of
    each type an optimal packing uses."""
    count = [0] * len(w)
    c = C
    while choice[c] != -1:
        i = choice[c]
        count[i] += 1
        c -= w[i]
    return count


def show(C, w, p):
    """Prints the whole table P[0..C], then the answer and one optimal
    packing."""
    P, choice = knapsack_dp(C, w, p)

    print(f"C = {C}, w = {w}, p = {p}")
    print(f"{'c':>4} {'P(c)':>6}   object added")
    for c in range(C + 1):
        if choice[c] == -1:
            added = "-"
        else:
            i = choice[c]
            added = f"type {i} (w={w[i]}, p={p[i]}) + P({c - w[i]})"
        print(f"{c:>4} {P[c]:>6}   {added}")

    count = optimal_objects(C, w, choice)
    used = ", ".join(f"{k} x type {i}" for i, k in enumerate(count) if k > 0)
    print(f"P({C}) = {P[C]}  ->  {used if used else 'nothing fits'}")
    print()
    return P[C]


if __name__ == "__main__":
    # (4a) P(16) with the weights and profits of part (2).
    a = show(16, [4, 5, 8], [7, 6, 9])

    # (4b) P(12) with the second set of weights and profits.
    b = show(12, [5, 6, 7], [7, 6, 9])

    # Answers worked out by hand.
    print("matches hand-computed answers:", a == 28 and b == 16)
