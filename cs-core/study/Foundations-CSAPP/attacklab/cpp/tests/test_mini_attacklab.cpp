#include "../include/mini_attacklab.hpp"

#include <iostream>
#include <vector>

namespace {

int failures = 0;

void expect_true(const char *label, bool value)
{
    if (!value) {
        std::cerr << "FAIL: " << label << '\n';
        ++failures;
    }
}

void expect_false(const char *label, bool value)
{
    if (value) {
        std::cerr << "FAIL: " << label << '\n';
        ++failures;
    }
}

}  // 테스트 helper 이름공간 끝

int main()
{
    std::vector<std::uint8_t> bytes;

    expect_true("parser accepts comments", attacklab::parse_hex_string("# phase1\n00 00\n# tail\nc0 17 40 00 00 00 00 00", bytes));
    expect_false("parser rejects odd token", attacklab::parse_hex_string("0", bytes));

    expect_true(
        "phase1 valid",
        attacklab::parse_hex_string(
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "
            "c0 17 40 00 00 00 00 00",
            bytes) &&
            attacklab::phase1(bytes));
    expect_false(
        "phase1 wrong address",
        attacklab::parse_hex_string(
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "
            "c1 17 40 00 00 00 00 00",
            bytes) &&
            attacklab::phase1(bytes));

    expect_true("phase2 valid", attacklab::load_hex_file("data/phase2.txt", bytes) && attacklab::phase2(bytes));
    if (attacklab::load_hex_file("data/phase2.txt", bytes)) {
        bytes[40] ^= 0x01;
        expect_false("phase2 wrong return address", attacklab::phase2(bytes));
    }

    expect_true("phase3 valid", attacklab::load_hex_file("data/phase3.txt", bytes) && attacklab::phase3(bytes));
    if (attacklab::load_hex_file("data/phase3.txt", bytes)) {
        bytes[55] ^= 0x01;
        expect_false("phase3 wrong string", attacklab::phase3(bytes));
    }

    expect_true("phase4 valid", attacklab::load_hex_file("data/phase4.txt", bytes) && attacklab::phase4(bytes));
    if (attacklab::load_hex_file("data/phase4.txt", bytes)) {
        bytes[40] ^= 0x01;
        expect_false("phase4 wrong gadget", attacklab::phase4(bytes));
    }

    expect_true("phase5 valid", attacklab::load_hex_file("data/phase5.txt", bytes) && attacklab::phase5(bytes));
    if (attacklab::load_hex_file("data/phase5.txt", bytes)) {
        bytes[64] ^= 0x08;
        expect_false("phase5 wrong offset", attacklab::phase5(bytes));
    }

    if (failures != 0) {
        return 1;
    }

    std::cout << "C++ mini-attacklab tests passed\n";
    return 0;
}
