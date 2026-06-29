import numpy as np
from numba import njit


@njit
def rule110(width, generations):
    rule = np.array([0, 1, 1, 1, 0, 1, 1, 0], dtype=np.int32)

    current = np.zeros(width, dtype=np.int32)
    next_gen = np.zeros(width, dtype=np.int32)
    current[width - 1] = 1

    for _ in range(generations):
        for i in range(width):
            left = current[i - 1] if i > 0 else 0
            center = current[i]
            right = current[i + 1] if i < width - 1 else 0
            index = left * 4 + center * 2 + right
            next_gen[i] = rule[index]
        current, next_gen = next_gen, current

    count = 0
    for i in range(width):
        count += current[i]
    return count


# warmup
rule110(100, 10)

# main
count = rule110(5_000, 20_000)
print(f"Population: {count}")
