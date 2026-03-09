#include "inc/Connection.hpp"

#include "inc/debug.hpp"

#include <unistd.h>     // close(3)
#include <sys/socket.h> // getsockopt(2) 
#include <ctime>

Connection::Connection(const int fd, const std::string &ip):
recvbuf(),
sendbuf(),
ipaddr(ip),
sockfd(fd),
nickname(),
servername(),
hostname(),
username(),
timestamp(std::time(NULL)),
membership(0U),
chandb(),
is_doomed(false),
is_pinged(false),
is_authed(false),
is_registered(false)
{
    #ifndef NDEBUG
    std::cout
    << debug_sgr_params::bold_green
    << "connection |"
    << debug_sgr_params::background_gray
    << sockfd
    << debug_sgr_params::reset
    << debug_sgr_params::bold_green
    << "| has been created"
    << debug_sgr_params::reset
    << std::endl;
    #endif
}

Connection::~Connection()
{
    close(sockfd);

    #ifndef NDEBUG
    std::cout
    << debug_sgr_params::bold_red
    << "connection |"
    << debug_sgr_params::background_gray
    << sockfd
    << debug_sgr_params::reset
    << debug_sgr_params::bold_red
    << "| has been destroyed"
    << debug_sgr_params::reset
    << std::endl;
    #endif
}
