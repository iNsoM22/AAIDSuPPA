#include "similarity.hpp"

#include <cmath>
#include <cstdio>
#include <fstream>
#include <iostream>

int main() {
    const std::vector<float> a{1.0f, 0.0f, 0.0f};
    const std::vector<float> b{0.5f, 0.0f, 0.5f};
    const float cos = similarity::cosine(a, b);
    if (std::fabs(cos - 0.5f) > 1e-6f) {
        std::cerr << "cosine mismatch: " << cos << "\n";
        return 1;
    }

    const std::string path = "test_embeddings.bin";
    {
        std::ofstream out(path, std::ios::binary);
        uint32_t n = 2;
        uint32_t d = 3;
        out.write(reinterpret_cast<const char*>(&n), sizeof(n));
        out.write(reinterpret_cast<const char*>(&d), sizeof(d));
        const std::vector<float> values{1.f, 0.f, 0.f, 0.5f, 0.f, 0.5f};
        out.write(reinterpret_cast<const char*>(values.data()),
                  static_cast<std::streamsize>(values.size() * sizeof(float)));
    }

    uint32_t loaded_n = 0;
    uint32_t loaded_d = 0;
    const auto matrix = similarity::load_embeddings(path, loaded_n, loaded_d);
    if (loaded_n != 2 || loaded_d != 3 || matrix.size() != 2 || matrix[1][2] != 0.5f) {
        std::cerr << "load_embeddings result mismatch\n";
        return 1;
    }

    std::remove(path.c_str());
    return 0;
}
