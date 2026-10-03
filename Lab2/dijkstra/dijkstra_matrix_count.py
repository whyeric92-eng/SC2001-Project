"""Same as dijkstra_matrix.py, plus counting of distance comparisons in
counter.comparisons. Used only to count comparisons: the timing uses
dijkstra_matrix.py, so the counting does not slow it down.
"""
import counter

INF = float("inf")

def dijkstra_matrix_count(matrix, source):
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
            if in_queue[v]:
                if u == -1:
                    u = v
                else:
                    counter.comparisons += 1
                    if dist[v] < dist[u]:
                        u = v

        # The rest of Q is unreachable (graph not connected).
        if dist[u] == INF:
            break

        in_queue[u] = False

        # Relax every edge (u, v): scan the whole row, O(|V|).
        for v in range(n):
            if matrix[u][v] != INF:
                counter.comparisons += 1
                if dist[v] > dist[u] + matrix[u][v]:
                    dist[v] = dist[u] + matrix[u][v]
                    par[v] = u

    return dist, par
