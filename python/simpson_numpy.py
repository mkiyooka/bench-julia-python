import numpy as np


def simpson(n: int) -> float:
    h = 1.0 / n
    f0 = 4.0 / (1.0 + 0.0 * 0.0)
    fn = 4.0 / (1.0 + 1.0 * 1.0)

    indices = np.arange(1, n)
    x = indices * h
    coeffs = np.where(indices % 2 == 0, 2.0, 4.0)
    s = f0 + fn + np.sum(coeffs * 4.0 / (1.0 + x * x))
    return s * h / 3.0


n = 50_000_000
pi_est = simpson(n)
print(f"Pi ≈ {pi_est}")
