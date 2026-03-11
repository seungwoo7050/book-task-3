#include "inc/Channel.hpp"

#include "inc/Connection.hpp"

#include "inc/debug.hpp"

unsigned Channel::lbit = 1U;   // client 수 제한
unsigned Channel::ibit = 2U;   // invite 전용
unsigned Channel::tbit = 4U;   // operator만 topic 변경
unsigned Channel::kbit = 8U;   // key 필요

unsigned Channel::rdstate() const
{
    return this->state;
}

Channel::Channel(const std::string &channelname, Connection *founder):
state(0U),
clientdb(),
privdb(),
invitedb(),
name(channelname),
limit(0U),
topic(),
key()
{
    this->clientdb.insert(std::pair<int, Connection *>(founder->sockfd, founder));
    this->privdb.insert(std::pair<Connection *, enum CHANOPS>(founder, Channel::OPERATOR));

    #ifndef NDEBUG
    std::cout
    << debug_sgr_params::bold_green
    << "channel |"
    << debug_sgr_params::background_gray
    << name
    << debug_sgr_params::reset
    << debug_sgr_params::bold_green
    << "| has been created"
    << debug_sgr_params::reset
    << std::endl;
    #endif
}

Channel::~Channel()
{
    #ifndef NDEBUG
    std::cout
    << debug_sgr_params::bold_red
    << "channel |"
    << debug_sgr_params::background_gray
    << name
    << debug_sgr_params::reset
    << debug_sgr_params::bold_red
    << "| has been destroyed"
    << debug_sgr_params::reset
    << std::endl;
    #endif
}

void Channel::part(Connection *&client)
{
    if (this->invitedb.find(client->sockfd) != this->invitedb.end())
    {
        this->invitedb.erase(client->sockfd);
    }

    if (this->privdb.find(client) != this->privdb.end())
    {
        this->privdb.erase(client);
    }

    if (this->clientdb.find(client->sockfd) != this->clientdb.end())
    {
        this->clientdb.erase(client->sockfd);
    }
}
