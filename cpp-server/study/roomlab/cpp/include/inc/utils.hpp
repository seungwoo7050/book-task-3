#pragma once

#include <sys/types.h>  // ssize_t
#include <string>
#include <ctime>

namespace utils
{
    /* Reads upto n bytes. Uninterruptible. */
    ssize_t     full_recvn(int sockfd, void *buf, size_t n);

    /* Writes upto n bytes. Uninterruptible. */
    ssize_t     full_sendn(int sockfd, const void *buf, size_t n);

    std::string time_to_str(std::time_t time);
}
