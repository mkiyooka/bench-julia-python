function monte_carlo_pi_vectorized(n::Int)
    x = rand(n)
    y = rand(n)
    count = sum(@. x * x + y * y <= 1.0)
    return 4.0 * count / n
end

n = 10_000_000
pi_est = monte_carlo_pi_vectorized(n)
println("Pi ≈ $pi_est")
