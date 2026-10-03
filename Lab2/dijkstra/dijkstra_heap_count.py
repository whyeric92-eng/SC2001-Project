"""Same as dijkstra_heap.py, plus counting of distance comparisons in
counter.comparisons. Used only to count comparisons: the timing uses
dijkstra_heap.py, so the counting does not slow it down.
"""
import counter
from min_heap_count import build_min_heap, enqueue, dequeue

INF = float("inf")

def dijkstra_heap_count(adj, source):
    n = len(adj)

    # Initialize(G, s)
    dist = [INF] * n
    par = [None] * n
    dist[source] = 0

    # Heap priority queue: holds (dist, vertex) pairs for all vertices,
    # in_queue[v] says whether v is still in Q.
    queue = []
    for v in range(n):
        queue.append((dist[v], v))
    build_min_heap(queue)
    in_queue = [True] * n

    # While Q is not empty
    while len(queue) > 0:
        # Remove u with minimal dist from Q: O(log |V|).
        _, u = dequeue(queue)

        # Outdated pair: u was already removed with a smaller dist.
        if not in_queue[u]:
            continue

        # The rest of Q is unreachable (graph not connected).
        if dist[u] == INF:
            break

        in_queue[u] = False

        # Relax every edge (u, v): only u's own edges are visited.
        for v, w in adj[u]:
            counter.comparisons += 1
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                par[v] = u
                # Add v with its new dist; the old pair becomes outdated.
                enqueue(queue, (dist[v], v))

    return dist, par
