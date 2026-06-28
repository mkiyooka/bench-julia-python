#include <cstdio>
#include <random>

double monte_carlo_pi(int n) {
    std::mt19937_64 rng(42);
    std::uniform_real_distribution<double> dist(0.0, 1.0);
    int count = 0;
    for (int i = 0; i < n; ++i) {
        double x = dist(rng);
        double y = dist(rng);
        if (x * x + y * y <= 1.0) {
            ++count;
        }
    }
    return 4.0 * count / n;
}

int main() {
    int n = 10'000'000;
    double pi_est = monte_carlo_pi(n);
    std::printf("Pi ≈ %.10f\n", pi_est);
    return 0;
}
