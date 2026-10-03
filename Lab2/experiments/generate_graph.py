"""Generates a random connected graph with |V| vertices and |E| edges,
as both an adjacency matrix (part a) and adjacency lists (part b).
"""
import random

INF = float("inf")
MAX_WEIGHT = 100


def generate_graph(n, m, seed=None):
    """Random connected undirected graph: n vertices, m edges, integer
    weights in [1, MAX_WEIGHT]. Returns (matrix, adj).

    m must be between n - 1 (a tree) and n * (n - 1) / 2 (complete).
    """
    if m < n - 1 or m > n * (n - 1) // 2:
        raise ValueError("m must be between n - 1 and n * (n - 1) / 2")

    rng = random.Random(seed)

    matrix = []
    adj = []
    for _ in range(n):
        matrix.append([INF] * n)
        adj.append([])

    # Step 1: a random spanning tree makes the graph connected. Visit
    # the vertices in random order, joining each to an earlier one.
    order = []
    for v in range(n):
        order.append(v)
    rng.shuffle(order)
    for i in range(1, n):
        u = order[i]
        v = order[rng.randint(0, i - 1)]
        add_edge(matrix, adj, u, v, rng.randint(1, MAX_WEIGHT))

    # Step 2: add random edges until there are m. Pairs that are the
    # same vertex or already joined are skipped and tried again.
    edges = n - 1
    while edges < m:
        u = rng.randint(0, n - 1)
        v = rng.randint(0, n - 1)
        if u != v and matrix[u][v] == INF:
            add_edge(matrix, adj, u, v, rng.randint(1, MAX_WEIGHT))
            edges += 1

    return matrix, adj


def add_edge(matrix, adj, u, v, w):
    # Undirected graph: store the edge in both directions.
    matrix[u][v] = w
    matrix[v][u] = w
    adj[u].append((v, w))
    adj[v].append((u, w))


if __name__ == "__main__":
    # Quick sanity check on a tiny graph: 5 vertices, 6 edges.
    matrix, adj = generate_graph(5, 6, seed=42)

    print("adjacency matrix:")
    for row in matrix:
        print("  ", row)

    print("adjacency lists:")
    for u in range(len(adj)):
        print("  ", u, "->", adj[u])
