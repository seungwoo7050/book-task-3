/*
 * Starter proxy.
 *
 * The completed implementations live in ../c and ../cpp.
 */

#include <pthread.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "csapp.h"

static void *thread(void *arg);

int main(int argc, char **argv)
{
    int listenfd;
    pthread_t tid;

    if (argc != 2) {
        fprintf(stderr, "Usage: %s <port>\n", argv[0]);
        return 1;
    }

    signal(SIGPIPE, SIG_IGN);
    listenfd = open_listenfd(argv[1]);
    if (listenfd < 0) {
        fprintf(stderr, "open_listenfd failed\n");
        return 1;
    }

    while (1) {
        int *connfdp = (int *)malloc(sizeof(int));
        struct sockaddr_storage clientaddr;
        socklen_t clientlen = sizeof(clientaddr);

        if (connfdp == NULL) {
            break;
        }
        *connfdp = accept(listenfd, (struct sockaddr *)&clientaddr, &clientlen);
        if (*connfdp < 0) {
            free(connfdp);
            continue;
        }
        pthread_create(&tid, NULL, thread, connfdp);
    }

    close(listenfd);
    return 0;
}

static void *thread(void *arg)
{
    int connfd = *(int *)arg;

    pthread_detach(pthread_self());
    free(arg);

    /*
     * TODO:
     * - read the request line and headers
     * - parse the absolute URI
     * - build a normalized HTTP/1.0 request
     * - forward the response
     * - add caching
     */
    close(connfd);
    return NULL;
}
