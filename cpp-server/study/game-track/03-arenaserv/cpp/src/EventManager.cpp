#include "inc/EventManager.hpp"

/* getaddrinfo(3) */
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <iostream>
#include <arpa/inet.h>  // inet_ntoa(3)
#include <fcntl.h>      // fcntl(2)
#include <unistd.h>     // close(3)
#include <cerrno>
#include <cstring>      // std::memset
#include <stdexcept>
#include <limits>

#if defined(__linux__)
#include <sys/signalfd.h>
#include <sys/ioctl.h>
#include <signal.h>
#endif

namespace
{
#if defined(__APPLE__)
	EventManager::EventType to_event_type(const short filter)
	{
		switch (filter)
		{
			case EVFILT_SIGNAL:
				return EventManager::EventType::Signal;
			case EVFILT_READ:
				return EventManager::EventType::Read;
			case EVFILT_WRITE:
				return EventManager::EventType::Write;
			default:
				return EventManager::EventType::Read;
		}
	}
#elif defined(__linux__)
	uint32_t base_events()
	{
		uint32_t events = EPOLLIN;
		#ifdef EPOLLRDHUP
		events |= EPOLLRDHUP;
		#endif
		return events;
	}

	bool is_fd_open(const int fd)
	{
		return fcntl(fd, F_GETFD) != -1;
	}

	int epoll_update(const int epfd, const int fd, const uint32_t events)
	{
		struct epoll_event ev;
		std::memset(&ev, 0, sizeof(ev));
		ev.data.fd = fd;
		ev.events = events;
		if (epoll_ctl(epfd, EPOLL_CTL_MOD, fd, &ev) == 0)
			return 0;
		if (errno == EBADF && !is_fd_open(fd))
			return 0;
		if (errno != ENOENT)
			return -1;
		if (epoll_ctl(epfd, EPOLL_CTL_ADD, fd, &ev) == 0)
			return 0;
		if (errno == EBADF && !is_fd_open(fd))
			return 0;
		return -1;
	}

	std::size_t available_read_bytes(const int fd)
	{
		int bytes = 0;
		if (ioctl(fd, FIONREAD, &bytes) == -1)
			return 0;
		if (bytes < 0)
			return 0;
		return static_cast<std::size_t>(bytes);
	}

	int socket_error_code(const int fd)
	{
		int error = 0;
		socklen_t len = sizeof(error);
		if (getsockopt(fd, SOL_SOCKET, SO_ERROR, &error, &len) < 0)
			return 0;
		return error;
	}
#endif
}

int EventManager::listen_event(const int ident, const EventType type)
{
#if defined(__APPLE__)
	short filter;
	switch (type)
	{
		case EventType::Signal:
			filter = EVFILT_SIGNAL;
			break;
		case EventType::Read:
			filter = EVFILT_READ;
			break;
		case EventType::Write:
			filter = EVFILT_WRITE;
			break;
		default:
			return -1;
	}

	const unsigned short flags = EV_ADD | EV_ENABLE;
	struct kevent ev;
	EV_SET(&ev, ident, filter, flags, 0, 0, NULL);

	++this->nevents;
	return kevent(this->kq, &ev, 1, NULL, 0, NULL);
#elif defined(__linux__)
	if (type == EventType::Signal)
	{
		if (this->signal_fd != -1)
			return 0;

		sigset_t mask;
		sigemptyset(&mask);
		sigaddset(&mask, ident);

		int sfd = signalfd(-1, &mask, SFD_NONBLOCK | SFD_CLOEXEC);
		if (sfd == -1)
			return -1;

		struct epoll_event ev;
		std::memset(&ev, 0, sizeof(ev));
		ev.data.fd = sfd;
		ev.events = EPOLLIN;
		if (epoll_ctl(this->epfd, EPOLL_CTL_ADD, sfd, &ev) < 0)
		{
			close(sfd);
			this->signal_fd = -1;
			return -1;
		}

		this->signal_fd = sfd;
		++this->nevents;
		this->_adjust_capacity();
		return 0;
	}

	uint32_t events = 0;
	if (type == EventType::Read)
		events = base_events();
	else if (type == EventType::Write)
		events = base_events() | EPOLLOUT;
	else
		return -1;

	struct epoll_event ev;
	std::memset(&ev, 0, sizeof(ev));
	ev.data.fd = ident;
	ev.events = events;
	if (epoll_ctl(this->epfd, EPOLL_CTL_ADD, ident, &ev) < 0)
		return -1;

	++this->nevents;
	this->_adjust_capacity();
	return 0;
#else
	(void)ident;
	(void)type;
	return -1;
#endif
}

int EventManager::open_listenfd(const char *portstr)
{
	addrinfo hints;
	std::memset(&hints, 0, sizeof(addrinfo));

	hints.ai_family = AF_INET;        	// AF_UNSPEC 대신 IPv4만 사용한다. 그렇지 않으면 EINVAL이 날 수 있다.
	hints.ai_socktype = SOCK_STREAM;    // SOCK_STREAM을 사용한다.
	hints.ai_protocol = IPPROTO_TCP;    // TCP를 사용한다.

	// 모든 주소를 허용하고, 로컬 IPv를 사용하며, 숫자 port로 연결한다.
	hints.ai_flags = AI_PASSIVE | AI_ADDRCONFIG | AI_NUMERICSERV;

	addrinfo *listp = NULL;
	if (getaddrinfo(NULL, portstr, &hints, &listp) != 0)
	{
		return -1;
	}

	int listenfd = -1;
	addrinfo *p = listp;
	for (; p; p = p->ai_next)
	{
		if ((listenfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) < 0)
			continue; // socket 생성에 실패했으니 다음 후보를 시도한다.

		int optval = 1;
		if (setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(int)) < 0  // bind 시 "Address already in use" 오류를 줄이기 위해 설정한다.
			|| bind(listenfd, p->ai_addr, p->ai_addrlen) < 0)
		{
			close(listenfd);
			continue;
		}

		break;
	}

	freeaddrinfo(listp);    // 참고로 freeaddrinfo(NULL)은 안전하다.
	if (!p) // 어떤 주소도 열리지 않았으므로 오류를 반환한다.
		return -1;
	
	if (listen(listenfd, 1024) < 0) // fd를 accept 가능한 listening socket으로 전환한다.
	{
		close(listenfd);
		return -1;
	}

	if (fcntl(listenfd, F_SETFL, O_NONBLOCK) == -1)
	{
		close(listenfd);
		return -1;
	}

	return listenfd;
}

int EventManager::accept_node(const int listenfd, std::string &ipaddr)
{
	sockaddr_storage	client_addr = {};
	socklen_t			addr_size = sizeof(client_addr);
	
	int clientfd = accept(listenfd, reinterpret_cast<sockaddr *>(&client_addr), &addr_size);
	if (clientfd == -1)
	{
		return -1;
	}

	if (fcntl(clientfd, F_SETFL, O_NONBLOCK) == -1)
	{
		close(clientfd);
		return -1;
	}

	if (client_addr.ss_family == AF_INET)
	{
		sockaddr_in *ipv4 = reinterpret_cast<sockaddr_in *>(&client_addr);
		in_addr addr = ipv4->sin_addr;
		ipaddr = inet_ntoa(addr);
	}
	
	return clientfd;
}

int EventManager::retrieve_events(std::deque<int> &newq,
	std::set<int> &sendq,
	std::deque<int> &sentq,
	std::vector<Event> &events,
	int timeout_ms)
{
	const std::size_t newqsize = newq.size(), sendqsize = sendq.size(), sentqsize = sentq.size();

#if defined(__APPLE__)
	for (std::size_t i = 0; i < newqsize; ++i)
	{
		int sockfd = newq.front();
		EV_SET(&this->eventlist[i], sockfd, EVFILT_READ, EV_ADD | EV_ENABLE | EV_CLEAR, 0, 0, NULL);
		EV_SET(&this->eventlist[newqsize + i], sockfd, EVFILT_WRITE, EV_ADD | EV_DISABLE, 0, 0, NULL);
		newq.pop_front();
	}

	this->nevents += newqsize * 2; // 다소 비효율적이어도 여기서 write event 수를 함께 센다.
	this->_adjust_capacity();

	std::set<int>::iterator cur = sendq.begin();
	for (std::size_t i = newqsize * 2; i < newqsize * 2 + sendqsize; ++i)
	{
		std::set<int>::iterator pre = cur++;
		int sockfd = *pre;
		EV_SET(&this->eventlist[i], sockfd, EVFILT_WRITE, EV_ENABLE, 0, 0, NULL);
		sendq.erase(pre);
	}

	for (std::size_t i = newqsize * 2 + sendqsize; i < newqsize * 2 + sendqsize + sentqsize; ++i)
	{
		int sockfd = sentq.front();
		EV_SET(&this->eventlist[i], sockfd, EVFILT_WRITE, EV_DISABLE, 0, 0, NULL);
		sentq.pop_back();
	}

	timespec time = {};
	time.tv_sec = timeout_ms / 1000;
	time.tv_nsec = static_cast<long>(timeout_ms % 1000) * 1000000L;
	int nev = kevent(this->kq,
						this->eventlist.data(),
						newqsize * 2 + sendqsize + sentqsize,
						this->eventlist.data(),
						this->nevents,
						&time);
	if (nev < 0)
	{
		throw std::runtime_error("kevent: ");
	}

	events.clear();
	events.reserve(static_cast<std::size_t>(nev));
	for (int i = 0; i < nev; ++i)
	{
		const struct kevent &kev = this->eventlist[i];
		Event event;
		event.fd = static_cast<int>(kev.ident);
		event.type = to_event_type(kev.filter);
		event.eof = (kev.flags & EV_EOF) != 0;
		event.error = (kev.flags & EV_ERROR) != 0;
		event.error_code = event.error ? static_cast<int>(kev.data) : 0;
		event.data = kev.data < 0 ? 0 : static_cast<std::size_t>(kev.data);
		events.push_back(event);
	}

	return static_cast<int>(events.size());
#elif defined(__linux__)
	for (std::size_t i = 0; i < newqsize; ++i)
	{
		int sockfd = newq.front();
		if (epoll_update(this->epfd, sockfd, base_events()) < 0)
		{
			throw std::runtime_error("epoll_ctl: ");
		}
		newq.pop_front();
	}

	this->nevents += static_cast<int>(newqsize);
	this->_adjust_capacity();

	std::set<int>::iterator cur = sendq.begin();
	for (std::size_t i = 0; i < sendqsize; ++i)
	{
		std::set<int>::iterator pre = cur++;
		int sockfd = *pre;
		if (epoll_update(this->epfd, sockfd, base_events() | EPOLLOUT) < 0)
		{
			throw std::runtime_error("epoll_ctl: ");
		}
		sendq.erase(pre);
	}

	for (std::size_t i = 0; i < sentqsize; ++i)
	{
		int sockfd = sentq.front();
		if (epoll_update(this->epfd, sockfd, base_events()) < 0)
		{
			throw std::runtime_error("epoll_ctl: ");
		}
		sentq.pop_back();
	}

	int nev = epoll_wait(this->epfd, this->eventlist.data(), this->capacity, timeout_ms);
	if (nev < 0)
	{
		throw std::runtime_error("epoll_wait: ");
	}

	events.clear();
	events.reserve(static_cast<std::size_t>(nev) * 2);
	for (int i = 0; i < nev; ++i)
	{
		const struct epoll_event &ev = this->eventlist[i];
		const int fd = ev.data.fd;

		if (this->signal_fd != -1 && fd == this->signal_fd)
		{
			signalfd_siginfo info;
			std::memset(&info, 0, sizeof(info));
			if (read(this->signal_fd, &info, sizeof(info)) >= 0)
			{
				Event event;
				event.fd = static_cast<int>(info.ssi_signo);
				event.type = EventType::Signal;
				event.data = 0;
				event.eof = false;
				event.error = false;
				event.error_code = 0;
				events.push_back(event);
			}
			continue;
		}

		const bool has_read = (ev.events & EPOLLIN) != 0;
		const bool has_write = (ev.events & EPOLLOUT) != 0;
		const bool has_error = (ev.events & EPOLLERR) != 0;
		const bool has_hup = (ev.events & EPOLLHUP) != 0;
		bool has_rdhup = false;
		#ifdef EPOLLRDHUP
		has_rdhup = (ev.events & EPOLLRDHUP) != 0;
		#endif

		const bool is_eof = has_hup || has_rdhup;
		const int error_code = has_error ? socket_error_code(fd) : 0;

		if (has_read || is_eof || has_error)
		{
			Event event;
			event.fd = fd;
			event.type = EventType::Read;
			event.data = available_read_bytes(fd);
			event.eof = is_eof;
			event.error = has_error;
			event.error_code = error_code;
			events.push_back(event);
		}

		if (has_write)
		{
			Event event;
			event.fd = fd;
			event.type = EventType::Write;
			event.data = std::numeric_limits<std::size_t>::max();
			event.eof = is_eof;
			event.error = has_error;
			event.error_code = error_code;
			events.push_back(event);
		}
	}

	return static_cast<int>(events.size());
#else
	(void)newq;
	(void)sendq;
	(void)sentq;
	(void)events;
	return -1;
#endif
}

EventManager::EventManager()
#if defined(__APPLE__)
: eventlist(100), kq(kqueue()), capacity(100), nevents(0)
#elif defined(__linux__)
: eventlist(100), epfd(epoll_create1(0)), signal_fd(-1), capacity(100), nevents(0)
#endif
{
#if defined(__APPLE__)
	if (this->kq == -1)
	{
		throw std::runtime_error("failed to create a kernel event queue: ");
	}
#elif defined(__linux__)
	if (this->epfd == -1)
	{
		throw std::runtime_error("failed to create an epoll instance: ");
	}
#endif
}

EventManager::~EventManager()
{
#if defined(__APPLE__)
	if (this->kq != -1)
	{
		close(this->kq);
	}
#elif defined(__linux__)
	if (this->signal_fd != -1)
	{
		close(this->signal_fd);
	}
	if (this->epfd != -1)
	{
		close(this->epfd);
	}
#endif
}

void EventManager::_adjust_capacity()
{
	if (this->nevents > this->capacity / 2)
	{
		this->capacity *= 2;
		this->eventlist.resize(capacity);
	}
	else if (this->nevents < this->capacity / 3 && this->capacity > 100)
	{
		this->capacity /= 2;
		this->eventlist.resize(capacity);
	}
}

void EventManager::on_disconnect(std::size_t count)
{
#if defined(__linux__)
	count = 1;
#endif
	if (count == 0)
		return;
	if (this->nevents >= static_cast<int>(count))
		this->nevents -= static_cast<int>(count);
	else
		this->nevents = 0;
}
