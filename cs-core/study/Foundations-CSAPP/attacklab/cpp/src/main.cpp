#include "mini_attacklab.hpp"

#include <cstdlib>
#include <iostream>
#include <vector>

int main(int argc, char **argv)
{
    std::vector<std::uint8_t> bytes;
    int phase = 0;

    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <phase> <payload_file>\n";
        return 1;
    }

    phase = std::atoi(argv[1]);
    if (!attacklab::load_hex_file(argv[2], bytes)) {
        std::cerr << "could not parse payload file: " << argv[2] << '\n';
        return 1;
    }

    if (!attacklab::validate_phase(phase, bytes)) {
        std::cout << "Phase " << phase << " rejected: " << attacklab::phase_name(phase) << '\n';
        return 1;
    }

    std::cout << "Phase " << phase << " accepted: " << attacklab::phase_name(phase) << '\n';
    return 0;
}
