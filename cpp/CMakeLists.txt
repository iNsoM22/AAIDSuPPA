cmake_minimum_required(VERSION 3.20)
project(academic_integrity_engine CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

set(CMAKE_CXX_FLAGS_RELEASE "-O3 -march=native -DNDEBUG")
set(CMAKE_CXX_FLAGS_DEBUG   "-g -O0 -fsanitize=address")

find_package(OpenMP REQUIRED)

add_library(engine_lib
    src/similarity.cpp
    src/comparator_serial.cpp
    src/comparator_omp.cpp
)
target_include_directories(engine_lib PUBLIC include/)
target_link_libraries(engine_lib PUBLIC OpenMP::OpenMP_CXX)

add_executable(engine src/main.cpp)
target_link_libraries(engine PRIVATE engine_lib)

enable_testing()
add_subdirectory(tests)
