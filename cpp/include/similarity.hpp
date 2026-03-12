#pragma once
#include "types.hpp"
#include <string>

namespace similarity {

float cosine(const std::vector<float>& a, const std::vector<float>& b);

EmbeddingMatrix load_embeddings(const std::string& path,
                                uint32_t& out_n,
                                uint32_t& out_d);

} // namespace similarity
