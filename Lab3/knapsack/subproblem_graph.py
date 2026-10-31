"""Part (2): the subproblem graph of P(C).

Vertices are the capacities c reachable from C. There is a directed
edge c -> c - w[i] for every type i with w[i] <= c, because computing
P(c) makes a recursive call on P(c - w[i]).
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
PLOT_DIR = os.path.join(HERE, "..", "results", "plots")

# Edge colour of each object type, same palette as Lab1 and Lab2.
COLOURS = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]


def subproblem_graph(C, w):
    """Returns (vertices, edges) of the subproblem graph of P(C).

    vertices: the reachable capacities, largest first
    edges:    (c, c - w[i], i) for every vertex c and type i that fits
    """
    vertices = set()
    edges = []
    stack = [C]

    # Depth-first search from C: each capacity is expanded only once.
    while stack:
        c = stack.pop()
        if c in vertices:
            continue
        vertices.add(c)
        for i in range(len(w)):
            if w[i] <= c:
                edges.append((c, c - w[i], i))
                stack.append(c - w[i])

    edges.sort(key=lambda e: (-e[0], e[2]))
    return sorted(vertices, reverse=True), edges


def layers(C, vertices, edges):
    """Puts each vertex on the layer of its longest path from C, so
    every edge points to a lower layer."""
    level = {C: 0}
    for c in vertices:                  # largest first: parents come first
        for x, d, _ in edges:
            if x == c:
                level[d] = max(level.get(d, 0), level[c] + 1)
    rows = {}
    for c in vertices:
        rows.setdefault(level[c], []).append(c)
    return [rows[k] for k in sorted(rows)]


def draw(C, w, p, path):
    """Draws the subproblem graph top-down, P(C) at the top. Each edge
    is coloured by the object type it subtracts."""
    vertices, edges = subproblem_graph(C, w)

    # Position: layers top-down, vertices of a layer spread evenly and
    # centred, largest capacity on the left.
    rows = layers(C, vertices, edges)
    width = max(len(r) for r in rows)
    pos = {}
    for k, row in enumerate(rows):
        for j, c in enumerate(row):
            pos[c] = ((j - (len(row) - 1) / 2) * 2.0 * width / len(row) * 0.9,
                      -2.2 * k)

    fig, ax = plt.subplots(figsize=(9, 7))
    radius = 0.45

    for c, d, i in edges:
        (x1, y1), (x2, y2) = pos[c], pos[d]
        # Edges that skip a layer are bent so they pass around the
        # vertices in between.
        skip = round((y1 - y2) / 2.2) > 1
        rad = (0.25 if x2 >= x1 else -0.25) if skip else 0.0
        ax.add_patch(FancyArrowPatch(
            (x1, y1), (x2, y2),
            connectionstyle=f"arc3,rad={rad}",
            arrowstyle="-|>", mutation_scale=15, lw=1.8,
            color=COLOURS[i % len(COLOURS)],
            shrinkA=19, shrinkB=19, zorder=1,
        ))

    for c in vertices:
        base = not any(wi <= c for wi in w)
        ax.add_patch(plt.Circle(
            pos[c], radius, zorder=2,
            facecolor="#dddddd" if base else "white",
            edgecolor="#333333", lw=1.5,
        ))
        ax.text(*pos[c], f"P({c})", ha="center", va="center",
                fontsize=10.5, fontweight="bold", zorder=3)

    legend = [
        Line2D([0], [0], color=COLOURS[i % len(COLOURS)], lw=2,
               label=f"type {i}: c → c − {w[i]}   (w={w[i]}, p={p[i]})")
        for i in range(len(w))
    ]
    legend.append(Line2D([0], [0], marker="o", color="w",
                         markerfacecolor="#dddddd", markeredgecolor="#333333",
                         markersize=12, label="base case: nothing fits, P = 0"))
    ax.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.5, 0.0),
              ncol=2, fontsize=10, frameon=False)

    ax.set_title(f"Subproblem graph of P({C}): "
                 f"{len(vertices)} vertices, {len(edges)} edges", fontsize=13)
    xs = [x for x, _ in pos.values()]
    ax.set_xlim(min(xs) - 1, max(xs) + 1)
    ax.set_ylim(-2.2 * (len(rows) - 1) - 0.8, 0.8)
    ax.set_aspect("equal")
    ax.axis("off")

    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    # Part (2): P(15) with n = 3.
    C, w, p = 15, [4, 5, 8], [7, 6, 9]
    vertices, edges = subproblem_graph(C, w)

    print(f"Subproblem graph of P({C}), w = {w}")
    print(f"{len(vertices)} vertices: {vertices}")
    print(f"{len(edges)} edges:")
    for c in vertices:
        out = [f"P({d})" for x, d, _ in edges if x == c]
        print(f"  P({c:>2}) -> {', '.join(out) if out else '(base case)'}")

    path = os.path.join(PLOT_DIR, "subproblem_graph_P15.png")
    draw(C, w, p, path)
    print("saved", os.path.normpath(path))
