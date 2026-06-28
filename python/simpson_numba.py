from numba import njit


@njit
def simpson(n: int) -> float:
    h = 1.0 / n
    s = 4.0 / (1.0 + 0.0 * 0.0) + 4.0 / (1.0 + 1.0 * 1.0)
    for i in range(1, n):
        x = i * h
        if i % 2 == 0:
            s += 2.0 * 4.0 / (1.0 + x * x)
        else:
            s += 4.0 * 4.0 / (1.0 + x * x)
    return s * h / 3.0


simpson(1000)

n = 100_000_000
pi_est = simpson(n)
print(f"Pi ≈ {pi_est}")
