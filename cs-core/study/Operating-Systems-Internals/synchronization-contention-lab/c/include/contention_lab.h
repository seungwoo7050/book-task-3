#ifndef CONTENTION_LAB_H
#define CONTENTION_LAB_H

typedef struct lab_metrics {
    const char *scenario;
    int ok;
    long elapsed_ms;
    long wait_events;
    long final_count;
    long expected_count;
    int max_concurrency;
    int permit_limit;
    long produced;
    long consumed;
    int max_occupancy;
    int capacity;
    int underflow;
    int overflow;
} lab_metrics_t;

int run_counter_scenario(int threads, int iterations, lab_metrics_t *metrics);
int run_gate_scenario(int threads, int iterations, lab_metrics_t *metrics);
int run_buffer_scenario(int threads, int iterations, lab_metrics_t *metrics);
void print_metrics(const lab_metrics_t *metrics);

#endif
