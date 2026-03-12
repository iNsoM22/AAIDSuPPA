#include "comparator_omp.hpp"
#include "comparator_serial.hpp"
#include "similarity.hpp"
#include "timer.hpp"

#include <iostream>
#include <sstream>
#include <string>

namespace {

std::string json_escape(const std::string& in) {
    std::string out;
    out.reserve(in.size());
    for (char c : in) {
        switch (c) {
        case '\\': out += "\\\\"; break;
        case '"': out += "\\\""; break;
        case '\n': out += "\\n"; break;
        case '\r': out += "\\r"; break;
        case '\t': out += "\\t"; break;
        default: out += c; break;
        }
    }
    return out;
}

} // namespace

int main(int argc, char* argv[]) {
    std::string mode = "serial";
    std::string input_path;
    ComparisonConfig config;

    for (int i = 1; i < argc; ++i) {
        const std::string arg = argv[i];
        if (arg == "--mode" && i + 1 < argc) mode = argv[++i];
        else if (arg == "--input" && i + 1 < argc) input_path = argv[++i];
        else if (arg == "--threshold" && i + 1 < argc) config.threshold = std::stof(argv[++i]);
        else if (arg == "--threads" && i + 1 < argc) config.num_threads = std::stoi(argv[++i]);
        else if (arg == "--schedule" && i + 1 < argc) config.schedule = argv[++i];
        else if (arg == "--chunk" && i + 1 < argc) config.chunk_size = std::stoi(argv[++i]);
    }

    if (input_path.empty()) {
        std::cerr << "--input is required\n";
        return 2;
    }

    try {
        uint32_t n = 0;
        uint32_t d = 0;
        const auto embeddings = similarity::load_embeddings(input_path, n, d);

        Timer timer;
        timer.start();

        ResultList results;
        if (mode == "omp") {
            results = comparator::run_omp(embeddings, config);
        } else {
            mode = "serial";
            results = comparator::run_serial(embeddings, config);
        }

        const double elapsed = timer.elapsed_ms();
        const uint64_t total_pairs = static_cast<uint64_t>(n) * (n - 1) / 2;

        std::ostringstream out;
        out << "{\n";
        out << "  \"mode\": \"" << json_escape(mode) << "\",\n";
        out << "  \"n_students\": " << n << ",\n";
        out << "  \"embedding_dim\": " << d << ",\n";
        out << "  \"threshold\": " << config.threshold << ",\n";
        out << "  \"elapsed_ms\": " << elapsed << ",\n";
        out << "  \"n_flagged_pairs\": " << results.size() << ",\n";
        out << "  \"total_pairs\": " << total_pairs << ",\n";
        out << "  \"flagged_pairs\": [";

        for (size_t i = 0; i < results.size(); ++i) {
            const auto& r = results[i];
            out << "{\"i\":" << r.student_i << ",\"j\":" << r.student_j << ",\"score\":" << r.score << "}";
            if (i + 1 < results.size()) out << ",";
        }

        out << "]\n";
        out << "}\n";

        std::cout << out.str();
        return 0;
    } catch (const std::exception& ex) {
        std::cerr << ex.what() << "\n";
        return 1;
    }
}
