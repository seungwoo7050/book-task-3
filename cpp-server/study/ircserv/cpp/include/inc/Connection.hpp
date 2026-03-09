#pragma once

#include <sys/socket.h>
#include <string>
#include <ctime>

#include "Channel.hpp"

class Connection
{
    public:
    std::string         recvbuf; // truncated reply 
    std::string         sendbuf; // to send

    std::string         ipaddr;
    
    // sockaddr_storage    addr;
    // socklen_t           addrlen;
    
    const int           sockfd;
    std::string         nickname;   // max 9 chars, if exceeded, save as IP
    std::string         servername;
    std::string         hostname;
    std::string         username;
    std::time_t         timestamp;
    unsigned            membership;

    std::map<std::string, Channel *> chandb;

    // TODO: migrate all flags to a single bit field
    bool                is_doomed;
    bool                is_pinged;
    bool                is_authed; // PASS
    bool                is_registered; // NICK USER QUIT 

    public:
    int                 state;

    public:
    Connection(const int fd, const std::string &ip);
    ~Connection();
};
