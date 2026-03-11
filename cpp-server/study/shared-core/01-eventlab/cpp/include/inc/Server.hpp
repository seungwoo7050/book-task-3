#pragma once

#include "EventManager.hpp"

#include <cstddef>
#include <ctime>
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
        std::time_t timestamp;
        bool        pinged;
        bool        doomed;

        Client();
        Client(int socket_fd, const std::string &ip);
    };

    static const std::string servername;
    static const std::size_t bufsiz;
    static const std::time_t timeout;
    static const std::time_t cutoff;

    Server(const char *portstr);
    ~Server();

    void run();

private:
    static bool validate_port(const char *portstr);

    void run_event_loop();
    void keep_alive();
    void accept_connection(int sockfd, const std::string &ipaddr);
    void disconnect(int sockfd);
    ssize_t read_packet(Client &client, std::size_t maxlen);
    ssize_t send_packet(Client &client);
    void process_input(Client &client);
    void handle_line(Client &client, const std::string &line);
    void queue_reply(Client &client, const std::string &reply);

    int                     listenfd;
    EventManager            manager;
    bool                    interrupt;
    std::map<int, Client>   clients;
    std::set<int>           sendq;

    Server(const Server &other);
    Server &operator=(const Server &rhs);
};
