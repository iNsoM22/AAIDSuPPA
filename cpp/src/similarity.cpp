#include "similarity.hpp"

#include <fstream>
#include <stdexcept>

namespace similarity {

float cosine(const std::vector<float>& a, const std::vector<float>& b) {
    if (a.size() != b.size()) {
        throw std::invalid_argument("cosine: vector dimension mismatch");
    }

    float dot = 0.0f;
    for (size_t i = 0; i < a.size(); ++i) {
        dot += a[i] * b[i];
    }
    return dot;
}

EmbeddingMatrix load_embeddings(const std::string& path,
                                uint32_t& out_n,
                                uint32_t& out_d) {
    std::ifstream in(path, std::ios::binary);
    if (!in) {
        throw std::runtime_error("Failed to open embedding file: " + path);
    }

    in.read(reinterpret_cast<char*>(&out_n), sizeof(uint32_t));
    in.read(reinterpret_cast<char*>(&out_d), sizeof(uint32_t));
    if (!in || out_d == 0) {
        throw std::runtime_error("Invalid embedding header");
    }

    EmbeddingMatrix embeddings(out_n, std::vector<float>(out_d));
    for (uint32_t i = 0; i < out_n; ++i) {
        in.read(reinterpret_cast<char*>(embeddings[i].data()),
                static_cast<std::streamsize>(out_d * sizeof(float)));
        if (!in) {
            throw std::runtime_error("Unexpected EOF while reading embeddings");
        }
    }

    return embeddings;
}

} // namespace similarity
