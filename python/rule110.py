def rule110():
    width = 10_000
    generations = 50_000
    rule = [0, 1, 1, 1, 0, 1, 1, 0]

    current = [0] * width
    next_gen = [0] * width
    current[width - 1] = 1

    for _ in range(generations):
        for i in range(width):
            left = current[i - 1] if i > 0 else 0
            center = current[i]
            right = current[i + 1] if i < width - 1 else 0
            index = left * 4 + center * 2 + right
            next_gen[i] = rule[index]
        current, next_gen = next_gen, current

    count = sum(current)
    print(f"Population: {count}")


rule110()
