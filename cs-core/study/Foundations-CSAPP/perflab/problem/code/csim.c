/*
 * csim.c - Cache simulator starter for Performance Lab.
 */

#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>

#include "cachelab.h"

int main(int argc, char *argv[])
{
    int s = 0;
    int E = 0;
    int b = 0;
    int verbose = 0;
    char *tracefile = NULL;
    int opt;

    while ((opt = getopt(argc, argv, "s:E:b:t:vh")) != -1) {
        switch (opt) {
        case 's':
            s = atoi(optarg);
            break;
        case 'E':
            E = atoi(optarg);
            break;
        case 'b':
            b = atoi(optarg);
            break;
        case 't':
            tracefile = optarg;
            break;
        case 'v':
            verbose = 1;
            break;
        case 'h':
        default:
            fprintf(stderr, "Usage: %s -s <s> -E <E> -b <b> -t <tracefile> [-v]\n", argv[0]);
            return 1;
        }
    }

    if (s <= 0 || E <= 0 || b <= 0 || tracefile == NULL) {
        fprintf(stderr, "Missing required arguments.\n");
        return 1;
    }

    (void)verbose;
    printSummary(0, 0, 0);
    return 0;
}
