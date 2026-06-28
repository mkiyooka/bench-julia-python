cmake_minimum_required(VERSION 3.20)
project(bench LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

foreach(target monte_carlo_pi nbody simpson rule110)
    add_executable(${target} src/${target}.cpp)
endforeach()
