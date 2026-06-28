function monte_carlo_pi(n::Int)
    count = 0
    for _ in 1:n
        x = rand()
        y = rand()
        if x * x + y * y <= 1.0
            count += 1
        end
    end
    return 4.0 * count / n
end

n = 10_000_000
pi_est = monte_carlo_pi(n)
println("Pi ≈ $pi_est")
