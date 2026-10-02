INF = float("inf")

def dijkstra_matrix(matrix, source):
    """Part (a): Dijkstra with an adjacency matrix and an array as the
    priority queue.

    matrix[u][v] is the weight of edge (u, v), or INF if there is no
    edge. Returns (dist, par).
    """
    n = len(matrix)

    # Initialize(G, s)
    dist = [INF] * n
    par = [None] * n
    dist[source] = 0

    # Array priority queue: dist holds the keys, in_queue[v] says whether v is still in Q.
    in_queue = [True] * n

    # While Q is not empty: one vertex is removed per iteration.
    for _ in range(n):
        # Remove u with minimal dist from Q: full scan, O(|V|).
        u = -1
        for v in range(n):
            if in_queue[v] and (u == -1 or dist[v] < dist[u]):
                u = v

        # The rest of Q is unreachable (graph not connected).
        if dist[u] == INF:
            break

        in_queue[u] = False

        # Relax every edge (u, v): scan the whole row, O(|V|).
        for v in range(n):
            if matrix[u][v] != INF and dist[v] > dist[u] + matrix[u][v]:
                dist[v] = dist[u] + matrix[u][v]
                par[v] = u

    return dist, par

# Time complexity: Theta(|V|^2), independent of |E|.
#   - Initialize:           O(|V|)
#   - Remove minimum:       |V| times, O(|V|) each  -> O(|V|^2)
#   - Scan row of u:        |V| times, O(|V|) each  -> O(|V|^2)
#   - Relax updates:        at most 2|E| in total   -> O(|E|)
# Since |E| < |V|^2, the total is O(|V|^2).


if __name__ == "__main__":
    # Correctness check: run on the example graph from the lecture
    # slides (page 17), a..j -> 0..9, and compare with the slides' answer.
    names = "abcdefghij"
    edges = [
        ("a", "c", 1), ("a", "b", 6), ("c", "e", 4), ("c", "g", 7),
        ("b", "e", 8), ("b", "d", 3), ("e", "d", 9), ("e", "f", 5),
        ("e", "h", 7), ("d", "f", 2), ("g", "h", 0), ("g", "i", 2),
        ("h", "i", 4), ("h", "f", 0), ("h", "j", 9), ("f", "j", 5),
        ("i", "j", 6),
    ]

    n = len(names)
    matrix = [[INF] * n for _ in range(n)]
    for u, v, w in edges:
        # Undirected graph: store each edge in both directions.
        matrix[names.index(u)][names.index(v)] = w
        matrix[names.index(v)][names.index(u)] = w

    dist, par = dijkstra_matrix(matrix, names.index("a"))
    for v in range(n):
        parent = names[par[v]] if par[v] is not None else "-"
        print(f"{names[v]}: dist = {dist[v]}, par = {parent}")

    expected = [0, 6, 1, 9, 5, 8, 8, 8, 10, 13]
    print("matches lecture slides:", dist == expected)
