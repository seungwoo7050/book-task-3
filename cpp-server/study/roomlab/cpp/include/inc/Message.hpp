#pragma once

#include <string>
#include <map>
#include <vector>

class Message
{
    public:
    static enum COMM
    {
        PASS,
        NICK,
        USER,
        JOIN,
        PART,
        PRIVMSG,
        NOTICE,
        KICK,
        INVITE,
        TOPIC,
        MODE,
        PING,
		PONG,
        QUIT,
        CAP,
        UNK,
        COMM_CNT
    } COMM;

    typedef enum COMM label;
    
    label       comm;
    std::string prefix;
    std::string command;
    std::vector<std::string> params;

    public:
    Message(const std::string &raw);
};
