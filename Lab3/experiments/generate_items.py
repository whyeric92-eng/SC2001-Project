import random


def generate_items(n, seed=None, max_weight=100, max_profit=100):
    """n random object types: weights in 1..max_weight and profits in
    1..max_profit. Returns (w, p)."""
    rng = random.Random(seed)
    w = [rng.randint(1, max_weight) for _ in range(n)]
    p = [rng.randint(1, max_profit) for _ in range(n)]
    return w, p
