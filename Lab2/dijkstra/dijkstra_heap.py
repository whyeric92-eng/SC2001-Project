from min_heap import build_min_heap, enqueue, dequeue

INF = float("inf")

def dijkstra_heap(adj, source):
    """Part (b): Dijkstra with an array of adjacency lists and a
    min-heap as the priority queue.

    adj[u] is the list of (v, w) pairs, one per edge (u, v) of weight
    w. Returns (dist, par).
    """
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
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                par[v] = u
                # Add v with its new dist; the old pair becomes outdated.
                enqueue(queue, (dist[v], v))

    return dist, par

# Time complexity: O((|V| + |E|) log |V|), which is O(|E| log |V|)
# for a connected graph.
#   - Initialize, build heap:  O(|V|)
#   - Scan adjacency lists:    each list once, 2|E| pairs  -> O(|E|)
#   - enqueue:                 at most 2|E| times
#   - dequeue:                 at most |V| + 2|E| times
# The heap never holds more than |V| + 2|E| < 3|V|^2 pairs, so each
# enqueue/dequeue is O(log |V|)  -> O((|V| + |E|) log |V|) in total.


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
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        # Undirected graph: store each edge in both directions.
        adj[names.index(u)].append((names.index(v), w))
        adj[names.index(v)].append((names.index(u), w))

    dist, par = dijkstra_heap(adj, names.index("a"))
    for v in range(n):
        parent = names[par[v]] if par[v] is not None else "-"
        print(f"{names[v]}: dist = {dist[v]}, par = {parent}")

    expected = [0, 6, 1, 9, 5, 8, 8, 8, 10, 13]
    print("matches lecture slides:", dist == expected)
