import numpy as np


def monte_carlo_pi(n: int) -> float:
    x = np.random.random(n)
    y = np.random.random(n)
    count = np.sum(x * x + y * y <= 1.0)
    return 4.0 * count / n


n = 10_000_000
pi_est = monte_carlo_pi(n)
print(f"Pi ≈ {pi_est}")
