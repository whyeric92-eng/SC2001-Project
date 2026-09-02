import random

X = 10**9

SIZES = [1_000, 2_000, 5_000, 10_000, 20_000, 50_000, 100_000, 200_000, 500_000, 1_000_000, 2_000_000, 5_000_000, 10_000_000]

def generate_data(n, x, seed=None):
    rng = random.Random(seed)
    return [rng.randint(1, x) for _ in range(n)]

if __name__ == "__main__":
    data = generate_data(10, 100, seed=42)
    print(data)