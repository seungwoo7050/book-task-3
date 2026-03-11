#include "inc/Server.hpp"

#include "inc/utils.hpp"

#include <algorithm>
#include <cerrno>
#include <chrono>
#include <csignal>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <exception>
#include <sstream>
#include <stdexcept>
#include <unistd.h>
#include <vector>

const std::string Server::servername = "arenaserv";
const std::size_t Server::bufsiz = 4096UL;
const std::uint64_t Server::tick_interval_ms = 100ULL;

Server::Client::Client()
    : fd(-1), ipaddr(), recvbuf(), sendbuf(), token(), doomed(false)
{
}

Server::Client::Client(int socket_fd, const std::string &ip)
    : fd(socket_fd), ipaddr(ip), recvbuf(), sendbuf(), token(), doomed(false)
{
}

Server::Server(const char *portstr)
    : listenfd(validate_port(portstr) ? -1 : throw std::invalid_argument("inappropriate port number")),
      manager(),
      interrupt(false),
      clients(),
      token_to_fd(),
      sendq(),
      engine(),
      last_tick_ms(current_millis())
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
        throw std::runtime_error("failed to register arenaserv events: ");

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

std::uint64_t Server::current_millis()
{
    return static_cast<std::uint64_t>(
        std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::steady_clock::now().time_since_epoch()).count());
}

void Server::run_event_loop()
{
    static std::deque<int> newq;
    static std::deque<int> sentq;
    static std::vector<EventManager::Event> events;

    int nev = this->manager.retrieve_events(newq, this->sendq, sentq, events, 50);
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
            const std::size_t maxlen = std::min<std::size_t>(event.data == 0 ? bufsiz : event.data, bufsiz);
            ssize_t bytes = this->read_packet(client, maxlen);
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

    this->pump_ticks();
}

void Server::pump_ticks()
{
    const std::uint64_t now = current_millis();
    while (this->last_tick_ms + tick_interval_ms <= now)
    {
        this->engine.advance_one_tick();
        this->dispatch_engine_events();
        this->last_tick_ms += tick_interval_ms;
    }
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
}

void Server::disconnect(int sockfd)
{
    std::map<int, Client>::iterator found = this->clients.find(sockfd);
    if (found == this->clients.end())
        return;

    if (!found->second.token.empty())
    {
        this->engine.disconnect_player(found->second.token);
        this->token_to_fd.erase(found->second.token);
    }

    close(found->second.fd);
    found->second.fd = -1;
    this->sendq.erase(sockfd);
    this->clients.erase(found);
    this->manager.on_disconnect();
}

ssize_t Server::read_packet(Client &client, std::size_t maxlen)
{
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
    std::istringstream iss(line);
    std::vector<std::string> tokens;
    std::string token;
    while (iss >> token)
        tokens.push_back(token);
    if (tokens.empty())
        return;

    std::string command = tokens[0];
    std::transform(command.begin(), command.end(), command.begin(), ::toupper);

    if (command == "HELLO")
    {
        if (tokens.size() != 2)
            this->send_error(client, "invalid_input", "usage: HELLO <nick>");
        else
            this->handle_hello(client, tokens[1]);
        return;
    }
    if (command == "QUEUE")
    {
        if (tokens.size() != 1)
            this->send_error(client, "invalid_input", "usage: QUEUE");
        else
            this->handle_queue(client);
        return;
    }
    if (command == "READY")
    {
        if (tokens.size() != 1)
            this->send_error(client, "invalid_input", "usage: READY");
        else
            this->handle_ready(client);
        return;
    }
    if (command == "INPUT")
    {
        this->handle_input(client, line);
        return;
    }
    if (command == "REJOIN")
    {
        if (tokens.size() != 2)
            this->send_error(client, "invalid_input", "usage: REJOIN <token>");
        else
            this->handle_rejoin(client, tokens[1]);
        return;
    }
    if (command == "LEAVE")
    {
        if (tokens.size() != 1)
            this->send_error(client, "invalid_input", "usage: LEAVE");
        else
            this->handle_leave(client);
        return;
    }
    if (command == "PING")
    {
        if (tokens.size() != 2)
            this->send_error(client, "invalid_input", "usage: PING <ms>");
        return;
    }
    if (command == "QUIT")
    {
        this->handle_leave(client);
        client.doomed = true;
        return;
    }

    this->send_error(client, "unknown_command", "unsupported command");
}

void Server::handle_hello(Client &client, const std::string &nick)
{
    if (!client.token.empty())
    {
        this->send_error(client, "bad_state", "already registered");
        return;
    }

    MatchEngine::Error error;
    std::string token;
    if (!this->engine.register_player(nick, token, error))
    {
        this->send_error(client, error.code, error.message);
        return;
    }

    client.token = token;
    this->token_to_fd[token] = client.fd;
    this->dispatch_engine_events();
}

void Server::handle_queue(Client &client)
{
    if (client.token.empty())
    {
        this->send_error(client, "unknown_session", "HELLO must complete before QUEUE");
        return;
    }

    MatchEngine::Error error;
    if (!this->engine.queue_player(client.token, error))
    {
        this->send_error(client, error.code, error.message);
        return;
    }
    this->dispatch_engine_events();
}

void Server::handle_ready(Client &client)
{
    if (client.token.empty())
    {
        this->send_error(client, "unknown_session", "HELLO must complete before READY");
        return;
    }

    MatchEngine::Error error;
    if (!this->engine.ready_player(client.token, error))
    {
        this->send_error(client, error.code, error.message);
        return;
    }
    this->dispatch_engine_events();
}

void Server::handle_input(Client &client, const std::string &line)
{
    if (client.token.empty())
    {
        this->send_error(client, "unknown_session", "HELLO must complete before INPUT");
        return;
    }

    std::istringstream iss(line);
    std::string command;
    std::string seq_token;
    std::string dx_token;
    std::string dy_token;
    std::string facing_token;
    std::string fire_token;
    if (!(iss >> command >> seq_token >> dx_token >> dy_token >> facing_token >> fire_token))
    {
        this->send_error(client, "invalid_input", "usage: INPUT <seq> <dx> <dy> <facing> <fire>");
        return;
    }

    char *endptr = NULL;
    long seq = std::strtol(seq_token.c_str(), &endptr, 10);
    if (*endptr != '\0')
    {
        this->send_error(client, "invalid_input", "seq must be an integer");
        return;
    }
    long dx = std::strtol(dx_token.c_str(), &endptr, 10);
    if (*endptr != '\0')
    {
        this->send_error(client, "invalid_input", "dx must be an integer");
        return;
    }
    long dy = std::strtol(dy_token.c_str(), &endptr, 10);
    if (*endptr != '\0')
    {
        this->send_error(client, "invalid_input", "dy must be an integer");
        return;
    }
    long fire = std::strtol(fire_token.c_str(), &endptr, 10);
    if (*endptr != '\0')
    {
        this->send_error(client, "invalid_input", "fire must be 0 or 1");
        return;
    }

    MatchEngine::Error error;
    MatchEngine::Input input(static_cast<int>(seq), static_cast<int>(dx), static_cast<int>(dy), facing_token.empty() ? 'N' : facing_token[0], fire != 0);
    if (!this->engine.submit_input(client.token, input, error))
    {
        this->send_error(client, error.code, error.message);
        return;
    }
}

void Server::handle_rejoin(Client &client, const std::string &token)
{
    if (!client.token.empty())
    {
        this->send_error(client, "bad_state", "connection already owns a session");
        return;
    }

    MatchEngine::Error error;
    if (!this->engine.rejoin_player(token, error))
    {
        this->send_error(client, error.code, error.message);
        return;
    }

    client.token = token;
    this->token_to_fd[token] = client.fd;
    this->dispatch_engine_events();
}

void Server::handle_leave(Client &client)
{
    if (client.token.empty())
        return;

    MatchEngine::Error error;
    this->engine.leave_player(client.token, error);
    this->token_to_fd.erase(client.token);
    client.token.clear();
}

void Server::dispatch_engine_events()
{
    const std::vector<MatchEngine::Event> events = this->engine.drain_events();
    for (std::vector<MatchEngine::Event>::const_iterator it = events.begin(); it != events.end(); ++it)
    {
        if (it->scope == MatchEngine::EventScope::Single)
        {
            std::map<std::string, int>::iterator found = this->token_to_fd.find(it->token);
            if (found == this->token_to_fd.end())
                continue;
            std::map<int, Client>::iterator client_it = this->clients.find(found->second);
            if (client_it == this->clients.end())
                continue;
            this->queue_reply(client_it->second, it->line + "\r\n");
            continue;
        }

        const std::vector<std::string> room_tokens = this->engine.room_tokens();
        for (std::vector<std::string>::const_iterator token_it = room_tokens.begin(); token_it != room_tokens.end(); ++token_it)
        {
            std::map<std::string, int>::iterator found = this->token_to_fd.find(*token_it);
            if (found == this->token_to_fd.end())
                continue;
            std::map<int, Client>::iterator client_it = this->clients.find(found->second);
            if (client_it == this->clients.end())
                continue;
            this->queue_reply(client_it->second, it->line + "\r\n");
        }
    }
}

void Server::queue_reply(Client &client, const std::string &reply)
{
    if (client.doomed)
        return;
    client.sendbuf += reply;
    this->sendq.insert(client.fd);
}

void Server::send_error(Client &client, const std::string &code, const std::string &message)
{
    this->queue_reply(client, "ERROR " + code + " " + message + "\r\n");
}
