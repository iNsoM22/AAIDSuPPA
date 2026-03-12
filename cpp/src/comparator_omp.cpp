#include "comparator_omp.hpp"

#include "similarity.hpp"

#include <omp.h>

namespace comparator {

ResultList run_omp(const EmbeddingMatrix& embeddings,
                   const ComparisonConfig& config) {
    const int n = static_cast<int>(embeddings.size());
    if (n < 2) {
        return {};
    }

    if (config.num_threads > 0) {
        omp_set_num_threads(config.num_threads);
    }

    omp_sched_t sched_kind;
    if (config.schedule == "static") {
        sched_kind = omp_sched_static;
    } else if (config.schedule == "guided") {
        sched_kind = omp_sched_guided;
    } else {
        sched_kind = omp_sched_dynamic;
    }
    omp_set_schedule(sched_kind, config.chunk_size);

    const int max_threads = config.num_threads > 0 ? config.num_threads : omp_get_max_threads();
    std::vector<ResultList> thread_results(max_threads);

#pragma omp parallel for schedule(runtime) default(none) shared(embeddings, config, n, thread_results)
    for (int i = 0; i < n - 1; ++i) {
        const int tid = omp_get_thread_num();
        auto& local = thread_results[tid];
        for (int j = i + 1; j < n; ++j) {
            const float score = similarity::cosine(embeddings[i], embeddings[j]);
            if (score >= config.threshold) {
                local.push_back({
                    static_cast<uint32_t>(i),
                    static_cast<uint32_t>(j),
                    score,
                });
            }
        }
    }

    ResultList results;
    for (auto& partial : thread_results) {
        results.insert(results.end(), partial.begin(), partial.end());
    }
    return results;
}

} // namespace comparator
