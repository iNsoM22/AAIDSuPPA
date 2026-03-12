#!/usr/bin/env bash
set -euo pipefail

BUILD_DIR="cpp/build"
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

cmake .. -DCMAKE_BUILD_TYPE=Release
make -j"$(nproc)"

echo "Build complete. Engine binary at: $BUILD_DIR/engine"
