import numpy as np
from numba import njit


@njit
def step(current, next_gen, rule, width):
    for i in range(width):
        left = current[i - 1] if i > 0 else 0
        center = current[i]
        right = current[i + 1] if i < width - 1 else 0
        index = left * 4 + center * 2 + right
        next_gen[i] = rule[index]


@njit
def run(width, generations, rule):
    current = np.zeros(width, dtype=np.int32)
    next_gen = np.zeros(width, dtype=np.int32)
    current[width - 1] = 1

    for _ in range(generations):
        step(current, next_gen, rule, width)
        current, next_gen = next_gen, current

    count = 0
    for i in range(width):
        count += current[i]
    return count


rule = np.array([0, 1, 1, 1, 0, 1, 1, 0], dtype=np.int32)

# warmup
run(100, 10, rule)

# main
count = run(5_000, 20_000, rule)
print(f"Population: {count}")
