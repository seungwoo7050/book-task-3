#include "../include/mini_bomb.h"

#include <stdio.h>

static int failures = 0;

static void expect_true(const char *label, int value)
{
    if (!value) {
        fprintf(stderr, "FAIL: %s\n", label);
        failures += 1;
    }
}

static void expect_false(const char *label, int value)
{
    if (value) {
        fprintf(stderr, "FAIL: %s\n", label);
        failures += 1;
    }
}

int main(void)
{
    expect_true("phase1 exact string", bomb_phase_1("Assembly reveals intent."));
    expect_false("phase1 rejects typo", bomb_phase_1("Assembly reveals intent"));
    expect_false("phase1 rejects null", bomb_phase_1(NULL));

    expect_true("phase2 doubling sequence", bomb_phase_2("1 2 4 8 16 32"));
    expect_false("phase2 wrong seed", bomb_phase_2("0 0 0 0 0 0"));
    expect_false("phase2 wrong recurrence", bomb_phase_2("1 2 4 8 16 31"));

    expect_true("phase3 accepts valid case 1", bomb_phase_3("1 311"));
    expect_true("phase3 accepts valid case 6", bomb_phase_3("6 128"));
    expect_false("phase3 rejects wrong value", bomb_phase_3("1 312"));
    expect_false("phase3 rejects range miss", bomb_phase_3("8 999"));

    expect_true("phase4 accepts target 6", bomb_phase_4("6 6"));
    expect_false("phase4 rejects official-style 7 0", bomb_phase_4("7 0"));
    expect_false("phase4 rejects out of range", bomb_phase_4("15 6"));

    expect_true("phase5 accepts nibble map", bomb_phase_5("01234."));
    expect_false("phase5 rejects wrong nibble", bomb_phase_5("01234/"));
    expect_false("phase5 rejects wrong length", bomb_phase_5("01234"));

    expect_true("phase6 accepts reorder", bomb_phase_6("4 6 2 3 5 1"));
    expect_false("phase6 rejects duplicate", bomb_phase_6("4 6 2 2 5 1"));
    expect_false("phase6 rejects wrong order", bomb_phase_6("1 2 3 4 5 6"));

    expect_true("secret accepts bst path", bomb_secret_phase("35"));
    expect_false("secret rejects another node", bomb_secret_phase("99"));
    expect_false("secret rejects non-number", bomb_secret_phase("thirty-five"));

    if (failures != 0) {
        return 1;
    }

    puts("C mini-bomb tests passed");
    return 0;
}
