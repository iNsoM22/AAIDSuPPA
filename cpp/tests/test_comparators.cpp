#include "comparator_omp.hpp"
#include "comparator_serial.hpp"

#include <algorithm>
#include <iostream>

namespace {

void sort_results(ResultList& results) {
    std::sort(results.begin(), results.end(), [](const auto& lhs, const auto& rhs) {
        if (lhs.student_i != rhs.student_i) return lhs.student_i < rhs.student_i;
        if (lhs.student_j != rhs.student_j) return lhs.student_j < rhs.student_j;
        return lhs.score < rhs.score;
    });
}

} // namespace

int main() {
    EmbeddingMatrix embeddings{
        {1.0f, 0.0f},
        {0.99f, 0.01f},
        {0.0f, 1.0f},
    };

    ComparisonConfig cfg;
    cfg.threshold = 0.95f;
    cfg.num_threads = 2;

    auto serial = comparator::run_serial(embeddings, cfg);
    auto omp = comparator::run_omp(embeddings, cfg);

    sort_results(serial);
    sort_results(omp);

    if (serial.size() != 1 || omp.size() != 1) {
        std::cerr << "Expected exactly one flagged pair\n";
        return 1;
    }

    if (serial[0].student_i != omp[0].student_i ||
        serial[0].student_j != omp[0].student_j) {
        std::cerr << "Serial and OMP pair mismatch\n";
        return 1;
    }

    return 0;
}
