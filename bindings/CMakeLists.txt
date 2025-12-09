cmake_minimum_required(VERSION 3.16)
project(backend)

find_package(pybind11 REQUIRED)

pybind11_add_module(backend pybind_module.cpp)
target_include_directories(backend PRIVATE ../backend/include)
