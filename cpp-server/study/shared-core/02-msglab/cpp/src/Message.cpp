#include "inc/Message.hpp"
#include "inc/Parser.hpp"
#include <string>
#include <sstream>

static const std::string translator[Message::COMM_CNT] = {
    "PASS",
    "NICK",
    "USER",
    "JOIN",
    "PART",
    "PRIVMSG",
    "NOTICE",
    "KICK",
    "INVITE",
    "TOPIC",
    "MODE",
    "PING",
    "PONG",
    "QUIT",
    "CAP",
    "UNK"
};

Message::Message(const std::string &stream): // stream이 비어 있지 않다고 가정한다.
comm(UNK),
prefix(),
command(),
params()
{
    std::istringstream  iss(stream);
    std::string         token;

    if (stream.at(0) == ':')
    {
        iss.get();
        if (!std::getline(iss, token, ' ').fail())
            this->prefix = token;
        token.clear();
        if (iss.peek() == std::istringstream::traits_type::eof())
            return;
    }

    while (token.empty())
    {
        if (std::getline(iss, token, ' ').fail())
            break;
    }

    this->command = token;
    Parser::toupper(this->command);

    for (std::size_t i = 0; i < COMM_CNT; ++i)
    {
        if (translator[i] == this->command)
        {
            this->comm = static_cast<label>(i);
            break;
        }
    }

    while (iss.peek() != std::istringstream::traits_type::eof())
    {
        if (iss.peek() == ':')
        {
            iss.get();
            if (!std::getline(iss, token, '\0').fail())
                this->params.push_back(token);
            break;
        }
        if (!std::getline(iss, token, ' ').fail() && !token.empty())
            this->params.push_back(token);
    }
}
