#include <dirent.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/time.h>

#include "../code/memlib.h"
#include "../code/mm.h"

typedef struct {
    int errors;
    int ops;
    size_t peak_live;
    size_t peak_heap;
    double seconds;
} trace_result_t;

static unsigned char expected_byte(int id, size_t index)
{
    return (unsigned char)(((unsigned int)(id + 1) * 131u + (unsigned int)(index * 17u)) & 0xffu);
}

static void fill_pattern(void *ptr, int id, size_t size)
{
    size_t index;
    unsigned char *bytes = (unsigned char *)ptr;

    for (index = 0; index < size; ++index) {
        bytes[index] = expected_byte(id, index);
    }
}

static int verify_pattern(const void *ptr, int id, size_t size, const char *trace_name, const char *context)
{
    size_t index;
    const unsigned char *bytes = (const unsigned char *)ptr;

    for (index = 0; index < size; ++index) {
        if (bytes[index] != expected_byte(id, index)) {
            fprintf(stderr,
                    "%s: payload mismatch for id %d during %s at byte %zu\n",
                    trace_name, id, context, index);
            return 1;
        }
    }
    return 0;
}

static int verify_preserved_prefix(const void *ptr, int id, size_t old_size, size_t new_size, const char *trace_name)
{
    size_t kept = old_size < new_size ? old_size : new_size;
    return verify_pattern(ptr, id, kept, trace_name, "realloc");
}

static int overlap(const void *left_ptr, size_t left_size, const void *right_ptr, size_t right_size)
{
    const char *left_lo = (const char *)left_ptr;
    const char *left_hi = left_lo + left_size;
    const char *right_lo = (const char *)right_ptr;
    const char *right_hi = right_lo + right_size;

    return left_lo < right_hi && right_lo < left_hi;
}

static int verify_non_overlap(const void *candidate,
                              size_t candidate_size,
                              void **blocks,
                              size_t *sizes,
                              int ids,
                              int current_id,
                              const char *trace_name)
{
    int id;

    if (candidate == NULL || candidate_size == 0) {
        return 0;
    }

    for (id = 0; id < ids; ++id) {
        if (id == current_id || blocks[id] == NULL || sizes[id] == 0) {
            continue;
        }
        if (overlap(candidate, candidate_size, blocks[id], sizes[id])) {
            fprintf(stderr, "%s: allocation for id %d overlaps active block %d\n", trace_name, current_id, id);
            return 1;
        }
    }
    return 0;
}

static char *dup_string(const char *src)
{
    size_t length = strlen(src) + 1;
    char *copy = (char *)malloc(length);
    if (copy != NULL) {
        memcpy(copy, src, length);
    }
    return copy;
}

static int has_rep_suffix(const char *name)
{
    size_t len = strlen(name);
    return len > 4 && strcmp(name + len - 4, ".rep") == 0;
}

static int compare_names(const void *left, const void *right)
{
    const char *const *lhs = (const char *const *)left;
    const char *const *rhs = (const char *const *)right;
    return strcmp(*lhs, *rhs);
}

static int collect_trace_names(const char *trace_dir, char ***names_out)
{
    DIR *dir = opendir(trace_dir);
    struct dirent *entry;
    char **names = NULL;
    int count = 0;
    int capacity = 0;

    if (dir == NULL) {
        fprintf(stderr, "Cannot open %s: %s\n", trace_dir, strerror(errno));
        return -1;
    }

    while ((entry = readdir(dir)) != NULL) {
        char path[PATH_MAX];
        struct stat st;
        char **grown;

        if (!has_rep_suffix(entry->d_name)) {
            continue;
        }

        snprintf(path, sizeof(path), "%s/%s", trace_dir, entry->d_name);
        if (stat(path, &st) != 0 || !S_ISREG(st.st_mode)) {
            continue;
        }

        if (count == capacity) {
            capacity = capacity == 0 ? 8 : capacity * 2;
            grown = (char **)realloc(names, (size_t)capacity * sizeof(char *));
            if (grown == NULL) {
                closedir(dir);
                return -1;
            }
            names = grown;
        }

        names[count] = dup_string(entry->d_name);
        if (names[count] == NULL) {
            closedir(dir);
            return -1;
        }
        ++count;
    }

    closedir(dir);

    qsort(names, (size_t)count, sizeof(char *), compare_names);
    *names_out = names;
    return count;
}

static void free_trace_names(char **names, int count)
{
    int index;
    for (index = 0; index < count; ++index) {
        free(names[index]);
    }
    free(names);
}

static double now_seconds(void)
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (double)tv.tv_sec + (double)tv.tv_usec / 1000000.0;
}

static int run_trace(const char *trace_path, const char *trace_name, int verbose, trace_result_t *result)
{
    FILE *fp = fopen(trace_path, "r");
    void **blocks = NULL;
    size_t *sizes = NULL;
    int ids = 0;
    int total_ops = 0;
    int errors = 0;
    int op_index;
    size_t live_bytes = 0;
    size_t peak_live = 0;
    size_t peak_heap = 0;
    double start;
    double end;

    if (fp == NULL) {
        fprintf(stderr, "Cannot open %s: %s\n", trace_path, strerror(errno));
        return 1;
    }

    if (fscanf(fp, "%d %d", &ids, &total_ops) != 2 || ids <= 0 || total_ops < 0) {
        fclose(fp);
        fprintf(stderr, "%s: malformed header\n", trace_name);
        return 1;
    }

    blocks = (void **)calloc((size_t)ids, sizeof(void *));
    sizes = (size_t *)calloc((size_t)ids, sizeof(size_t));
    if (blocks == NULL || sizes == NULL) {
        fclose(fp);
        free(blocks);
        free(sizes);
        fprintf(stderr, "%s: out of memory in driver\n", trace_name);
        return 1;
    }

    mem_reset_brk();
    if (mm_init() < 0) {
        fclose(fp);
        free(blocks);
        free(sizes);
        fprintf(stderr, "%s: mm_init failed\n", trace_name);
        return 1;
    }

    peak_heap = mem_heapsize();
    start = now_seconds();

    for (op_index = 0; op_index < total_ops; ++op_index) {
        char op;
        int id;
        size_t size = 0;

        if (fscanf(fp, " %c %d", &op, &id) != 2) {
            fprintf(stderr, "%s: malformed operation %d\n", trace_name, op_index);
            ++errors;
            break;
        }
        if (id < 0 || id >= ids) {
            fprintf(stderr, "%s: invalid id %d\n", trace_name, id);
            ++errors;
            break;
        }

        if (op == 'a' || op == 'r') {
            if (fscanf(fp, " %zu", &size) != 1) {
                fprintf(stderr, "%s: missing size for operation %d\n", trace_name, op_index);
                ++errors;
                break;
            }
        }

        if (op == 'a') {
            void *ptr;

            if (blocks[id] != NULL) {
                fprintf(stderr, "%s: id %d allocated twice without free\n", trace_name, id);
                ++errors;
                continue;
            }

            ptr = mm_malloc(size);
            if (size == 0) {
                if (ptr != NULL) {
                    fprintf(stderr, "%s: mm_malloc(0) returned non-NULL\n", trace_name);
                    ++errors;
                }
                continue;
            }
            if (ptr == NULL) {
                fprintf(stderr, "%s: mm_malloc(%zu) returned NULL\n", trace_name, size);
                ++errors;
                continue;
            }
            if (((size_t)ptr & 0xfu) != 0u) {
                fprintf(stderr, "%s: mm_malloc(%zu) returned misaligned pointer\n", trace_name, size);
                ++errors;
            }

            blocks[id] = ptr;
            sizes[id] = size;
            errors += verify_non_overlap(ptr, size, blocks, sizes, ids, id, trace_name);
            fill_pattern(ptr, id, size);
            live_bytes += size;
        } else if (op == 'f') {
            if (blocks[id] != NULL) {
                errors += verify_pattern(blocks[id], id, sizes[id], trace_name, "free");
                live_bytes -= sizes[id];
            }
            mm_free(blocks[id]);
            blocks[id] = NULL;
            sizes[id] = 0;
        } else if (op == 'r') {
            void *old_ptr = blocks[id];
            size_t old_size = sizes[id];
            void *new_ptr;

            if (old_ptr != NULL) {
                errors += verify_pattern(old_ptr, id, old_size, trace_name, "realloc-before");
            }

            new_ptr = mm_realloc(old_ptr, size);
            live_bytes -= old_size;

            if (size == 0) {
                if (new_ptr != NULL) {
                    fprintf(stderr, "%s: realloc(%d, 0) returned non-NULL\n", trace_name, id);
                    ++errors;
                }
                blocks[id] = NULL;
                sizes[id] = 0;
            } else {
                if (new_ptr == NULL) {
                    fprintf(stderr, "%s: mm_realloc(%d, %zu) returned NULL\n", trace_name, id, size);
                    ++errors;
                    blocks[id] = NULL;
                    sizes[id] = 0;
                } else {
                    if (((size_t)new_ptr & 0xfu) != 0u) {
                        fprintf(stderr, "%s: mm_realloc(%d, %zu) returned misaligned pointer\n", trace_name, id, size);
                        ++errors;
                    }
                    blocks[id] = new_ptr;
                    sizes[id] = size;
                    errors += verify_preserved_prefix(new_ptr, id, old_size, size, trace_name);
                    errors += verify_non_overlap(new_ptr, size, blocks, sizes, ids, id, trace_name);
                    fill_pattern(new_ptr, id, size);
                    live_bytes += size;
                }
            }
        } else {
            fprintf(stderr, "%s: unknown op '%c'\n", trace_name, op);
            ++errors;
            break;
        }

        if (live_bytes > peak_live) {
            peak_live = live_bytes;
        }
        if (mem_heapsize() > peak_heap) {
            peak_heap = mem_heapsize();
        }
    }

    end = now_seconds();

    for (op_index = 0; op_index < ids; ++op_index) {
        if (blocks[op_index] != NULL) {
            errors += verify_pattern(blocks[op_index], op_index, sizes[op_index], trace_name, "final-check");
            mm_free(blocks[op_index]);
        }
    }

    fclose(fp);
    free(blocks);
    free(sizes);

    result->errors = errors;
    result->ops = total_ops;
    result->peak_live = peak_live;
    result->peak_heap = peak_heap;
    result->seconds = end - start;

    if (verbose) {
        double util = peak_heap == 0 ? 0.0 : (double)peak_live / (double)peak_heap;
        double throughput = result->seconds <= 0.0 ? 0.0 : (double)total_ops / result->seconds;
        printf("Trace %s: errors=%d peak_live=%zu peak_heap=%zu util=%.3f throughput=%.0f ops/s\n",
               trace_name, errors, peak_live, peak_heap, util, throughput);
    }

    return errors;
}

int main(int argc, char **argv)
{
    char **trace_names = NULL;
    const char *trace_dir = NULL;
    int verbose = 0;
    int trace_count;
    int index;
    int total_errors = 0;
    int total_ops = 0;
    double total_seconds = 0.0;
    double total_util = 0.0;

    for (index = 1; index < argc; ++index) {
        if (strcmp(argv[index], "-t") == 0 && index + 1 < argc) {
            trace_dir = argv[++index];
        } else if (strcmp(argv[index], "-v") == 0) {
            verbose = 1;
        } else {
            fprintf(stderr, "Usage: %s -t <trace_dir> [-v]\n", argv[0]);
            return 1;
        }
    }

    if (trace_dir == NULL) {
        fprintf(stderr, "Usage: %s -t <trace_dir> [-v]\n", argv[0]);
        return 1;
    }

    trace_count = collect_trace_names(trace_dir, &trace_names);
    if (trace_count <= 0) {
        fprintf(stderr, "No trace files found in %s\n", trace_dir);
        return 1;
    }

    mem_init();

    for (index = 0; index < trace_count; ++index) {
        char path[PATH_MAX];
        trace_result_t result;
        double util;

        snprintf(path, sizeof(path), "%s/%s", trace_dir, trace_names[index]);
        total_errors += run_trace(path, trace_names[index], verbose, &result);
        util = result.peak_heap == 0 ? 0.0 : (double)result.peak_live / (double)result.peak_heap;
        total_util += util;
        total_ops += result.ops;
        total_seconds += result.seconds;
    }

    mem_deinit();

    printf("Summary: traces=%d errors=%d avg_util=%.3f throughput=%.0f ops/s\n",
           trace_count,
           total_errors,
           trace_count == 0 ? 0.0 : total_util / (double)trace_count,
           total_seconds <= 0.0 ? 0.0 : (double)total_ops / total_seconds);

    free_trace_names(trace_names, trace_count);
    return total_errors == 0 ? 0 : 1;
}
