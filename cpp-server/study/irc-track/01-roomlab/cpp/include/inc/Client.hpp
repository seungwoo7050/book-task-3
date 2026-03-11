#pragma once

#include "Connection.hpp"
#include "Channel.hpp"


#include <string>

#include <map>

class Client: public Connection
{
    private:
    Connection *link;

    public:
    unsigned membership; // 최대 10개의 channel에 참여할 수 있다.
    std::map<std::string, Channel *> chandb;

    public:
    

    public:
    Client(Connection *conn);
    virtual ~Client();

    private:
    Client(const Client &other);            /* 복사 금지 */
    Client  &operator=(const Client &rhs);  /* 복사 금지 */
};
