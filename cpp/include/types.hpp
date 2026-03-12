#pragma once
#include <cstdint>
#include <string>
#include <vector>

struct SimilarityResult {
    uint32_t student_i;
    uint32_t student_j;
    float score;
};

struct ComparisonConfig {
    float threshold = 0.85f;
    int num_threads = 0;
    std::string schedule = "dynamic";
    int chunk_size = 32;
};

using EmbeddingMatrix = std::vector<std::vector<float>>;
using ResultList = std::vector<SimilarityResult>;
