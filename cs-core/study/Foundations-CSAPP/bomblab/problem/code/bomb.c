/*
 * High-level skeleton of the official Bomb Lab program.
 *
 * This file is a shape reference only. It is not the runnable course bomb.
 * The real phase implementations live inside the external course binary.
 */

#include <stdio.h>
#include <stdlib.h>

void initialize_bomb(void);
char *read_line(void);
void phase_1(const char *input);
void phase_2(const char *input);
void phase_3(const char *input);
void phase_4(const char *input);
void phase_5(const char *input);
void phase_6(const char *input);
void secret_phase(void);

int main(int argc, char *argv[])
{
    FILE *infile;
    char *input;

    if (argc == 1) {
        infile = stdin;
    } else if (argc == 2) {
        infile = fopen(argv[1], "r");
        if (!infile) {
            fprintf(stderr, "%s: could not open %s\n", argv[0], argv[1]);
            exit(8);
        }
    } else {
        fprintf(stderr, "Usage: %s [input_file]\n", argv[0]);
        exit(8);
    }

    (void)infile;
    initialize_bomb();

    input = read_line();
    phase_1(input);
    input = read_line();
    phase_2(input);
    input = read_line();
    phase_3(input);
    input = read_line();
    phase_4(input);
    input = read_line();
    phase_5(input);
    input = read_line();
    phase_6(input);

    return 0;
}
