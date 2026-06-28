function rule110()
    width = 10_000
    generations = 50_000
    rule = [0, 1, 1, 1, 0, 1, 1, 0]

    current = zeros(Int, width)
    next = zeros(Int, width)
    current[width] = 1

    for _ in 1:generations
        @inbounds for i in 1:width
            left = i > 1 ? current[i - 1] : 0
            center = current[i]
            right = i < width ? current[i + 1] : 0
            index = left * 4 + center * 2 + right
            next[i] = rule[index + 1]
        end
        current, next = next, current
    end

    count = 0
    @inbounds for i in 1:width
        count += current[i]
    end
    println("Population: $count")
end

rule110()
