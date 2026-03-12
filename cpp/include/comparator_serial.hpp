#pragma once
#include "types.hpp"

namespace comparator {

ResultList run_serial(const EmbeddingMatrix& embeddings,
                      const ComparisonConfig& config);

} // namespace comparator
