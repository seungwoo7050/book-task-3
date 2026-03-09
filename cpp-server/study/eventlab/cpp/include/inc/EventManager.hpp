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
    /* registers for a single event; returns -1 on error */
    int                         listen_event(const int ident, EventType type);

    /* returns a non-blocking listening socket descriptor
    bound to the specified port; -1 on error. */
    static int                  open_listenfd(const char *portstr);

    /* returns a non-blocking connection socket descriptor;
    -1 on error. */
    int                         accept_node(const int listenfd, std::string &ipaddr);

    /* returns number of kernel-detected events. returns -1 on error
    newq: newly accepted sockets during previous event loop cycle -- enable reads; disable writes
    sendq: sockets w/ data to send for current elc -- enable writes
    sentq: sockets w/ data sent during previous elc -- disable writes */
    int                         retrieve_events(std::deque<int> &newq,
                                    std::set<int> &sendq,
                                    std::deque<int> &sentq,
                                    std::vector<Event> &events);

    void                        on_disconnect(std::size_t count = 2);

    private:
    /* adjust eventlist capacity */
    void                        _adjust_capacity();

    public:
    EventManager();
    ~EventManager();

    private:
    EventManager(const EventManager &other);              /* delete */
    EventManager   &operator=(const EventManager &rhs);   /* delete */

};
