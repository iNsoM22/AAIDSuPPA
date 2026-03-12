#pragma once
#include <chrono>

class Timer {
    using clock = std::chrono::high_resolution_clock;
    clock::time_point start_;

public:
    void start() { start_ = clock::now(); }

    double elapsed_ms() const {
        auto end = clock::now();
        return std::chrono::duration<double, std::milli>(end - start_).count();
    }
};
