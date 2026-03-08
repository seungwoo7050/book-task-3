#include "mini_bomb.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int read_line(FILE *input, char *buffer, size_t size)
{
    size_t length;

    if (fgets(buffer, (int)size, input) == NULL) {
        return 0;
    }
    length = strcspn(buffer, "\r\n");
    buffer[length] = '\0';
    return 1;
}

static int validate_phase(int phase, const char *input)
{
    switch (phase) {
    case 1:
        return bomb_phase_1(input);
    case 2:
        return bomb_phase_2(input);
    case 3:
        return bomb_phase_3(input);
    case 4:
        return bomb_phase_4(input);
    case 5:
        return bomb_phase_5(input);
    case 6:
        return bomb_phase_6(input);
    default:
        return 0;
    }
}

int main(int argc, char **argv)
{
    FILE *input = stdin;
    char line[128];
    int phase;

    if (argc == 2) {
        input = fopen(argv[1], "r");
        if (input == NULL) {
            fprintf(stderr, "could not open %s\n", argv[1]);
            return 1;
        }
    } else if (argc > 2) {
        fprintf(stderr, "Usage: %s [input_file]\n", argv[0]);
        return 1;
    }

    puts("Welcome to the study mini bomb. Solve six phases carefully.");

    for (phase = 1; phase <= 6; ++phase) {
        if (!read_line(input, line, sizeof(line)) || !validate_phase(phase, line)) {
            puts("BOOM!!!");
            if (input != stdin) {
                fclose(input);
            }
            return 1;
        }
        printf("Phase %d defused.\n", phase);
    }

    if (read_line(input, line, sizeof(line)) && line[0] != '\0') {
        if (!bomb_secret_phase(line)) {
            puts("BOOM!!!");
            if (input != stdin) {
                fclose(input);
            }
            return 1;
        }
        puts("Secret phase defused.");
    }

    puts("Bomb defused.");

    if (input != stdin) {
        fclose(input);
    }
    return 0;
}
