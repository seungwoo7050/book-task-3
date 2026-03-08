#include "../include/mini_attacklab.h"

#include <stdio.h>
#include <string.h>

static int failures = 0;

static void expect_true(const char *label, int value)
{
    if (!value) {
        fprintf(stderr, "FAIL: %s\n", label);
        ++failures;
    }
}

static void expect_false(const char *label, int value)
{
    if (value) {
        fprintf(stderr, "FAIL: %s\n", label);
        ++failures;
    }
}

static int parse(const char *text, unsigned char *bytes, size_t *len)
{
    return parse_hex_string(text, bytes, 256, len);
}

int main(void)
{
    unsigned char bytes[256];
    size_t len = 0;

    expect_true("parser accepts comments",
                parse("# phase1\n00 00\n# tail\nc0 17 40 00 00 00 00 00", bytes, &len));
    expect_false("parser rejects odd token", parse("0", bytes, &len));

    expect_true(
        "phase1 valid",
        parse("00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "
              "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "
              "c0 17 40 00 00 00 00 00",
              bytes,
              &len) &&
            attacklab_phase_1(bytes, len));
    expect_false(
        "phase1 wrong address",
        parse("00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "
              "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "
              "c1 17 40 00 00 00 00 00",
              bytes,
              &len) &&
            attacklab_phase_1(bytes, len));

    expect_true("phase2 valid", load_hex_file("data/phase2.txt", bytes, sizeof(bytes), &len) && attacklab_phase_2(bytes, len));
    if (load_hex_file("data/phase2.txt", bytes, sizeof(bytes), &len)) {
        bytes[40] ^= 0x01;
        expect_false("phase2 wrong return address", attacklab_phase_2(bytes, len));
    }

    expect_true("phase3 valid", load_hex_file("data/phase3.txt", bytes, sizeof(bytes), &len) && attacklab_phase_3(bytes, len));
    if (load_hex_file("data/phase3.txt", bytes, sizeof(bytes), &len)) {
        bytes[55] ^= 0x01;
        expect_false("phase3 wrong string", attacklab_phase_3(bytes, len));
    }

    expect_true("phase4 valid", load_hex_file("data/phase4.txt", bytes, sizeof(bytes), &len) && attacklab_phase_4(bytes, len));
    if (load_hex_file("data/phase4.txt", bytes, sizeof(bytes), &len)) {
        bytes[40] ^= 0x01;
        expect_false("phase4 wrong gadget", attacklab_phase_4(bytes, len));
    }

    expect_true("phase5 valid", load_hex_file("data/phase5.txt", bytes, sizeof(bytes), &len) && attacklab_phase_5(bytes, len));
    if (load_hex_file("data/phase5.txt", bytes, sizeof(bytes), &len)) {
        bytes[64] ^= 0x08;
        expect_false("phase5 wrong offset", attacklab_phase_5(bytes, len));
    }

    if (failures != 0) {
        return 1;
    }

    puts("C mini-attacklab tests passed");
    return 0;
}
