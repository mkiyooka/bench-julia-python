import numpy as np


def rule110(width, generations):
    rule = np.array([0, 1, 1, 1, 0, 1, 1, 0], dtype=np.int32)

    current = np.zeros(width, dtype=np.int32)
    current[width - 1] = 1

    for _ in range(generations):
        left = np.roll(current, 1)
        right = np.roll(current, -1)
        left[0] = 0
        right[-1] = 0
        index = left * 4 + current * 2 + right
        current = rule[index]

    count = np.sum(current)
    return count


count = rule110(5_000, 20_000)
print(f"Population: {count}")
