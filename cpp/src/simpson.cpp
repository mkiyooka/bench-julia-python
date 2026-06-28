#include <cstdio>

double simpson(int n) {
    double h = 1.0 / n;
    double s = 4.0 / (1.0 + 0.0 * 0.0) + 4.0 / (1.0 + 1.0 * 1.0);
    for (int i = 1; i < n; ++i) {
        double x = i * h;
        if (i % 2 == 0) {
            s += 2.0 * 4.0 / (1.0 + x * x);
        } else {
            s += 4.0 * 4.0 / (1.0 + x * x);
        }
    }
    return s * h / 3.0;
}

int main() {
    int n = 100'000'000;
    double pi_est = simpson(n);
    std::printf("Pi ≈ %.10f\n", pi_est);
    return 0;
}
