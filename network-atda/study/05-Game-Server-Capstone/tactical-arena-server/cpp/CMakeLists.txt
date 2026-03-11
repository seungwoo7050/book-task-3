cmake_minimum_required(VERSION 3.20)

project(tactical_arena_server LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Threads REQUIRED)
find_package(SQLite3 REQUIRED)
find_path(BOOST_INCLUDE_DIR boost/asio.hpp
    HINTS
        /opt/homebrew/include
        /usr/local/include
        /usr/include
)

if(NOT BOOST_INCLUDE_DIR)
    message(FATAL_ERROR "boost/asio.hpp not found")
endif()

add_library(arena_core
    src/protocol.cpp
    src/state.cpp
    src/repository.cpp
)

target_include_directories(arena_core
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
        ${BOOST_INCLUDE_DIR}
)

target_link_libraries(arena_core
    PUBLIC
        SQLite::SQLite3
        Threads::Threads
)

add_executable(arena_server src/arena_server.cpp)
target_link_libraries(arena_server PRIVATE arena_core)

add_executable(arena_bot src/arena_bot.cpp)
target_link_libraries(arena_bot PRIVATE arena_core)

add_executable(arena_loadtest src/arena_loadtest.cpp)
target_link_libraries(arena_loadtest PRIVATE arena_core)

enable_testing()

add_executable(test_protocol tests/test_protocol.cpp)
target_link_libraries(test_protocol PRIVATE arena_core)
add_test(NAME test_protocol COMMAND test_protocol)

add_executable(test_state tests/test_state.cpp)
target_link_libraries(test_state PRIVATE arena_core)
add_test(NAME test_state COMMAND test_state)

add_executable(test_repository tests/test_repository.cpp)
target_link_libraries(test_repository PRIVATE arena_core)
add_test(NAME test_repository COMMAND test_repository)
