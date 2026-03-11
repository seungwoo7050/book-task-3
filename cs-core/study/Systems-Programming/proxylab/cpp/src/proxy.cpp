#include <csignal>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <strings.h>
#include <pthread.h>
#include <string>
#include <unistd.h>

#include "csapp.h"

namespace {

constexpr std::size_t kMaxCacheSize = 1048576;
constexpr std::size_t kMaxObjectSize = 102400;
constexpr std::size_t kMaxRequestSize = 65536;

const char *kUserAgentHeader =
    "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:10.0.3) "
    "Gecko/20120305 Firefox/10.0.3\r\n";

struct CacheEntry {
    char uri[MAXLINE];
    char *data;
    std::size_t size;
    CacheEntry *prev;
    CacheEntry *next;
};

CacheEntry *g_cache_head = nullptr;
CacheEntry *g_cache_tail = nullptr;
std::size_t g_cache_total = 0;
pthread_mutex_t g_cache_lock = PTHREAD_MUTEX_INITIALIZER;

void remove_entry(CacheEntry *entry)
{
    if (entry->prev != nullptr) {
        entry->prev->next = entry->next;
    } else {
        g_cache_head = entry->next;
    }

    if (entry->next != nullptr) {
        entry->next->prev = entry->prev;
    } else {
        g_cache_tail = entry->prev;
    }
}

void insert_front(CacheEntry *entry)
{
    entry->prev = nullptr;
    entry->next = g_cache_head;
    if (g_cache_head != nullptr) {
        g_cache_head->prev = entry;
    } else {
        g_cache_tail = entry;
    }
    g_cache_head = entry;
}

void promote_entry(CacheEntry *entry)
{
    if (entry == g_cache_head) {
        return;
    }
    remove_entry(entry);
    insert_front(entry);
}

bool cache_lookup(const char *uri, char **data_out, std::size_t *size_out)
{
    pthread_mutex_lock(&g_cache_lock);
    for (CacheEntry *entry = g_cache_head; entry != nullptr; entry = entry->next) {
        if (std::strcmp(entry->uri, uri) == 0) {
            char *copy = static_cast<char *>(std::malloc(entry->size));
            if (copy == nullptr) {
                pthread_mutex_unlock(&g_cache_lock);
                return false;
            }
            promote_entry(entry);
            std::memcpy(copy, entry->data, entry->size);
            *data_out = copy;
            *size_out = entry->size;
            pthread_mutex_unlock(&g_cache_lock);
            return true;
        }
    }
    pthread_mutex_unlock(&g_cache_lock);
    return false;
}

void cache_store(const char *uri, const char *data, std::size_t size)
{
    CacheEntry *entry;

    if (size == 0 || size > kMaxObjectSize) {
        return;
    }

    entry = static_cast<CacheEntry *>(std::malloc(sizeof(CacheEntry)));
    if (entry == nullptr) {
        return;
    }
    entry->data = static_cast<char *>(std::malloc(size));
    if (entry->data == nullptr) {
        std::free(entry);
        return;
    }

    std::strncpy(entry->uri, uri, MAXLINE - 1);
    entry->uri[MAXLINE - 1] = '\0';
    std::memcpy(entry->data, data, size);
    entry->size = size;

    pthread_mutex_lock(&g_cache_lock);
    while (g_cache_tail != nullptr && g_cache_total + size > kMaxCacheSize) {
        CacheEntry *victim = g_cache_tail;
        remove_entry(victim);
        g_cache_total -= victim->size;
        std::free(victim->data);
        std::free(victim);
    }
    insert_front(entry);
    g_cache_total += size;
    pthread_mutex_unlock(&g_cache_lock);
}

void client_error(int fd, const char *status, const char *message)
{
    char response[MAXLINE];
    int written = std::snprintf(response, sizeof(response),
                                "HTTP/1.0 %s\r\n"
                                "Content-Type: text/plain\r\n"
                                "Connection: close\r\n"
                                "\r\n"
                                "%s\r\n",
                                status, message);
    if (written > 0) {
        rio_writen(fd, response, static_cast<std::size_t>(written));
    }
}

int parse_uri(const char *uri, char *host, char *port, char *path)
{
    const char *host_start = uri;
    const char *path_start;
    const char *colon;
    std::size_t host_len;

    if (strncasecmp(uri, "http://", 7) == 0) {
        host_start = uri + 7;
    }

    path_start = std::strchr(host_start, '/');
    if (path_start == nullptr) {
        path_start = host_start + std::strlen(host_start);
        std::strcpy(path, "/");
    } else {
        std::snprintf(path, MAXLINE, "%s", path_start);
    }

    colon = static_cast<const char *>(std::memchr(host_start, ':', static_cast<std::size_t>(path_start - host_start)));
    if (colon != nullptr) {
        host_len = static_cast<std::size_t>(colon - host_start);
        std::snprintf(port, MAXLINE, "%.*s", static_cast<int>(path_start - colon - 1), colon + 1);
    } else {
        host_len = static_cast<std::size_t>(path_start - host_start);
        std::strcpy(port, "80");
    }

    if (host_len == 0 || host_len >= MAXLINE) {
        return -1;
    }
    std::snprintf(host, MAXLINE, "%.*s", static_cast<int>(host_len), host_start);
    return 0;
}

int append_line(char *request, std::size_t capacity, const char *line)
{
    const std::size_t used = std::strlen(request);
    const std::size_t line_len = std::strlen(line);
    if (used + line_len + 1 > capacity) {
        return -1;
    }
    std::memcpy(request + used, line, line_len + 1);
    return 0;
}

int build_request(char *request, std::size_t capacity, const char *host, const char *port,
                  const char *path, rio_t *client_rio)
{
    char line[MAXLINE];
    char host_line[MAXLINE];

    request[0] = '\0';
    if (std::snprintf(request, capacity, "GET %s HTTP/1.0\r\n", path) >= static_cast<int>(capacity)) {
        return -1;
    }

    if (std::strcmp(port, "80") == 0) {
        std::snprintf(host_line, sizeof(host_line), "Host: %s\r\n", host);
    } else {
        std::snprintf(host_line, sizeof(host_line), "Host: %s:%s\r\n", host, port);
    }

    if (append_line(request, capacity, host_line) < 0 ||
        append_line(request, capacity, kUserAgentHeader) < 0 ||
        append_line(request, capacity, "Connection: close\r\n") < 0 ||
        append_line(request, capacity, "Proxy-Connection: close\r\n") < 0) {
        return -1;
    }

    while (rio_readlineb(client_rio, line, sizeof(line)) > 0) {
        if (std::strcmp(line, "\r\n") == 0) {
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

void handle_client(int clientfd)
{
    char buf[MAXLINE];
    char method[MAXLINE];
    char uri[MAXLINE];
    char version[MAXLINE];
    char host[MAXLINE];
    char port[MAXLINE];
    char path[MAXLINE];
    char request[kMaxRequestSize];
    char *cached_data = nullptr;
    std::size_t cached_size = 0;
    rio_t client_rio;
    rio_t server_rio;
    int serverfd;
    ssize_t n;

    rio_readinitb(&client_rio, clientfd);
    if (rio_readlineb(&client_rio, buf, sizeof(buf)) <= 0) {
        return;
    }
    if (std::sscanf(buf, "%s %s %s", method, uri, version) != 3) {
        client_error(clientfd, "400 Bad Request", "Malformed request line");
        return;
    }
    if (strcasecmp(method, "GET") != 0) {
        client_error(clientfd, "501 Not Implemented", "Only GET is supported");
        return;
    }

    if (cache_lookup(uri, &cached_data, &cached_size)) {
        rio_writen(clientfd, cached_data, cached_size);
        std::free(cached_data);
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

    if (rio_writen(serverfd, request, std::strlen(request)) < 0) {
        close(serverfd);
        return;
    }

    rio_readinitb(&server_rio, serverfd);
    {
        char object_buf[kMaxObjectSize];
        std::size_t object_size = 0;
        bool cacheable = true;

        while ((n = rio_readnb(&server_rio, buf, sizeof(buf))) > 0) {
            if (rio_writen(clientfd, buf, static_cast<std::size_t>(n)) < 0) {
                break;
            }
            if (cacheable) {
                if (object_size + static_cast<std::size_t>(n) <= kMaxObjectSize) {
                    std::memcpy(object_buf + object_size, buf, static_cast<std::size_t>(n));
                    object_size += static_cast<std::size_t>(n);
                } else {
                    cacheable = false;
                }
            }
        }

        if (cacheable && object_size > 0) {
            cache_store(uri, object_buf, object_size);
        }
    }

    close(serverfd);
}

void *thread_main(void *arg)
{
    int clientfd = *static_cast<int *>(arg);
    pthread_detach(pthread_self());
    std::free(arg);
    handle_client(clientfd);
    close(clientfd);
    return nullptr;
}

}  // 내부 helper 이름공간 끝

int main(int argc, char **argv)
{
    int listenfd;

    std::signal(SIGPIPE, SIG_IGN);

    if (argc != 2) {
        std::fprintf(stderr, "Usage: %s <port>\n", argv[0]);
        return 1;
    }

    listenfd = open_listenfd(argv[1]);
    if (listenfd < 0) {
        std::fprintf(stderr, "open_listenfd failed\n");
        return 1;
    }

    while (true) {
        struct sockaddr_storage clientaddr;
        socklen_t clientlen = sizeof(clientaddr);
        int *clientfd = static_cast<int *>(std::malloc(sizeof(int)));
        pthread_t tid;

        if (clientfd == nullptr) {
            continue;
        }

        *clientfd = accept(listenfd, reinterpret_cast<struct sockaddr *>(&clientaddr), &clientlen);
        if (*clientfd < 0) {
            std::free(clientfd);
            continue;
        }
        pthread_create(&tid, nullptr, thread_main, clientfd);
    }
}
