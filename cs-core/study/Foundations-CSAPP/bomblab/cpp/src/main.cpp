#include "mini_bomb.hpp"

#include <fstream>
#include <iostream>
#include <string>

namespace {

bool validate_phase(int phase, const std::string &input)
{
    switch (phase) {
    case 1:
        return bomblab::phase1(input);
    case 2:
        return bomblab::phase2(input);
    case 3:
        return bomblab::phase3(input);
    case 4:
        return bomblab::phase4(input);
    case 5:
        return bomblab::phase5(input);
    case 6:
        return bomblab::phase6(input);
    default:
        return false;
    }
}

}  // 내부 helper 이름공간 끝

int main(int argc, char **argv)
{
    std::ifstream file;
    std::istream *input = &std::cin;
    std::string line;

    if (argc == 2) {
        file.open(argv[1]);
        if (!file) {
            std::cerr << "could not open " << argv[1] << '\n';
            return 1;
        }
        input = &file;
    } else if (argc > 2) {
        std::cerr << "Usage: " << argv[0] << " [input_file]\n";
        return 1;
    }

    std::cout << "Welcome to the study mini bomb. Solve six phases carefully.\n";

    for (int phase = 1; phase <= 6; ++phase) {
        if (!std::getline(*input, line) || !validate_phase(phase, line)) {
            std::cout << "BOOM!!!\n";
            return 1;
        }
        std::cout << "Phase " << phase << " defused.\n";
    }

    if (std::getline(*input, line) && !line.empty()) {
        if (!bomblab::secret_phase(line)) {
            std::cout << "BOOM!!!\n";
            return 1;
        }
        std::cout << "Secret phase defused.\n";
    }

    std::cout << "Bomb defused.\n";
    return 0;
}
