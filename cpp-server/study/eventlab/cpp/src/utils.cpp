#include "inc/utils.hpp"

#include <sys/socket.h> // recv(2) // send(2)
#include <cctype>       // std::toupper
#include <cerrno>
#include <cstring>
#include <string>

ssize_t utils::full_recvn(int sockfd, void *buf, size_t n)
{
    size_t nleft = n;
    ssize_t nread = 0;
    char *bufp = reinterpret_cast<char *>(buf);

    while (nleft > 0)
    {
        if ((nread = recv(sockfd, bufp, nleft, 0)) < 0)
            return -1;
        else if (nread == 0)
            break;
        nleft -= nread;
        bufp += nread;
    }
    bufp[n - nleft] = '\0';
    return n - nleft;
}

ssize_t utils::full_sendn(int sockfd, const void *buf, size_t n)
{
    size_t nleft = n;
    ssize_t nsent = 0;
    const char *bufp = reinterpret_cast<const char *>(buf);

    while (nleft > 0)
    {
        if ((nsent = send(sockfd, bufp, nleft, 0)) < 0)
            return -1;
        nleft -= nsent;
        bufp += nsent;
    }
    return n;
}

std::string utils::time_to_str(std::time_t time)
{
    if (time == -1)
        return std::strerror(errno);
    
    char time_stamp[18] = "[yyyymmdd_hhmmss]";
    std::strftime(time_stamp, sizeof(time_stamp), "[%Y%m%d_%H%M%S]", std::localtime(&time));
    return time_stamp;
}
