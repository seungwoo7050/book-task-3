#pragma once

#if defined(__APPLE__)
/* kqueue(2) */
#include <sys/event.h>
#include <sys/time.h>
#elif defined(__linux__)
/* epoll(7) */
#include <sys/epoll.h>
#endif

#include <vector>
#include <deque>
#include <set>
#include <cstddef>
#include <string>

class EventManager
{
    public:
    enum class EventType
    {
        Signal,
        Read,
        Write
    };

    struct Event
    {
        int             fd;
        EventType       type;
        std::size_t     data;
        bool            eof;
        bool            error;
        int             error_code;
    };

    private:
#if defined(__APPLE__)
    std::vector<struct kevent>  eventlist;
    const int                   kq;
#elif defined(__linux__)
    std::vector<struct epoll_event> eventlist;
    int                             epfd;
    int                             signal_fd;
#endif
    int                             capacity;
    int                             nevents;

    public:
    /* 단일 이벤트를 등록한다. 실패하면 -1을 반환한다. */
    int                         listen_event(const int ident, EventType type);

    /* 지정한 port에 bind된 non-blocking listening socket descriptor를 반환한다.
    실패하면 -1을 반환한다. */
    static int                  open_listenfd(const char *portstr);

    /* non-blocking connection socket descriptor를 반환한다.
    실패하면 -1을 반환한다. */
    int                         accept_node(const int listenfd, std::string &ipaddr);

    /* kernel이 감지한 이벤트 수를 반환한다. 실패하면 -1을 반환한다.
    newq: 직전 event loop cycle에서 새로 accept한 socket들로, read를 켜고 write는 끈다.
    sendq: 현재 cycle에서 보낼 데이터가 있는 socket들로, write를 켠다.
    sentq: 직전 cycle에서 전송을 마친 socket들로, write를 끈다. */
    int                         retrieve_events(std::deque<int> &newq,
                                    std::set<int> &sendq,
                                    std::deque<int> &sentq,
                                    std::vector<Event> &events);

    void                        on_disconnect(std::size_t count = 2);

    private:
    /* eventlist capacity를 조정한다. */
    void                        _adjust_capacity();

    public:
    EventManager();
    ~EventManager();

    private:
    EventManager(const EventManager &other);              /* 복사 금지 */
    EventManager   &operator=(const EventManager &rhs);   /* 복사 금지 */

};
