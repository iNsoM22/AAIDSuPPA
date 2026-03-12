#pragma once
#include "types.hpp"

namespace comparator {

ResultList run_omp(const EmbeddingMatrix& embeddings,
                   const ComparisonConfig& config);

} // namespace comparator
