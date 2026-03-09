#pragma once

#include "EventManager.hpp"
#include "Connection.hpp"
#include "Message.hpp"
#include "Channel.hpp"

#include <ctime>    // std::size_t  std::time_t
#include <string>

#include <list>
#include <map>
#include <set>

class Server
{
    public:
    friend class Executor;

    /* configs */
    static const std::string            servername;
    static const std::string            version;
    static const std::size_t            bufsiz;     /* recv(2) buffer size */
    static const std::string            crlf;       /* message boundary (switch to "\n" in developer mode) */
    static const std::time_t            timeout;    /* time allowed for idle clients (PING) */ 
    static const std::time_t            cutoff;     /* time granted to keep alive a connection (PONG) */

    /* is_support params */
    static const std::string            chantypes;  /* supported channel types */
    static const std::string            chanlimit;  /* max channel num (per chantype) a client can join */
    static const std::string            prefix;     /* supported channel membership prefixes */
    static const std::string            nicklen;    /* max nick len */
    static const std::string            userlen;    /* max user len */
    static const std::string            channellen; /* max channel len */
    static const std::string            hostlen; 	/* max host len */
    static const std::string            kicklen; 	/* max kick len */
    static const std::string            topiclen; 	/* max topic len */

    private:
    int                                 listenfd;
    const std::string                   password;
    EventManager                       kqmanager;
    bool                                interrupt;

    /* internal databases */
    std::list<Connection *>                                     nodes;
    std::map<int, std::list<Connection *>::iterator>            sockdb;
    std::map<std::string, std::list<Connection *>::iterator>    nickdb;
    std::list<Channel *>                                        chans;
    std::map<std::string, std::list<Channel *>::iterator>       chandb;
    std::set<int>                                               sendq;
    
    public:
    void        run();

    private:
    static bool _validate_port(const char *portstr);
    static bool _validate_password(const char *passwordstr);

    void        _run_event_loop();
    void        _keep_alive();

    void        _make_connection(int sockfd, const std::string &ipaddr);
    void        _disconnect(int sockfd);

    ssize_t     _read_packet(Connection *&node, std::size_t len);
    ssize_t     _send_packet(Connection *&node, std::size_t maxlen);

    public:
    Server(const char *portstr, const char *passwordstr);
    ~Server();

    private:
    Server(const Server &other);
    Server  &operator=(const Server &rhs);
};
