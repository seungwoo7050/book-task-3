/*
 * tsh_helper.h - Signal-safe helper routines for tiny shell.
 */

#ifndef TSH_HELPER_H
#define TSH_HELPER_H

#include <string.h>
#include <unistd.h>

static inline ssize_t sio_puts(const char *s)
{
    return write(STDOUT_FILENO, s, strlen(s));
}

static inline void sio_putl(long v)
{
    char buf[32];
    int i = 30;
    int neg = 0;

    if (v < 0) {
        neg = 1;
        v = -v;
    }
    buf[31] = '\0';
    do {
        buf[i--] = (char)('0' + (v % 10));
        v /= 10;
    } while (v > 0);
    if (neg) {
        buf[i--] = '-';
    }
    write(STDOUT_FILENO, &buf[i + 1], (size_t)(30 - i));
}

#endif
