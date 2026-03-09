#pragma once

#include "Connection.hpp"
#include "Channel.hpp"

// #include "Executor.hpp"

#include <string>

#include <map>

class Client: public Connection
{
    private:
    Connection *link;

    public:
    unsigned membership; // can join upto 10 channels
    std::map<std::string, Channel *> chandb;

    public:
    

    public:
    Client(Connection *conn);
    virtual ~Client();

    private:
    Client(const Client &other);            /* delete */
    Client  &operator=(const Client &rhs);  /* delete */
};
