#include "mini_attacklab.hpp"

#include <array>
#include <cctype>
#include <cstdint>
#include <fstream>
#include <iterator>
#include <sstream>
#include <string>

namespace attacklab {
namespace {

constexpr std::size_t kBufferSize = 40;
constexpr std::uint64_t kTouch1 = 0x4017c0ULL;
constexpr std::uint64_t kTouch2 = 0x4017ecULL;
constexpr std::uint64_t kTouch3 = 0x4018faULL;
constexpr std::uint64_t kBufferStart = 0x5561dc78ULL;
constexpr std::uint64_t kGadgetPopRax = 0x4019ccULL;
constexpr std::uint64_t kGadgetMovRaxRdi = 0x4019a2ULL;
constexpr std::uint64_t kGadgetMovRspRax = 0x4019d0ULL;
constexpr std::uint64_t kGadgetPopRsi = 0x401a10ULL;
constexpr std::uint64_t kGadgetLeaRdiRsiRax = 0x401a20ULL;
constexpr std::uint64_t kCookie = 0x1a2b3c4dULL;
constexpr std::array<std::uint8_t, 9> kCookieAscii = {'1', 'a', '2', 'b', '3', 'c', '4', 'd', '\0'};

int hex_value(char ch)
{
    if ('0' <= ch && ch <= '9') {
        return ch - '0';
    }
    if ('a' <= ch && ch <= 'f') {
        return ch - 'a' + 10;
    }
    if ('A' <= ch && ch <= 'F') {
        return ch - 'A' + 10;
    }
    return -1;
}

std::uint64_t read_u64_le(const std::vector<std::uint8_t> &bytes, std::size_t offset)
{
    std::uint64_t value = 0;

    for (int index = 7; index >= 0; --index) {
        value = (value << 8) | bytes[offset + static_cast<std::size_t>(index)];
    }
    return value;
}

bool matches_u64_le(const std::vector<std::uint8_t> &bytes, std::size_t offset, std::uint64_t expected)
{
    return read_u64_le(bytes, offset) == expected;
}

bool prefix_matches(const std::vector<std::uint8_t> &bytes, std::initializer_list<std::uint8_t> prefix)
{
    if (bytes.size() < prefix.size()) {
        return false;
    }
    return std::equal(prefix.begin(), prefix.end(), bytes.begin());
}

bool tail_matches(const std::vector<std::uint8_t> &bytes, std::size_t offset, const std::array<std::uint8_t, 9> &tail)
{
    if (offset + tail.size() > bytes.size()) {
        return false;
    }
    return std::equal(tail.begin(), tail.end(), bytes.begin() + static_cast<std::ptrdiff_t>(offset));
}

}  // 내부 helper 이름공간 끝

bool parse_hex_string(std::string_view text, std::vector<std::uint8_t> &bytes)
{
    bytes.clear();

    for (std::size_t index = 0; index < text.size();) {
        while (index < text.size() && std::isspace(static_cast<unsigned char>(text[index]))) {
            ++index;
        }
        if (index >= text.size()) {
            break;
        }
        if (text[index] == '#') {
            while (index < text.size() && text[index] != '\n') {
                ++index;
            }
            continue;
        }
        if (index + 1 >= text.size()) {
            return false;
        }

        const int high = hex_value(text[index]);
        const int low = hex_value(text[index + 1]);
        if (high < 0 || low < 0) {
            return false;
        }
        bytes.push_back(static_cast<std::uint8_t>((high << 4) | low));
        index += 2;

        if (index < text.size() && !std::isspace(static_cast<unsigned char>(text[index])) && text[index] != '#') {
            return false;
        }
    }

    return true;
}

bool load_hex_file(const char *path, std::vector<std::uint8_t> &bytes)
{
    std::ifstream file(path);
    std::string text;

    if (!file) {
        return false;
    }
    text.assign(std::istreambuf_iterator<char>(file), std::istreambuf_iterator<char>());
    return parse_hex_string(text, bytes);
}

bool phase1(const std::vector<std::uint8_t> &bytes)
{
    return bytes.size() == 48 && matches_u64_le(bytes, kBufferSize, kTouch1);
}

bool phase2(const std::vector<std::uint8_t> &bytes)
{
    return bytes.size() == 48 &&
           prefix_matches(bytes, {0x48, 0xc7, 0xc7, 0x4d, 0x3c, 0x2b, 0x1a, 0x68, 0xec, 0x17, 0x40, 0x00, 0xc3}) &&
           matches_u64_le(bytes, kBufferSize, kBufferStart);
}

bool phase3(const std::vector<std::uint8_t> &bytes)
{
    return bytes.size() == 57 &&
           prefix_matches(bytes, {0x48, 0xc7, 0xc7, 0xa8, 0xdc, 0x61, 0x55, 0x68, 0xfa, 0x18, 0x40, 0x00, 0xc3}) &&
           matches_u64_le(bytes, kBufferSize, kBufferStart) &&
           tail_matches(bytes, 48, kCookieAscii);
}

bool phase4(const std::vector<std::uint8_t> &bytes)
{
    return bytes.size() == 72 &&
           matches_u64_le(bytes, 40, kGadgetPopRax) &&
           matches_u64_le(bytes, 48, kCookie) &&
           matches_u64_le(bytes, 56, kGadgetMovRaxRdi) &&
           matches_u64_le(bytes, 64, kTouch2);
}

bool phase5(const std::vector<std::uint8_t> &bytes)
{
    return bytes.size() == 105 &&
           matches_u64_le(bytes, 40, kGadgetMovRspRax) &&
           matches_u64_le(bytes, 48, kGadgetMovRaxRdi) &&
           matches_u64_le(bytes, 56, kGadgetPopRsi) &&
           matches_u64_le(bytes, 64, 48ULL) &&
           matches_u64_le(bytes, 72, kGadgetLeaRdiRsiRax) &&
           matches_u64_le(bytes, 80, kGadgetMovRaxRdi) &&
           matches_u64_le(bytes, 88, kTouch3) &&
           tail_matches(bytes, 96, kCookieAscii);
}

bool validate_phase(int phase, const std::vector<std::uint8_t> &bytes)
{
    switch (phase) {
    case 1:
        return phase1(bytes);
    case 2:
        return phase2(bytes);
    case 3:
        return phase3(bytes);
    case 4:
        return phase4(bytes);
    case 5:
        return phase5(bytes);
    default:
        return false;
    }
}

const char *phase_name(int phase)
{
    switch (phase) {
    case 1:
        return "return-address overwrite";
    case 2:
        return "code injection with cookie register setup";
    case 3:
        return "code injection with cookie string placement";
    case 4:
        return "ROP chain for touch2";
    case 5:
        return "ROP chain for touch3 with relative string addressing";
    default:
        return "unknown";
    }
}

}  // attacklab 이름공간 끝
