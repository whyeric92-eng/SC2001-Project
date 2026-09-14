import random

X = 10**9

SIZES = [1_000, 2_000, 5_000, 10_000, 20_000, 50_000, 100_000, 200_000, 500_000, 1_000_000, 2_000_000, 5_000_000, 10_000_000]


def generate_data(n, x, seed=None):
    """Generate a random array of n integers in [1, x]."""
    rng = random.Random(seed)
    return [rng.randint(1, x) for _ in range(n)]


def generate_sorted(n, x, seed=None):
    """Generate a fully ascending-sorted array of n integers in [1, x].

    Starts from the same random data as generate_data (same seed), then
    sorts it, so the underlying values are comparable across dataset types.
    """
    data = generate_data(n, x, seed=seed)
    data.sort()
    return data


def generate_reverse_sorted(n, x, seed=None):
    """Generate a fully descending-sorted array of n integers in [1, x].

    This is the worst case for the insertion-sort base case (every
    inserted element has to shift all the way to the front).
    """
    data = generate_data(n, x, seed=seed)
    data.sort(reverse=True)
    return data


def generate_almost_sorted(n, x, seed=None, swap_fraction=0.05):
    """Generate a sorted array of n integers in [1, x] with a small
    fraction of elements randomly swapped out of place.

    swap_fraction=0.05 means 5% of n random index pairs get swapped
    after sorting. Uses the same seed as the sort/rng so runs are
    reproducible.
    """
    data = generate_data(n, x, seed=seed)
    data.sort()
    rng = random.Random(seed)  # separate RNG instance, same seed, for the swap positions
    num_swaps = max(1, int(n * swap_fraction))
    for _ in range(num_swaps):
        i = rng.randint(0, n - 1)
        j = rng.randint(0, n - 1)
        data[i], data[j] = data[j], data[i]
    return data


if __name__ == "__main__":
    # Quick sanity check of all four generators on a tiny array.
    print("random:        ", generate_data(10, 100, seed=42))
    print("sorted:        ", generate_sorted(10, 100, seed=42))
    print("reverse_sorted:", generate_reverse_sorted(10, 100, seed=42))
    print("almost_sorted: ", generate_almost_sorted(10, 100, seed=42))