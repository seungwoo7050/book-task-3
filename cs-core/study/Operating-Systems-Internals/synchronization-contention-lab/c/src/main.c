#include "contention_lab.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void usage(const char *program) {
    fprintf(stderr, "usage: %s --scenario <counter|gate|buffer> --threads <n> --iterations <n>\n", program);
}

int main(int argc, char **argv) {
    const char *scenario = NULL;
    int threads = 0;
    int iterations = 0;

    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--scenario") == 0 && i + 1 < argc) {
            scenario = argv[++i];
        } else if (strcmp(argv[i], "--threads") == 0 && i + 1 < argc) {
            threads = atoi(argv[++i]);
        } else if (strcmp(argv[i], "--iterations") == 0 && i + 1 < argc) {
            iterations = atoi(argv[++i]);
        } else {
            usage(argv[0]);
            return 1;
        }
    }

    if (scenario == NULL || threads <= 0 || iterations <= 0) {
        usage(argv[0]);
        return 1;
    }

    lab_metrics_t metrics;
    int rc = 1;
    if (strcmp(scenario, "counter") == 0) {
        rc = run_counter_scenario(threads, iterations, &metrics);
    } else if (strcmp(scenario, "gate") == 0) {
        rc = run_gate_scenario(threads, iterations, &metrics);
    } else if (strcmp(scenario, "buffer") == 0) {
        rc = run_buffer_scenario(threads, iterations, &metrics);
    } else {
        usage(argv[0]);
        return 1;
    }
    print_metrics(&metrics);
    return rc;
}
