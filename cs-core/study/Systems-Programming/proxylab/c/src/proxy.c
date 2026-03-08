#include <pthread.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <unistd.h>

#include "csapp.h"

#define MAX_CACHE_SIZE 1048576
#define MAX_OBJECT_SIZE 102400
#define MAX_REQUEST_SIZE 65536

static const char *user_agent_hdr =
    "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:10.0.3) "
    "Gecko/20120305 Firefox/10.0.3\r\n";

typedef struct cache_entry {
    char uri[MAXLINE];
    char *data;
    size_t size;
    struct cache_entry *prev;
    struct cache_entry *next;
} cache_entry_t;

static cache_entry_t *cache_head = NULL;
static cache_entry_t *cache_tail = NULL;
static size_t cache_total = 0;
static pthread_mutex_t cache_lock = PTHREAD_MUTEX_INITIALIZER;

static void *thread_main(void *arg);
static void handle_client(int clientfd);
static void client_error(int fd, const char *status, const char *message);
static int parse_uri(const char *uri, char *host, char *port, char *path);
static int append_line(char *request, size_t capacity, const char *line);
static int build_request(char *request, size_t capacity, const char *host, const char *port,
                         const char *path, rio_t *client_rio);
static int cache_lookup(const char *uri, char **data_out, size_t *size_out);
static void cache_store(const char *uri, const char *data, size_t size);

static void remove_entry(cache_entry_t *entry)
{
    if (entry->prev != NULL) {
        entry->prev->next = entry->next;
    } else {
        cache_head = entry->next;
    }

    if (entry->next != NULL) {
        entry->next->prev = entry->prev;
    } else {
        cache_tail = entry->prev;
    }
}

static void insert_front(cache_entry_t *entry)
{
    entry->prev = NULL;
    entry->next = cache_head;
    if (cache_head != NULL) {
        cache_head->prev = entry;
    } else {
        cache_tail = entry;
    }
    cache_head = entry;
}

static void promote_entry(cache_entry_t *entry)
{
    if (entry == cache_head) {
        return;
    }
    remove_entry(entry);
    insert_front(entry);
}

static int cache_lookup(const char *uri, char **data_out, size_t *size_out)
{
    cache_entry_t *entry;
    char *copy;

    pthread_mutex_lock(&cache_lock);
    for (entry = cache_head; entry != NULL; entry = entry->next) {
        if (strcmp(entry->uri, uri) == 0) {
            promote_entry(entry);
            copy = (char *)malloc(entry->size);
            if (copy == NULL) {
                pthread_mutex_unlock(&cache_lock);
                return 0;
            }
            memcpy(copy, entry->data, entry->size);
            *data_out = copy;
            *size_out = entry->size;
            pthread_mutex_unlock(&cache_lock);
            return 1;
        }
    }
    pthread_mutex_unlock(&cache_lock);
    return 0;
}

static void cache_store(const char *uri, const char *data, size_t size)
{
    cache_entry_t *entry;

    if (size == 0 || size > MAX_OBJECT_SIZE) {
        return;
    }

    entry = (cache_entry_t *)malloc(sizeof(cache_entry_t));
    if (entry == NULL) {
        return;
    }
    entry->data = (char *)malloc(size);
    if (entry->data == NULL) {
        free(entry);
        return;
    }

    strncpy(entry->uri, uri, MAXLINE - 1);
    entry->uri[MAXLINE - 1] = '\0';
    memcpy(entry->data, data, size);
    entry->size = size;

    pthread_mutex_lock(&cache_lock);

    while (cache_tail != NULL && cache_total + size > MAX_CACHE_SIZE) {
        cache_entry_t *victim = cache_tail;
        remove_entry(victim);
        cache_total -= victim->size;
        free(victim->data);
        free(victim);
    }

    insert_front(entry);
    cache_total += size;
    pthread_mutex_unlock(&cache_lock);
}

static void client_error(int fd, const char *status, const char *message)
{
    char response[MAXLINE];
    int written = snprintf(response, sizeof(response),
                           "HTTP/1.0 %s\r\n"
                           "Content-Type: text/plain\r\n"
                           "Connection: close\r\n"
                           "\r\n"
                           "%s\r\n",
                           status, message);
    if (written > 0) {
        rio_writen(fd, response, (size_t)written);
    }
}

static int parse_uri(const char *uri, char *host, char *port, char *path)
{
    const char *host_start = uri;
    const char *path_start;
    const char *colon;
    size_t host_len;

    if (strncasecmp(uri, "http://", 7) == 0) {
        host_start = uri + 7;
    }

    path_start = strchr(host_start, '/');
    if (path_start == NULL) {
        path_start = host_start + strlen(host_start);
        strcpy(path, "/");
    } else {
        snprintf(path, MAXLINE, "%s", path_start);
    }

    colon = memchr(host_start, ':', (size_t)(path_start - host_start));
    if (colon != NULL) {
        host_len = (size_t)(colon - host_start);
        snprintf(port, MAXLINE, "%.*s", (int)(path_start - colon - 1), colon + 1);
    } else {
        host_len = (size_t)(path_start - host_start);
        strcpy(port, "80");
    }

    if (host_len == 0 || host_len >= MAXLINE) {
        return -1;
    }
    snprintf(host, MAXLINE, "%.*s", (int)host_len, host_start);
    return 0;
}

static int append_line(char *request, size_t capacity, const char *line)
{
    size_t used = strlen(request);
    size_t line_len = strlen(line);

    if (used + line_len + 1 > capacity) {
        return -1;
    }
    memcpy(request + used, line, line_len + 1);
    return 0;
}

static int build_request(char *request, size_t capacity, const char *host, const char *port,
                         const char *path, rio_t *client_rio)
{
    char line[MAXLINE];
    char host_line[MAXLINE];

    request[0] = '\0';
    if (snprintf(request, capacity, "GET %s HTTP/1.0\r\n", path) >= (int)capacity) {
        return -1;
    }

    if (strcmp(port, "80") == 0) {
        snprintf(host_line, sizeof(host_line), "Host: %s\r\n", host);
    } else {
        snprintf(host_line, sizeof(host_line), "Host: %s:%s\r\n", host, port);
    }

    if (append_line(request, capacity, host_line) < 0 ||
        append_line(request, capacity, user_agent_hdr) < 0 ||
        append_line(request, capacity, "Connection: close\r\n") < 0 ||
        append_line(request, capacity, "Proxy-Connection: close\r\n") < 0) {
        return -1;
    }

    while (rio_readlineb(client_rio, line, sizeof(line)) > 0) {
        if (strcmp(line, "\r\n") == 0) {
            break;
        }
        if (strncasecmp(line, "Host:", 5) == 0 ||
            strncasecmp(line, "User-Agent:", 11) == 0 ||
            strncasecmp(line, "Connection:", 11) == 0 ||
            strncasecmp(line, "Proxy-Connection:", 17) == 0) {
            continue;
        }
        if (append_line(request, capacity, line) < 0) {
            return -1;
        }
    }

    return append_line(request, capacity, "\r\n");
}

static void handle_client(int clientfd)
{
    char buf[MAXLINE];
    char method[MAXLINE];
    char uri[MAXLINE];
    char version[MAXLINE];
    char host[MAXLINE];
    char port[MAXLINE];
    char path[MAXLINE];
    char request[MAX_REQUEST_SIZE];
    char *cached_data = NULL;
    size_t cached_size = 0;
    rio_t client_rio;
    rio_t server_rio;
    int serverfd;
    ssize_t n;

    rio_readinitb(&client_rio, clientfd);
    if (rio_readlineb(&client_rio, buf, sizeof(buf)) <= 0) {
        return;
    }
    if (sscanf(buf, "%s %s %s", method, uri, version) != 3) {
        client_error(clientfd, "400 Bad Request", "Malformed request line");
        return;
    }
    if (strcasecmp(method, "GET") != 0) {
        client_error(clientfd, "501 Not Implemented", "Only GET is supported");
        return;
    }

    if (cache_lookup(uri, &cached_data, &cached_size)) {
        rio_writen(clientfd, cached_data, cached_size);
        free(cached_data);
        return;
    }

    if (parse_uri(uri, host, port, path) < 0) {
        client_error(clientfd, "400 Bad Request", "Invalid URI");
        return;
    }
    if (build_request(request, sizeof(request), host, port, path, &client_rio) < 0) {
        client_error(clientfd, "400 Bad Request", "Request too large");
        return;
    }

    serverfd = open_clientfd(host, port);
    if (serverfd < 0) {
        client_error(clientfd, "502 Bad Gateway", "Upstream connection failed");
        return;
    }

    if (rio_writen(serverfd, request, strlen(request)) < 0) {
        close(serverfd);
        return;
    }

    rio_readinitb(&server_rio, serverfd);
    {
        char object_buf[MAX_OBJECT_SIZE];
        size_t object_size = 0;
        int cacheable = 1;

        while ((n = rio_readnb(&server_rio, buf, sizeof(buf))) > 0) {
            if (rio_writen(clientfd, buf, (size_t)n) < 0) {
                break;
            }
            if (cacheable) {
                if (object_size + (size_t)n <= MAX_OBJECT_SIZE) {
                    memcpy(object_buf + object_size, buf, (size_t)n);
                    object_size += (size_t)n;
                } else {
                    cacheable = 0;
                }
            }
        }

        if (cacheable && object_size > 0) {
            cache_store(uri, object_buf, object_size);
        }
    }

    close(serverfd);
}

static void *thread_main(void *arg)
{
    int clientfd = *(int *)arg;

    pthread_detach(pthread_self());
    free(arg);
    handle_client(clientfd);
    close(clientfd);
    return NULL;
}

int main(int argc, char **argv)
{
    int listenfd;

    signal(SIGPIPE, SIG_IGN);

    if (argc != 2) {
        fprintf(stderr, "Usage: %s <port>\n", argv[0]);
        return 1;
    }

    listenfd = open_listenfd(argv[1]);
    if (listenfd < 0) {
        fprintf(stderr, "open_listenfd failed\n");
        return 1;
    }

    while (1) {
        struct sockaddr_storage clientaddr;
        socklen_t clientlen = sizeof(clientaddr);
        int *clientfd = (int *)malloc(sizeof(int));
        pthread_t tid;

        if (clientfd == NULL) {
            continue;
        }

        *clientfd = accept(listenfd, (struct sockaddr *)&clientaddr, &clientlen);
        if (*clientfd < 0) {
            free(clientfd);
            continue;
        }
        pthread_create(&tid, NULL, thread_main, clientfd);
    }
}
