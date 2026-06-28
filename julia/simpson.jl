function simpson(n::Int)
    h = 1.0 / n
    s = 4.0 / (1.0 + 0.0 * 0.0) + 4.0 / (1.0 + 1.0 * 1.0)
    for i in 1:(n - 1)
        x = i * h
        if i % 2 == 0
            s += 2.0 * 4.0 / (1.0 + x * x)
        else
            s += 4.0 * 4.0 / (1.0 + x * x)
        end
    end
    return s * h / 3.0
end

n = 100_000_000
pi_est = simpson(n)
println("Pi ≈ $pi_est")
