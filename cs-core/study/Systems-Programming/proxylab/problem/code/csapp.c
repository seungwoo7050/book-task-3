#include "csapp.h"

static ssize_t rio_read(rio_t *rp, char *usrbuf, size_t n)
{
    size_t cnt;

    while (rp->rio_cnt <= 0) {
        rp->rio_cnt = (int)read(rp->rio_fd, rp->rio_buf, sizeof(rp->rio_buf));
        if (rp->rio_cnt < 0) {
            if (errno == EINTR) {
                continue;
            }
            return -1;
        }
        if (rp->rio_cnt == 0) {
            return 0;
        }
        rp->rio_bufptr = rp->rio_buf;
    }

    cnt = n;
    if ((size_t)rp->rio_cnt < n) {
        cnt = (size_t)rp->rio_cnt;
    }
    memcpy(usrbuf, rp->rio_bufptr, cnt);
    rp->rio_bufptr += cnt;
    rp->rio_cnt -= (int)cnt;
    return (ssize_t)cnt;
}

void rio_readinitb(rio_t *rp, int fd)
{
    rp->rio_fd = fd;
    rp->rio_cnt = 0;
    rp->rio_bufptr = rp->rio_buf;
}

ssize_t rio_readnb(rio_t *rp, void *usrbuf, size_t n)
{
    size_t nleft = n;
    ssize_t nread;
    char *bufp = (char *)usrbuf;

    while (nleft > 0) {
        nread = rio_read(rp, bufp, nleft);
        if (nread < 0) {
            return -1;
        }
        if (nread == 0) {
            break;
        }
        nleft -= (size_t)nread;
        bufp += nread;
    }
    return (ssize_t)(n - nleft);
}

ssize_t rio_readlineb(rio_t *rp, void *usrbuf, size_t maxlen)
{
    size_t index;
    ssize_t rc;
    char c;
    char *bufp = (char *)usrbuf;

    for (index = 1; index < maxlen; ++index) {
        rc = rio_read(rp, &c, 1);
        if (rc == 1) {
            *bufp++ = c;
            if (c == '\n') {
                break;
            }
        } else if (rc == 0) {
            if (index == 1) {
                return 0;
            }
            break;
        } else {
            return -1;
        }
    }
    *bufp = '\0';
    return (ssize_t)strlen((char *)usrbuf);
}

ssize_t rio_writen(int fd, const void *usrbuf, size_t n)
{
    size_t nleft = n;
    ssize_t nwritten;
    const char *bufp = (const char *)usrbuf;

    while (nleft > 0) {
        nwritten = write(fd, bufp, nleft);
        if (nwritten <= 0) {
            if (errno == EINTR) {
                nwritten = 0;
            } else {
                return -1;
            }
        }
        nleft -= (size_t)nwritten;
        bufp += nwritten;
    }
    return (ssize_t)n;
}

int open_clientfd(const char *hostname, const char *port)
{
    int clientfd = -1;
    struct addrinfo hints;
    struct addrinfo *listp = NULL;
    struct addrinfo *p;

    memset(&hints, 0, sizeof(hints));
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_NUMERICSERV | AI_ADDRCONFIG;

    if (getaddrinfo(hostname, port, &hints, &listp) != 0) {
        return -1;
    }

    for (p = listp; p != NULL; p = p->ai_next) {
        clientfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol);
        if (clientfd < 0) {
            continue;
        }
        if (connect(clientfd, p->ai_addr, p->ai_addrlen) == 0) {
            break;
        }
        close(clientfd);
        clientfd = -1;
    }

    freeaddrinfo(listp);
    return clientfd;
}

int open_listenfd(const char *port)
{
    int listenfd = -1;
    int optval = 1;
    struct addrinfo hints;
    struct addrinfo *listp = NULL;
    struct addrinfo *p;

    memset(&hints, 0, sizeof(hints));
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_PASSIVE | AI_NUMERICSERV | AI_ADDRCONFIG;
    hints.ai_family = AF_INET;

    if (getaddrinfo(NULL, port, &hints, &listp) != 0) {
        return -1;
    }

    for (p = listp; p != NULL; p = p->ai_next) {
        listenfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol);
        if (listenfd < 0) {
            continue;
        }
        setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(optval));
        if (bind(listenfd, p->ai_addr, p->ai_addrlen) == 0) {
            break;
        }
        close(listenfd);
        listenfd = -1;
    }

    freeaddrinfo(listp);
    if (listenfd < 0) {
        return -1;
    }
    if (listen(listenfd, LISTENQ) < 0) {
        close(listenfd);
        return -1;
    }
    return listenfd;
}
