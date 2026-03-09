#pragma once

#include <vector>
#include <string>
#include <unistd.h>

class Server;
class Connection;
class Message;
class Channel;

class Executor
{
    public:
    static enum NUMERICS
    {
        ERR_NEEDMOREPARAMS = 461,
        ERR_ALREADYREGISTRED = 462,
        ERR_PASSWDMISMATCH = 464
    } numerics;

    typedef enum NUMERICS numeric;

    public:
    static void to_doom(Server &server, Connection *&node, const std::string &reply);
    static void dispatch_packet(Server &server, Connection *&node, const std::string &reply);
    static void broadcast(Server &server, const std::string &reply);    /* send to every `registered` client */
    static void broadcast(Server &server, Channel *&channel, const std::string &reply);
    static void process(Server &server, Connection *&node, std::vector<Message> &batch);

    private:
    static std::string  _generate_reply(Server &server, Connection *&nodeptr, const Message &msg, numeric code);
    static numeric      _validate_pass(Server &server, Connection *&nodeptr, Message &msg);
    static void         _execute_pass(Server &server, Connection *&node, const Message &msg);
    static void         _execute_nick(Server &server, Connection *&node, const Message &msg);
    static void         _execute_user(Server &server, Connection *&node, const Message &msg);

    static void         _execute_cap(Server &server, Connection *&node, const Message &msg);
    static void         _execute_ping(Server &server, Connection *&node, const Message &msg);
    static void         _execute_privmsg(Server &server, Connection *&node, const Message &msg);
    static void         _execute_join(Server &server, Connection *&node, const Message &msg);
    static void         _execute_part(Server &server, Connection *&node, const Message &msg);

    static void _execute_quit(Server &server, Connection *&node, const Message &msg);
    static void _execute_topic(Server &server, Connection *&node, const Message &msg);
    static void _execute_notice(Server &server, Connection *&node, const Message &msg);
    static void _execute_kick(Server &server, Connection *&node, const Message &msg);
    static void _execute_invite(Server &server, Connection *&node, const Message &msg);
    static void _execute_mode(Server &server, Connection *&node, const Message &msg);

    static bool         _isNickInUse(const Server &server, const std::string &nickname);
	static std::string	_isupport(Server &server, Connection *&node);
    static std::string  _generate_rpl_namreply(const std::string &servname, Channel *&chan, Connection *&node);
};


/*
    enum COMMAND
    {
        PASS,
        NICK,
        USER,
        JOIN,
        PART,
        PRIVMSG,
        NOTICE,
        LUSER,
        KICK,
        INVITE,
        TOPIC,
        MODE,
        PING,
        // PONG,
        QUIT,
        CAP,
        UNK
        // MOTD?
    } command;


*/