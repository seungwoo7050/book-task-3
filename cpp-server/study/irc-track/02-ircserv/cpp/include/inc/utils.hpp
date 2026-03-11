#pragma once

#include <sys/types.h>  // ssize_t
#include <string>
#include <ctime>

namespace utils
{
    /* 최대 n bytes를 읽는다. EINTR이 와도 재시도한다. */
    ssize_t     full_recvn(int sockfd, void *buf, size_t n);

    /* 최대 n bytes를 쓴다. EINTR이 와도 재시도한다. */
    ssize_t     full_sendn(int sockfd, const void *buf, size_t n);

    std::string time_to_str(std::time_t time);
}
