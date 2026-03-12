#include "comparator_serial.hpp"

#include "similarity.hpp"

namespace comparator {

ResultList run_serial(const EmbeddingMatrix& embeddings,
                      const ComparisonConfig& config) {
    const size_t n = embeddings.size();
    ResultList results;
    results.reserve(n / 10);

    for (size_t i = 0; i + 1 < n; ++i) {
        for (size_t j = i + 1; j < n; ++j) {
            const float score = similarity::cosine(embeddings[i], embeddings[j]);
            if (score >= config.threshold) {
                results.push_back({
                    static_cast<uint32_t>(i),
                    static_cast<uint32_t>(j),
                    score,
                });
            }
        }
    }

    return results;
}

} // namespace comparator
