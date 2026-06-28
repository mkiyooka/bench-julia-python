#include <cstdio>
#include <vector>

int main() {
    const int width = 10'000;
    const int generations = 50'000;
    const int rule[8] = {0, 1, 1, 1, 0, 1, 1, 0};

    std::vector<int> current(width, 0);
    std::vector<int> next(width, 0);
    current[width - 1] = 1;

    for (int g = 0; g < generations; ++g) {
        for (int i = 0; i < width; ++i) {
            int left = i > 0 ? current[i - 1] : 0;
            int center = current[i];
            int right = i < width - 1 ? current[i + 1] : 0;
            int index = left * 4 + center * 2 + right;
            next[i] = rule[index];
        }
        std::swap(current, next);
    }

    int count = 0;
    for (int i = 0; i < width; ++i) {
        count += current[i];
    }
    std::printf("Population: %d\n", count);
    return 0;
}
