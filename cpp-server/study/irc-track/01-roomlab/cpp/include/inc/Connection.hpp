#pragma once

#include <sys/socket.h>
#include <string>
#include <ctime>

#include "Channel.hpp"

class Connection
{
    public:
    std::string         recvbuf; // 잘린 응답 조각 
    std::string         sendbuf; // 전송 대기 버퍼

    std::string         ipaddr;    
    const int           sockfd;
    std::string         nickname;   // 최대 9자. 넘기면 IP를 대신 저장
    std::string         servername;
    std::string         hostname;
    std::string         username;
    std::time_t         timestamp;
    unsigned            membership;

    std::map<std::string, Channel *> chandb;

    // TODO: 모든 flag를 하나의 bit field로 옮기기
    bool                is_doomed;
    bool                is_pinged;
    bool                is_authed; // PASS 완료
    bool                is_registered; // NICK USER QUIT 완료 

    public:
    int                 state;

    public:
    Connection(const int fd, const std::string &ip);
    ~Connection();
};
