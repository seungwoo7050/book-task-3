#ifndef CSAPP_H
#define CSAPP_H

#include <errno.h>
#include <netdb.h>
#include <netinet/in.h>
#include <pthread.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#define MAXLINE 8192
#define MAXBUF 8192
#define LISTENQ 1024
#define RIO_BUFSIZE 8192

typedef struct {
    int rio_fd;
    int rio_cnt;
    char *rio_bufptr;
    char rio_buf[RIO_BUFSIZE];
} rio_t;

#ifdef __cplusplus
extern "C" {
#endif

void rio_readinitb(rio_t *rp, int fd);
ssize_t rio_readnb(rio_t *rp, void *usrbuf, size_t n);
ssize_t rio_readlineb(rio_t *rp, void *usrbuf, size_t maxlen);
ssize_t rio_writen(int fd, const void *usrbuf, size_t n);
int open_clientfd(const char *hostname, const char *port);
int open_listenfd(const char *port);

#ifdef __cplusplus
}
#endif

#endif
