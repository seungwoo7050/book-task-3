#include "inc/Server.hpp"

#include "inc/utils.hpp"

#include <algorithm>
#include <cerrno>
#include <csignal>
#include <cstring>
#include <deque>
#include <exception>
#include <stdexcept>
#include <unistd.h>
#include <vector>

const std::string Server::servername = "eventlab";
const std::size_t Server::bufsiz = 4096UL;
const std::time_t Server::timeout = 2L;
const std::time_t Server::cutoff = 5L;

Server::Client::Client()
    : fd(-1), ipaddr(), recvbuf(), sendbuf(), timestamp(0), pinged(false), doomed(false)
{
}

Server::Client::Client(int socket_fd, const std::string &ip)
    : fd(socket_fd), ipaddr(ip), recvbuf(), sendbuf(), timestamp(std::time(NULL)), pinged(false), doomed(false)
{
}

Server::Server(const char *portstr)
    : listenfd(validate_port(portstr) ? -1 : throw std::invalid_argument("inappropriate port number")),
      manager(),
      interrupt(false),
      clients(),
      sendq()
{
    if ((this->listenfd = EventManager::open_listenfd(portstr)) == -1)
        throw std::runtime_error("failed to open a listening port: ");
}

Server::~Server()
{
    if (this->listenfd != -1)
        close(this->listenfd);

    for (std::map<int, Client>::iterator it = this->clients.begin(); it != this->clients.end(); ++it)
    {
        if (it->second.fd != -1)
            close(it->second.fd);
    }
}

void Server::run()
{
    if (this->manager.listen_event(SIGINT, EventManager::EventType::Signal) < 0
        || this->manager.listen_event(this->listenfd, EventManager::EventType::Read) < 0)
        throw std::runtime_error("failed to register eventlab events: ");

    while (!this->interrupt)
        this->run_event_loop();
}

bool Server::validate_port(const char *portstr)
{
    char *endptr = NULL;
    long port = std::strtol(portstr, &endptr, 10);
    if (*endptr != '\0')
        return false;
    return port > 0 && port < 65536;
}

void Server::run_event_loop()
{
    static std::deque<int> newq;
    static std::deque<int> sentq;
    static std::vector<EventManager::Event> events;

    this->keep_alive();

    int nev = this->manager.retrieve_events(newq, this->sendq, sentq, events);
    for (int i = 0; i < nev; ++i)
    {
        const EventManager::Event &event = events[static_cast<std::size_t>(i)];
        const int ident = event.fd;

        if (event.error)
        {
            if (ident == this->listenfd)
                throw std::runtime_error("listening socket failed: ");
            this->disconnect(ident);
            continue;
        }

        if (event.type == EventManager::EventType::Signal)
        {
            this->interrupt = true;
            continue;
        }

        if (event.type == EventManager::EventType::Read)
        {
            if (ident == this->listenfd)
            {
                std::string ipaddr;
                int sockfd = this->manager.accept_node(this->listenfd, ipaddr);
                if (sockfd != -1)
                {
                    this->accept_connection(sockfd, ipaddr);
                    newq.push_back(sockfd);
                }
                continue;
            }

            std::map<int, Client>::iterator found = this->clients.find(ident);
            if (found == this->clients.end())
                continue;

            if (event.eof && event.data == 0)
            {
                this->disconnect(ident);
                continue;
            }

            Client &client = found->second;
            ssize_t bytes = this->read_packet(client, std::min<std::size_t>(event.data == 0 ? bufsiz : event.data, bufsiz));
            if (bytes <= 0)
            {
                if (event.eof || bytes < 0)
                    this->disconnect(ident);
                continue;
            }

            this->process_input(client);
            continue;
        }

        if (event.type == EventManager::EventType::Write)
        {
            std::map<int, Client>::iterator found = this->clients.find(ident);
            if (found == this->clients.end())
                continue;

            Client &client = found->second;
            ssize_t bytes = this->send_packet(client);
            if (bytes < 0)
            {
                this->disconnect(ident);
                continue;
            }

            if (client.doomed && client.sendbuf.empty())
                this->disconnect(ident);
            else
                sentq.push_back(ident);
        }
    }
}

void Server::keep_alive()
{
    const std::time_t now = std::time(NULL);
    if (now < 0)
        return;

    std::vector<int> stale;
    for (std::map<int, Client>::iterator it = this->clients.begin(); it != this->clients.end(); ++it)
    {
        Client &client = it->second;
        if (!client.pinged && now - client.timestamp > timeout)
        {
            client.pinged = true;
            this->queue_reply(client, "PING :idle-check\r\n");
        }
        else if (client.pinged && now - client.timestamp > cutoff)
        {
            stale.push_back(client.fd);
        }
    }

    for (std::vector<int>::const_iterator it = stale.begin(); it != stale.end(); ++it)
        this->disconnect(*it);
}

void Server::accept_connection(int sockfd, const std::string &ipaddr)
{
    Client client(sockfd, ipaddr);
    std::pair<std::map<int, Client>::iterator, bool> inserted =
        this->clients.insert(std::make_pair(sockfd, client));
    if (!inserted.second)
    {
        close(sockfd);
        return;
    }

    this->queue_reply(inserted.first->second, "WELCOME " + ipaddr + "\r\n");
}

void Server::disconnect(int sockfd)
{
    std::map<int, Client>::iterator found = this->clients.find(sockfd);
    if (found == this->clients.end())
        return;

    close(found->second.fd);
    found->second.fd = -1;
    this->sendq.erase(sockfd);
    this->clients.erase(found);
    this->manager.on_disconnect();
}

ssize_t Server::read_packet(Client &client, std::size_t maxlen)
{
    client.timestamp = std::time(NULL);
    client.pinged = false;

    char buf[bufsiz + 1];
    std::memset(buf, 0, sizeof(buf));
    ssize_t bytes = utils::full_recvn(client.fd, buf, maxlen);
    if (bytes <= 0)
        return bytes;

    client.recvbuf.append(buf, static_cast<std::size_t>(bytes));
    return bytes;
}

ssize_t Server::send_packet(Client &client)
{
    if (client.sendbuf.empty())
        return 0;

    ssize_t bytes = utils::full_sendn(client.fd, client.sendbuf.c_str(), client.sendbuf.size());
    if (bytes < 0)
        return bytes;

    client.sendbuf.clear();
    return bytes;
}

void Server::process_input(Client &client)
{
    for (;;)
    {
        std::size_t pos = client.recvbuf.find('\n');
        if (pos == std::string::npos)
            break;

        std::string line = client.recvbuf.substr(0, pos);
        client.recvbuf.erase(0, pos + 1);
        if (!line.empty() && line[line.size() - 1] == '\r')
            line.erase(line.size() - 1);
        if (line.empty())
            continue;

        this->handle_line(client, line);
    }
}

void Server::handle_line(Client &client, const std::string &line)
{
    if (line == "QUIT")
    {
        this->queue_reply(client, "BYE\r\n");
        client.doomed = true;
        return;
    }

    if (line.compare(0, 4, "PING") == 0)
    {
        std::string token = line.size() > 4 ? line.substr(4) : "";
        if (!token.empty() && token[0] == ' ')
            token.erase(0, 1);
        if (!token.empty() && token[0] == ':')
            token.erase(0, 1);
        this->queue_reply(client, "PONG " + token + "\r\n");
        return;
    }

    this->queue_reply(client, "ECHO " + line + "\r\n");
}

void Server::queue_reply(Client &client, const std::string &reply)
{
    client.sendbuf += reply;
    this->sendq.insert(client.fd);
}
