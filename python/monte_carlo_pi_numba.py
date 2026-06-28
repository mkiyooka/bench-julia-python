import random

from numba import njit


@njit
def monte_carlo_pi(n: int) -> float:
    count = 0
    for _ in range(n):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            count += 1
    return 4.0 * count / n


monte_carlo_pi(1000)

n = 10_000_000
pi_est = monte_carlo_pi(n)
print(f"Pi ≈ {pi_est}")
