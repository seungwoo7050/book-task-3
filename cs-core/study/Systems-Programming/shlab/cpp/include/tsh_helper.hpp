/*
 * tsh_helper.hpp - tiny shell용 signal-safe helper 모음.
 */

#ifndef TSH_HELPER_HPP
#define TSH_HELPER_HPP

#include <cstring>
#include <unistd.h>

static inline ssize_t sio_puts(const char *s)
{
    return write(STDOUT_FILENO, s, std::strlen(s));
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
        buf[i--] = static_cast<char>('0' + (v % 10));
        v /= 10;
    } while (v > 0);
    if (neg) {
        buf[i--] = '-';
    }
    write(STDOUT_FILENO, &buf[i + 1], static_cast<size_t>(30 - i));
}

#endif
