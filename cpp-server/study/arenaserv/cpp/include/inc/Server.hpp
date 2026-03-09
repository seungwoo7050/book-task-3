#pragma once

#include "EventManager.hpp"
#include "MatchEngine.hpp"

#include <cstddef>
#include <cstdint>
#include <map>
#include <set>
#include <string>

class Server
{
public:
    struct Client
    {
        int         fd;
        std::string ipaddr;
        std::string recvbuf;
        std::string sendbuf;
        std::string token;
        bool        doomed;

        Client();
        Client(int socket_fd, const std::string &ip);
    };

    static const std::string servername;
    static const std::size_t bufsiz;
    static const std::uint64_t tick_interval_ms;

    Server(const char *portstr);
    ~Server();

    void run();

private:
    static bool validate_port(const char *portstr);
    static std::uint64_t current_millis();

    void run_event_loop();
    void pump_ticks();
    void accept_connection(int sockfd, const std::string &ipaddr);
    void disconnect(int sockfd);
    ssize_t read_packet(Client &client, std::size_t maxlen);
    ssize_t send_packet(Client &client);
    void process_input(Client &client);
    void handle_line(Client &client, const std::string &line);
    void handle_hello(Client &client, const std::string &nick);
    void handle_queue(Client &client);
    void handle_ready(Client &client);
    void handle_input(Client &client, const std::string &line);
    void handle_rejoin(Client &client, const std::string &token);
    void handle_leave(Client &client);
    void dispatch_engine_events();
    void queue_reply(Client &client, const std::string &reply);
    void send_error(Client &client, const std::string &code, const std::string &message);

    int                       listenfd;
    EventManager              manager;
    bool                      interrupt;
    std::map<int, Client>     clients;
    std::map<std::string, int> token_to_fd;
    std::set<int>             sendq;
    MatchEngine               engine;
    std::uint64_t             last_tick_ms;

    Server(const Server &other);
    Server &operator=(const Server &rhs);
};
