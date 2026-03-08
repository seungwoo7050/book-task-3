#include "../include/mini_bomb.hpp"

#include <iostream>
#include <string>

namespace {

int failures = 0;

void expect_true(const std::string &label, bool value)
{
    if (!value) {
        std::cerr << "FAIL: " << label << '\n';
        ++failures;
    }
}

void expect_false(const std::string &label, bool value)
{
    if (value) {
        std::cerr << "FAIL: " << label << '\n';
        ++failures;
    }
}

}  // namespace

int main()
{
    expect_true("phase1 exact string", bomblab::phase1("Assembly reveals intent."));
    expect_false("phase1 rejects typo", bomblab::phase1("Assembly reveals intent"));

    expect_true("phase2 doubling sequence", bomblab::phase2("1 2 4 8 16 32"));
    expect_false("phase2 wrong seed", bomblab::phase2("0 0 0 0 0 0"));
    expect_false("phase2 wrong recurrence", bomblab::phase2("1 2 4 8 16 31"));

    expect_true("phase3 accepts valid case 1", bomblab::phase3("1 311"));
    expect_true("phase3 accepts valid case 6", bomblab::phase3("6 128"));
    expect_false("phase3 rejects wrong value", bomblab::phase3("1 312"));
    expect_false("phase3 rejects range miss", bomblab::phase3("8 999"));

    expect_true("phase4 accepts target 6", bomblab::phase4("6 6"));
    expect_false("phase4 rejects 7 0", bomblab::phase4("7 0"));
    expect_false("phase4 rejects out of range", bomblab::phase4("15 6"));

    expect_true("phase5 accepts nibble map", bomblab::phase5("01234."));
    expect_false("phase5 rejects wrong nibble", bomblab::phase5("01234/"));
    expect_false("phase5 rejects wrong length", bomblab::phase5("01234"));

    expect_true("phase6 accepts reorder", bomblab::phase6("4 6 2 3 5 1"));
    expect_false("phase6 rejects duplicate", bomblab::phase6("4 6 2 2 5 1"));
    expect_false("phase6 rejects wrong order", bomblab::phase6("1 2 3 4 5 6"));

    expect_true("secret accepts bst path", bomblab::secret_phase("35"));
    expect_false("secret rejects another node", bomblab::secret_phase("99"));
    expect_false("secret rejects non-number", bomblab::secret_phase("thirty-five"));

    if (failures != 0) {
        return 1;
    }

    std::cout << "C++ mini-bomb tests passed\n";
    return 0;
}
