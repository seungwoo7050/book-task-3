#ifndef MINI_ATTACKLAB_H
#define MINI_ATTACKLAB_H

#include <stddef.h>

int parse_hex_string(const char *text, unsigned char *buffer, size_t capacity, size_t *out_len);
int load_hex_file(const char *path, unsigned char *buffer, size_t capacity, size_t *out_len);

int attacklab_phase_1(const unsigned char *bytes, size_t len);
int attacklab_phase_2(const unsigned char *bytes, size_t len);
int attacklab_phase_3(const unsigned char *bytes, size_t len);
int attacklab_phase_4(const unsigned char *bytes, size_t len);
int attacklab_phase_5(const unsigned char *bytes, size_t len);
int attacklab_validate_phase(int phase, const unsigned char *bytes, size_t len);
const char *attacklab_phase_name(int phase);

#endif
