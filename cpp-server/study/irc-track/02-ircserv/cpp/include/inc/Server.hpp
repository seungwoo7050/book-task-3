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

    /* 설정 값 */
    static const std::string            servername;
    static const std::string            version;
    static const std::size_t            bufsiz;     /* recv(2) buffer 크기 */
    static const std::string            crlf;       /* 메시지 경계 (`developer mode`에서는 "\n") */
    static const std::time_t            timeout;    /* idle client에 PING을 보내기까지의 유예 시간 */ 
    static const std::time_t            cutoff;     /* PING 이후 PONG을 기다리는 유예 시간 */

    /* ISUPPORT 파라미터 */
    static const std::string            chantypes;  /* 지원하는 channel type */
    static const std::string            chanlimit;  /* client가 channel type별로 참여할 수 있는 최대 channel 수 */
    static const std::string            prefix;     /* 지원하는 channel membership prefix */
    static const std::string            nicklen;    /* nick 최대 길이 */
    static const std::string            userlen;    /* user 최대 길이 */
    static const std::string            channellen; /* channel 이름 최대 길이 */
    static const std::string            hostlen; 	/* host 최대 길이 */
    static const std::string            kicklen; 	/* kick 사유 최대 길이 */
    static const std::string            topiclen; 	/* topic 최대 길이 */

    private:
    int                                 listenfd;
    const std::string                   password;
    EventManager                       kqmanager;
    bool                                interrupt;

    /* 내부 데이터베이스 */
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
