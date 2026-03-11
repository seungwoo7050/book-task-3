#ifndef MINI_ATTACKLAB_HPP
#define MINI_ATTACKLAB_HPP

#include <cstddef>
#include <cstdint>
#include <string_view>
#include <vector>

namespace attacklab {

bool parse_hex_string(std::string_view text, std::vector<std::uint8_t> &bytes);
bool load_hex_file(const char *path, std::vector<std::uint8_t> &bytes);

bool phase1(const std::vector<std::uint8_t> &bytes);
bool phase2(const std::vector<std::uint8_t> &bytes);
bool phase3(const std::vector<std::uint8_t> &bytes);
bool phase4(const std::vector<std::uint8_t> &bytes);
bool phase5(const std::vector<std::uint8_t> &bytes);
bool validate_phase(int phase, const std::vector<std::uint8_t> &bytes);
const char *phase_name(int phase);

}  // attacklab 이름공간 끝

#endif
