#include "contention_lab.h"

#include <errno.h>
#include <fcntl.h>
#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>

typedef struct {
    pthread_mutex_t lock;
    long counter;
    long wait_events;
    int iterations;
} counter_state_t;

typedef struct {
    sem_t *sem;
    char sem_name[64];
    pthread_mutex_t lock;
    long wait_events;
    long passes;
    int current_inside;
    int max_concurrency;
    int permit_limit;
    int iterations;
} gate_state_t;

typedef struct {
    pthread_mutex_t lock;
    pthread_cond_t not_empty;
    pthread_cond_t not_full;
    int buffer_count;
    int capacity;
    int producers;
    int total_items;
    long produced;
    long consumed;
    long wait_events;
    int max_occupancy;
    int underflow;
    int overflow;
} buffer_state_t;

typedef struct {
    counter_state_t *state;
} counter_arg_t;

typedef struct {
    gate_state_t *state;
} gate_arg_t;

typedef struct {
    buffer_state_t *state;
    int is_producer;
    int iterations;
} buffer_arg_t;

static long elapsed_ms(struct timespec start, struct timespec end) {
    long seconds = end.tv_sec - start.tv_sec;
    long nanos = end.tv_nsec - start.tv_nsec;
    return seconds * 1000 + nanos / 1000000;
}

static void *counter_worker(void *raw_arg) {
    counter_arg_t *arg = (counter_arg_t *)raw_arg;
    for (int i = 0; i < arg->state->iterations; i++) {
        if (pthread_mutex_trylock(&arg->state->lock) != 0) {
            __sync_fetch_and_add(&arg->state->wait_events, 1);
            pthread_mutex_lock(&arg->state->lock);
        }
        arg->state->counter += 1;
        pthread_mutex_unlock(&arg->state->lock);
    }
    return NULL;
}

static void *gate_worker(void *raw_arg) {
    gate_arg_t *arg = (gate_arg_t *)raw_arg;
    for (int i = 0; i < arg->state->iterations; i++) {
        if (sem_trywait(arg->state->sem) != 0) {
            if (errno == EAGAIN) {
                __sync_fetch_and_add(&arg->state->wait_events, 1);
            }
            sem_wait(arg->state->sem);
        }
        pthread_mutex_lock(&arg->state->lock);
        arg->state->current_inside += 1;
        if (arg->state->current_inside > arg->state->max_concurrency) {
            arg->state->max_concurrency = arg->state->current_inside;
        }
        pthread_mutex_unlock(&arg->state->lock);

        for (volatile int spin = 0; spin < 100; spin++) {
        }

        pthread_mutex_lock(&arg->state->lock);
        arg->state->current_inside -= 1;
        arg->state->passes += 1;
        pthread_mutex_unlock(&arg->state->lock);
        sem_post(arg->state->sem);
    }
    return NULL;
}

static void *buffer_worker(void *raw_arg) {
    buffer_arg_t *arg = (buffer_arg_t *)raw_arg;
    buffer_state_t *state = arg->state;

    if (arg->is_producer) {
        for (int i = 0; i < arg->iterations; i++) {
            pthread_mutex_lock(&state->lock);
            while (state->buffer_count == state->capacity) {
                state->wait_events += 1;
                pthread_cond_wait(&state->not_full, &state->lock);
            }
            state->buffer_count += 1;
            state->produced += 1;
            if (state->buffer_count > state->max_occupancy) {
                state->max_occupancy = state->buffer_count;
            }
            if (state->buffer_count > state->capacity) {
                state->overflow = 1;
            }
            pthread_cond_signal(&state->not_empty);
            pthread_mutex_unlock(&state->lock);
        }
        return NULL;
    }

    while (1) {
        pthread_mutex_lock(&state->lock);
        while (state->buffer_count == 0 && state->consumed < state->total_items) {
            if (state->produced >= state->total_items) {
                break;
            }
            state->wait_events += 1;
            pthread_cond_wait(&state->not_empty, &state->lock);
        }
        if (state->consumed >= state->total_items) {
            pthread_mutex_unlock(&state->lock);
            break;
        }
        if (state->buffer_count == 0) {
            pthread_mutex_unlock(&state->lock);
            continue;
        }
        state->buffer_count -= 1;
        if (state->buffer_count < 0) {
            state->underflow = 1;
        }
        state->consumed += 1;
        pthread_cond_signal(&state->not_full);
        pthread_mutex_unlock(&state->lock);
    }
    return NULL;
}

int run_counter_scenario(int threads, int iterations, lab_metrics_t *metrics) {
    memset(metrics, 0, sizeof(*metrics));
    metrics->scenario = "counter";
    metrics->expected_count = (long)threads * (long)iterations;

    counter_state_t state;
    pthread_mutex_init(&state.lock, NULL);
    state.counter = 0;
    state.wait_events = 0;
    state.iterations = iterations;

    pthread_t *workers = calloc((size_t)threads, sizeof(pthread_t));
    counter_arg_t arg = {.state = &state};
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int i = 0; i < threads; i++) {
        pthread_create(&workers[i], NULL, counter_worker, &arg);
    }
    for (int i = 0; i < threads; i++) {
        pthread_join(workers[i], NULL);
    }
    clock_gettime(CLOCK_MONOTONIC, &end);

    metrics->elapsed_ms = elapsed_ms(start, end);
    metrics->wait_events = state.wait_events;
    metrics->final_count = state.counter;
    metrics->ok = (state.counter == metrics->expected_count);

    free(workers);
    pthread_mutex_destroy(&state.lock);
    return metrics->ok ? 0 : 1;
}

int run_gate_scenario(int threads, int iterations, lab_metrics_t *metrics) {
    memset(metrics, 0, sizeof(*metrics));
    metrics->scenario = "gate";
    metrics->permit_limit = threads >= 4 ? threads / 4 : 1;
    metrics->expected_count = (long)threads * (long)iterations;

    gate_state_t state;
    memset(&state, 0, sizeof(state));
    pthread_mutex_init(&state.lock, NULL);
    state.iterations = iterations;
    state.permit_limit = metrics->permit_limit;
    snprintf(state.sem_name, sizeof(state.sem_name), "/contention-gate-%d", (int)getpid());
    sem_unlink(state.sem_name);
    state.sem = sem_open(state.sem_name, O_CREAT | O_EXCL, 0600, (unsigned int)state.permit_limit);
    if (state.sem == SEM_FAILED) {
        perror("sem_open");
        pthread_mutex_destroy(&state.lock);
        return 1;
    }
    sem_unlink(state.sem_name);

    pthread_t *workers = calloc((size_t)threads, sizeof(pthread_t));
    gate_arg_t arg = {.state = &state};
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int i = 0; i < threads; i++) {
        pthread_create(&workers[i], NULL, gate_worker, &arg);
    }
    for (int i = 0; i < threads; i++) {
        pthread_join(workers[i], NULL);
    }
    clock_gettime(CLOCK_MONOTONIC, &end);

    metrics->elapsed_ms = elapsed_ms(start, end);
    metrics->wait_events = state.wait_events;
    metrics->final_count = state.passes;
    metrics->max_concurrency = state.max_concurrency;
    metrics->ok = (state.passes == metrics->expected_count && state.max_concurrency <= state.permit_limit);

    free(workers);
    sem_close(state.sem);
    pthread_mutex_destroy(&state.lock);
    return metrics->ok ? 0 : 1;
}

int run_buffer_scenario(int threads, int iterations, lab_metrics_t *metrics) {
    memset(metrics, 0, sizeof(*metrics));
    metrics->scenario = "buffer";
    metrics->capacity = 8;

    int producers = threads / 2;
    int consumers = threads - producers;
    if (producers == 0 || consumers == 0) {
        return 1;
    }

    buffer_state_t state;
    memset(&state, 0, sizeof(state));
    pthread_mutex_init(&state.lock, NULL);
    pthread_cond_init(&state.not_empty, NULL);
    pthread_cond_init(&state.not_full, NULL);
    state.capacity = metrics->capacity;
    state.producers = producers;
    state.total_items = producers * iterations;

    pthread_t *workers = calloc((size_t)threads, sizeof(pthread_t));
    buffer_arg_t *args = calloc((size_t)threads, sizeof(buffer_arg_t));
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int i = 0; i < producers; i++) {
        args[i].state = &state;
        args[i].is_producer = 1;
        args[i].iterations = iterations;
        pthread_create(&workers[i], NULL, buffer_worker, &args[i]);
    }
    for (int i = producers; i < threads; i++) {
        args[i].state = &state;
        args[i].is_producer = 0;
        args[i].iterations = iterations;
        pthread_create(&workers[i], NULL, buffer_worker, &args[i]);
    }
    for (int i = 0; i < producers; i++) {
        pthread_join(workers[i], NULL);
    }
    pthread_mutex_lock(&state.lock);
    pthread_cond_broadcast(&state.not_empty);
    pthread_mutex_unlock(&state.lock);
    for (int i = producers; i < threads; i++) {
        pthread_join(workers[i], NULL);
    }
    clock_gettime(CLOCK_MONOTONIC, &end);

    metrics->elapsed_ms = elapsed_ms(start, end);
    metrics->wait_events = state.wait_events;
    metrics->produced = state.produced;
    metrics->consumed = state.consumed;
    metrics->max_occupancy = state.max_occupancy;
    metrics->underflow = state.underflow;
    metrics->overflow = state.overflow;
    metrics->ok = (state.produced == state.total_items &&
                   state.consumed == state.total_items &&
                   state.buffer_count == 0 &&
                   !state.underflow &&
                   !state.overflow);

    free(workers);
    free(args);
    pthread_mutex_destroy(&state.lock);
    pthread_cond_destroy(&state.not_empty);
    pthread_cond_destroy(&state.not_full);
    return metrics->ok ? 0 : 1;
}

void print_metrics(const lab_metrics_t *metrics) {
    printf("scenario=%s\n", metrics->scenario);
    printf("ok=%d\n", metrics->ok);
    printf("elapsed_ms=%ld\n", metrics->elapsed_ms);
    printf("wait_events=%ld\n", metrics->wait_events);
    printf("final_count=%ld\n", metrics->final_count);
    printf("expected_count=%ld\n", metrics->expected_count);
    printf("max_concurrency=%d\n", metrics->max_concurrency);
    printf("permit_limit=%d\n", metrics->permit_limit);
    printf("produced=%ld\n", metrics->produced);
    printf("consumed=%ld\n", metrics->consumed);
    printf("max_occupancy=%d\n", metrics->max_occupancy);
    printf("capacity=%d\n", metrics->capacity);
    printf("underflow=%d\n", metrics->underflow);
    printf("overflow=%d\n", metrics->overflow);
}
