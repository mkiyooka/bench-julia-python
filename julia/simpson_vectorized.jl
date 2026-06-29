function simpson_vectorized(n::Int)
    h = 1.0 / n
    x = collect(1:(n - 1)) .* h
    coeffs = ifelse.(isodd.(1:(n - 1)), 4.0, 2.0)
    s = sum(coeffs .* 4.0 ./ (1.0 .+ x .* x))
    s += 4.0 / (1.0 + 0.0 * 0.0) + 4.0 / (1.0 + 1.0 * 1.0)
    return s * h / 3.0
end

n = 50_000_000
pi_est = simpson_vectorized(n)
println("Pi ≈ $pi_est")
