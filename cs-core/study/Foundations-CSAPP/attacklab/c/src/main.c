#include "mini_attacklab.h"

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    unsigned char bytes[256];
    size_t len = 0;
    int phase;

    if (argc != 3) {
        fprintf(stderr, "Usage: %s <phase> <payload_file>\n", argv[0]);
        return 1;
    }

    phase = atoi(argv[1]);
    if (!load_hex_file(argv[2], bytes, sizeof(bytes), &len)) {
        fprintf(stderr, "could not parse payload file: %s\n", argv[2]);
        return 1;
    }

    if (!attacklab_validate_phase(phase, bytes, len)) {
        printf("Phase %d rejected: %s\n", phase, attacklab_phase_name(phase));
        return 1;
    }

    printf("Phase %d accepted: %s\n", phase, attacklab_phase_name(phase));
    return 0;
}
