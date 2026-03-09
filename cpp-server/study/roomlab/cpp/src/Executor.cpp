#include "inc/Executor.hpp"

#include "inc/Connection.hpp"
#include "inc/Server.hpp"
#include "inc/Message.hpp"
#include "inc/macros.hpp"
#include "inc/Parser.hpp"

#include "inc/debug.hpp"
#include "inc/utils.hpp"

#include <cctype>
#include <cstdlib>
#include <ctime>

void Executor::to_doom(Server &server, Connection *&node, const std::string &reply)
{
	node->is_doomed = true;
	node->sendbuf += reply;
	server.sendq.insert(node->sockfd);
}

void Executor::dispatch_packet(Server &server, Connection *&node, const std::string &reply)
{
	if (node->is_doomed)
		return;
	
	node->sendbuf += reply;
	server.sendq.insert(node->sockfd);
}

void Executor::broadcast(Server &server, const std::string &reply)
{
	for (std::list<Connection *>::iterator it = server.nodes.begin(); it != server.nodes.end(); ++it)
	{
		Connection *node = *it;
		if (node->is_registered)
		{
			dispatch_packet(server, node, reply);
		}
	}
}

void Executor::broadcast(Server &server, Channel *&channel, const std::string &reply)
{
	for (std::map<int, Connection *>::iterator it = channel->clientdb.begin(); it != channel->clientdb.end(); ++it)
	{
		Connection *client = it->second;
		dispatch_packet(server, client, reply);
	}
}

void Executor::process(Server &server, Connection *&node, std::vector<Message> &packet)
{
	for (std::vector<Message>::const_iterator it = packet.cbegin(); it != packet.cend(); ++it)
	{
		switch (it->comm)
		{
			case Message::PASS:		_execute_pass(server, node, *it); break;
			case Message::NICK:		_execute_nick(server, node, *it); break;
			case Message::USER:		_execute_user(server, node, *it); break;
			case Message::JOIN:		_execute_join(server, node, *it); break;
      		case Message::PART: 	_execute_part(server, node, *it); break;
			case Message::PRIVMSG:	_execute_privmsg(server, node, *it); break;
			case Message::NOTICE:	_execute_notice(server, node, *it); break;
			case Message::PING: 	_execute_ping(server, node, *it); break;
			case Message::PONG: 	break;	// do nothing
			case Message::QUIT: 	_execute_quit(server, node, *it); break;
			default:
			dispatch_packet(server, node, BUILD_ERR_UNKNOWNCOMMAND(server.servername, node->nickname, it->command));
		}
	}
}

void Executor::_execute_pass(Server &server, Connection *&node, const Message &msg)
{
    std::string rpl;

	if (node->is_authed == true)
	{
        rpl = BUILD_ERR_ALREADYREGISTRED(server.servername, node->nickname);
	}
	else if (msg.params.size() != 1)
	{
        rpl = BUILD_ERR_NEEDMOREPARAMS(server.servername, msg.command);
	}
	else if (msg.params.at(0) != server.password)
	{
		to_doom(server, node, BUILD_ERR_PASSWDMISMATCH(server.servername));
		return;
	}
	else
	{
		node->is_authed = true;
        return ;
	}
	if (!rpl.empty())
		dispatch_packet(server, node, rpl);
}


static bool isSpecialChar(char c) {
	std::string special_chars = "[]\\{}|";
    return special_chars.find(c) != std::string::npos;
}

static bool isValidNickname(const std::string &nickname) {
    if (nickname.empty() || nickname.size() > 30) return false;
    if (!std::isalpha(nickname[0]) && !isSpecialChar(nickname[0])) return false;
	for (size_t i = 1; i < nickname.size(); i++)
		if (!std::isalnum(static_cast<unsigned char>(nickname[i])) && !isSpecialChar(nickname[i]))  return false;
	return true;
}

bool Executor::_isNickInUse(const Server &server, const std::string &nickname) {
	std::map<std::string, std::list<Connection *>::iterator>::const_iterator it = server.nickdb.find(nickname);

	if (it == server.nickdb.cend())
		return false;
	else
		return true;
}

void Executor::_execute_nick(Server &server, Connection *&node, const Message &msg)
{
	std::string rpl;

	if (msg.params.size() != 1)
	{
		rpl = BUILD_ERR_NONICKNAMEGIVEN(server.servername);
		dispatch_packet(server, node, rpl);
		return;
	}
	std::string lower = msg.params[0];
	Parser::tolower(lower);
	if (!node->is_authed)
		rpl = BUILD_ERR_NOTREGISTERED(server.servername, msg.params[0]);
	else if (!isValidNickname(msg.params[0]))
		rpl = BUILD_ERR_ERRONEUSNICKNAME(server.servername, msg.params[0]);
	else if (_isNickInUse(server, lower))
		rpl = BUILD_ERR_NICKNAMEINUSE(server.servername, msg.params[0]);
	else
	{
		if (node->is_registered)
		{
			if (lower == node->nickname)
				return;
			broadcast(server, ":" + node->nickname + " NICK " + msg.params[0] + "\r\n");
			if (server.nickdb.find(node->nickname) != server.nickdb.end())
				server.nickdb.erase(node->nickname);
		}
		node->nickname = lower;
		if (server.sockdb.find(node->sockfd) != server.sockdb.end())
			server.nickdb.insert(std::pair<std::string, std::list<Connection *>::iterator>(lower, server.sockdb.find(node->sockfd)->second));
		if (!node->is_registered)
			return;
	}
	dispatch_packet(server, node, rpl);
}

std::string Executor::_isupport(Server &server, Connection *&node)
{
	std::string res = ":" + server.servername + " 005 " + node->nickname + " ";
	res += "AWAYLEN=1 ";
	res += "-AWAYLEN ";
	res += "CASEMAPPING=ascii ";
	res += "CHANLIMIT=" + server.chanlimit + " ";
	res += "CHANMODE=i,t,k,o,l ";

	res += "CHANNELLEN=" + server.channellen + " ";
	res += "CHANTYPES=" + server.chantypes + " ";
	res += "ELIST=M ";
	res += "-ELIST ";
	res += "EXCEPTS ";

	res += "-EXCEPTS ";
	res += ":are supported by this server\r\n";

	res += ":" + server.servername + " 005 " + node->nickname + " ";
	res += "HOSTLEN=" + server.hostlen + " ";
	res += "INVEX ";
	res += "-INVEX ";
	res += "KICKLEN=" + server.kicklen + " ";
	res += "MAXLIST=itkol:120 ";

	res += "MODES=1 ";
	res += "NICKLEN=" + server.nicklen + " ";
	res += "STATUSMSG=@ ";
	res += "TARGMAX=JOIN:1,PART:1 ";
	res += "TOPICLEN=" + server.topiclen + " ";
	res += "USERLEN=" + server.userlen + " ";
	res += ":are supported by this server\r\n";
	return res;
}

void Executor::_execute_user(Server &server, Connection *&node, const Message &msg)
{
	std::string rpl;
	
	if (!node->is_authed)
		rpl = BUILD_ERR_NOTREGISTERED(server.servername, node->ipaddr);
	else if (msg.params.size() != 4)
		rpl = BUILD_ERR_NEEDMOREPARAMS(server.servername, msg.command);
	else if (node->is_registered)
		rpl = BUILD_ERR_ALREADYREGISTRED(server.servername, node->nickname);
	else
	{
		if (!node->nickname.empty())
		{
			node->is_registered = true;
			if (msg.params[0].size() > 11)
				node->username = "~" + msg.params[0].substr(0, 11);
			else
				node->username = "~" + msg.params[0];
			if (msg.params[1] == "0")
				node->hostname = "localhost";
			else
				node->hostname = msg.params[1];
			if (msg.params[2] == "*")
				node->servername = server.servername;
			else
				node->servername = msg.params[2];
			rpl = BUILD_RPL_WELCOME(server.servername, "localhost", node->nickname, node->username, node->hostname);
			rpl += BUILD_RPL_YOURHOST(server.servername, node->nickname, server.version);
			rpl += BUILD_RPL_CREATED(server.servername, node->nickname);
			rpl += BUILD_RPL_MYINFO(server.servername, node->nickname, server.version, "", ""); //usermode, channelmode
			rpl += _isupport(server, node);
		}
		else
			rpl = BUILD_ERR_NONICKNAMEGIVEN(server.servername);
	}
	dispatch_packet(server, node, rpl);
}

void Executor::_execute_cap(Server &server, Connection *&node, const Message &msg)
{
	std::string rpl;

	if (msg.params.size() == 1 && msg.params[0] == "END")
		return;
	if (msg.params.size() != 2)
		rpl = BUILD_ERR_NEEDMOREPARAMS(server.servername, msg.command);
	else if (msg.params[0] == "LS" && msg.params[1] == "302")
		rpl = "CAP * LS :\r\n";
	else
		rpl = BUILD_ERR_UNKNOWNCOMMAND(server.servername, "", "CAP");
	dispatch_packet(server, node, rpl);
}

void Executor::_execute_ping(Server &server, Connection *&node, const Message &msg)
{
	std::string rpl;

	if (msg.params.size() != 1)
	{
		rpl = BUILD_ERR_NEEDMOREPARAMS(server.servername, msg.command);
		dispatch_packet(server, node, rpl);
		return;
	}
	rpl = "PONG " + msg.params[0] + "\r\n";
	dispatch_packet(server, node, rpl);
}

static bool isChannelMembership(char c) {
	std::string special_chars = "~&@%+";
    return special_chars.find(c) != std::string::npos;
}

void Executor::_execute_privmsg(Server &server, Connection *&node, const Message &msg)
{
	if (node->is_registered == false)
	{
		dispatch_packet(server, node, BUILD_ERR_NOTREGISTERED(server.servername, node->nickname));
        return;
	}

	std::string rpl;
	if (msg.params.size() != 2)
		rpl = BUILD_ERR_NEEDMOREPARAMS(server.servername, msg.command);
	else if (msg.params[0].size() < 1)
		rpl = BUILD_ERR_NORECIPIENT(server.servername, node->nickname, "PRIVMSG");
	else if (msg.params[1].size() < 1)
		rpl = BUILD_ERR_NOTEXTTOSEND(server.servername, node->nickname);
	else if (msg.params[0].find(',') != std::string::npos)
		rpl = BUILD_ERR_TOOMANYTARGETS(server.servername, node->nickname, msg.params[0]);
	else if (msg.params[0].find('#') != std::string::npos) //channel
	{
		size_t i = 0;
		bool isOp = false;
		while (i < msg.params[0].size() && isChannelMembership(msg.params[0][i]))
		{
			if (msg.params[0][i] != '@')
			{
				rpl = BUILD_ERR_CANNOTSENDTOCHAN(server.servername, msg.command, msg.params[0]);
				dispatch_packet(server, node, rpl);
				return;
			}
			isOp = true;
			i++;
		}
		if (msg.params[0].size() == i || msg.params[0][i] != '#' || msg.params[0].size() == i + 1)
		{
			rpl = BUILD_ERR_NORECIPIENT(server.servername, node->nickname, "PRIVMSG");
			dispatch_packet(server, node, rpl);
			return;
		}
		std::string target = msg.params[0].substr(i, msg.params[0].size());
		Parser::tolower(target);
		std::map<std::string, std::list<Channel *>::iterator>::iterator it = server.chandb.find(target);
		if (it == server.chandb.end())
		{
			rpl = BUILD_ERR_NOSUCHNICK(server.servername, node->nickname, msg.params[0]);
			dispatch_packet(server, node, rpl);
			return;
		}
		Channel *channelPtr = *(it->second);

		if ((channelPtr->rdstate() & Channel::ibit) && (channelPtr->clientdb.find(node->sockfd) == channelPtr->clientdb.end() && channelPtr->clientdb.find(node->sockfd) == channelPtr->invitedb.end()))
		{
			rpl = BUILD_ERR_CANNOTSENDTOCHAN(server.servername, node->nickname, msg.params[0]);
			dispatch_packet(server, node, rpl);
			return;
		}
		std::string toSend;
		toSend = ":" + node->nickname + "!" + node->username + "@" + node->hostname + " PRIVMSG " + msg.params[0] + " :" + msg.params[1];
		if (isOp)
		{
			for (std::map<Connection *, enum Channel::CHANOPS>::iterator it = channelPtr->privdb.begin(); it != channelPtr->privdb.end(); ++it)
			{
				if (it->second != Channel::OPERATOR)
					continue;
				Connection *operClient = it->first;
				dispatch_packet(server, operClient, toSend + "\r\n");
			}
		}
		else
			broadcast(server, channelPtr, toSend + "\r\n");
		return;
	}
	else
	{
		//client
		std::string nick = msg.params[0];
		Parser::tolower(nick);
		std::map<std::string, std::list<Connection *>::iterator>::iterator it = server.nickdb.find(nick);
		if (it == server.nickdb.end())
		{
			rpl = BUILD_ERR_NOSUCHNICK(server.servername, node->nickname, msg.params[0]);
			dispatch_packet(server, node, rpl);
			return;
		}
		std::string toSend;
		toSend = ":" + node->nickname + " PRIVMSG " + msg.params[0] + " :" + msg.params[1];
		dispatch_packet(server, *it->second, toSend + "\r\n");
		return;
	}
	dispatch_packet(server, node, rpl);
}

void Executor::_execute_notice(Server &server, Connection *&node, const Message &msg)
{
	if (node->is_registered == false)
	{
		dispatch_packet(server, node, BUILD_ERR_NOTREGISTERED(server.servername, node->nickname));
        return;
	}

	std::string rpl;
	if (msg.params.size() != 2)
		return;
	else if (msg.params[0].size() < 1)
		return;
	else if (msg.params[1].size() < 1)
		return;
	else if (msg.params[0].find(',') != std::string::npos)
		return;
	else if (msg.params[0].find('#') != std::string::npos) //channel
	{
		size_t i = 0;
		bool isOp = false;
		while (i < msg.params[0].size() && isChannelMembership(msg.params[0][i]))
		{
			if (msg.params[0][i] != '@')
				return;
			isOp = true;
			i++;
		}
		if (msg.params[0].size() == i || msg.params[0][i] != '#' || msg.params[0].size() == i + 1)
			return;
		std::string target = msg.params[0].substr(i, msg.params[0].size());
		Parser::tolower(target);
		std::map<std::string, std::list<Channel *>::iterator>::iterator it = server.chandb.find(target);
		if (it == server.chandb.end())
			return;
		Channel *channelPtr = *(it->second);
		if ((channelPtr->rdstate() & Channel::ibit) && (channelPtr->clientdb.find(node->sockfd) == channelPtr->clientdb.end() && channelPtr->clientdb.find(node->sockfd) == channelPtr->invitedb.end()))
			return;
		std::string toSend;
		toSend = ":" + node->nickname + "!" + node->username + "@" + node->hostname + " PRIVMSG " + msg.params[0] + " :" + msg.params[1];
		if (isOp)
		{
			for (std::map<Connection *, enum Channel::CHANOPS>::iterator it = channelPtr->privdb.begin(); it != channelPtr->privdb.end(); ++it)
			{
				if (it->second != Channel::OPERATOR)
					continue;
				Connection *operClient = it->first;
				dispatch_packet(server, operClient, toSend + "\r\n");
			}
		}
		else
			broadcast(server, channelPtr, toSend + "\r\n");
		return;
	}
	else
	{
		//client
		std::string nick = msg.params[0];
		Parser::tolower(nick);
		std::map<std::string, std::list<Connection *>::iterator>::iterator it = server.nickdb.find(nick);
		if (it == server.nickdb.end())
			return;
		std::string toSend;
		toSend = ":" + node->nickname + " PRIVMSG " + msg.params[0] + " :" + msg.params[1];
		dispatch_packet(server, *it->second, toSend + "\r\n");
		return;
	}
}

void Executor::_execute_quit(Server &server, Connection *&node, const Message &msg)
{
	if (!node->is_authed)
	{
		dispatch_packet(server, node, BUILD_ERR_NOTREGISTERED(server.servername, node->nickname));
		return;
	}
    std::string quit_message;
    if (!msg.params.empty())
    {
        quit_message = msg.params[0];
    }
    else
    {
        quit_message = "Client Quit";
    }

    for (std::map<std::string, Channel *>::iterator it = node->chandb.begin(); it != node->chandb.end(); ++it)
    {
        Channel *channel = it->second;
        Executor::broadcast(server, channel, ":" + node->nickname + " QUIT :" + quit_message + "\r\n");
    }

    to_doom(server, node, ""); // QUIT has no reply
}

void Executor::_execute_topic(Server &server, Connection *&node, const Message &msg)
{
	if (node->is_registered == false)
	{
		dispatch_packet(server, node, BUILD_ERR_NOTREGISTERED(server.servername, node->nickname));
        return;
	}

    if (msg.params.size() != 1 && msg.params.size() != 2)
    {
		dispatch_packet(server, node, BUILD_ERR_NEEDMOREPARAMS(server.servername, msg.command));
        return;
    }

    std::string channame = msg.params.at(0);
	Parser::tolower(channame);
	std::string topic = (msg.params.size() == 2 ? msg.params.at(1) : "");

	if (server.chandb.find(channame) == server.chandb.end())
	{
		dispatch_packet(server, node, BUILD_ERR_NOSUCHCHANNEL(server.servername, node->nickname, channame));
		return;
	}

	std::map<std::string, Channel *>::iterator chanit = node->chandb.find(channame);
	if (chanit == node->chandb.end())
	{
		dispatch_packet(server, node, BUILD_ERR_NOTONCHANNEL(server.servername, node->nickname, channame));
		return;
	}

    Channel		*chan = chanit->second;
	if (chan->state & Channel::tbit && chan->privdb.find(node) == chan->privdb.end())
	{
		dispatch_packet(server, node, BUILD_ERR_CHANOPRIVSNEEDED(server.servername, channame));
		return;
	}

	if (msg.params.size() == 1)
	{
		if (chan->topic.empty())
		{
			dispatch_packet(server, node, BUILD_RPL_NOTOPIC(server.servername, node->nickname, channame));
		}
		else
		{
			dispatch_packet(server, node, BUILD_RPL_TOPIC(server.servername, node->nickname, channame, chan->topic));
			dispatch_packet(server, node, BUILD_RPL_TOPICWHOTIME(server.servername, node->nickname, channame, chan->topic_setter, chan->topic_time));
		}
		return;
	}

	if (chan->topic == topic) // ignore command if <topic> is the same as previous topic 
		return;

	chan->topic = topic;
	chan->topic_time = utils::time_to_str(std::time(NULL));
	chan->topic_setter = node->nickname;
    Executor::broadcast(server, chan, ":" + node->nickname + " TOPIC " + channame + " :" + chan->topic + "\r\n");
}

void Executor::_execute_invite(Server &server, Connection *&node, const Message &msg)
{
	if (node->is_registered == false)
	{
		dispatch_packet(server, node, BUILD_ERR_NOTREGISTERED(server.servername, node->nickname));
        return;
	}

	if (msg.params.size() != 2)
	{
		dispatch_packet(server, node, BUILD_ERR_NEEDMOREPARAMS(server.servername, msg.command));
		return;
	}

	std::string target = msg.params[0];
	Parser::tolower(target);
	std::string channame = msg.params[1];
	Parser::tolower(channame);

	std::map<std::string, std::list<Channel *>::iterator>::iterator it = server.chandb.find(channame);
	if (it == server.chandb.end())
	{
		dispatch_packet(server, node, BUILD_ERR_NOSUCHCHANNEL(server.servername, node->nickname, channame));
		return;
	}

	Channel *chan = *it->second;

	if (chan->clientdb.find(node->sockfd) == chan->clientdb.end())
	{
		dispatch_packet(server, node, BUILD_ERR_NOTONCHANNEL(server.servername, node->nickname, channame));
		return;
	}

	if ((chan->state & Channel::ibit) && chan->privdb.find(node) == chan->privdb.end())
	{

		dispatch_packet(server, node, BUILD_ERR_CHANOPRIVSNEEDED(server.servername, channame));
		return;
	}

	std::map<std::string, std::list<Connection *>::iterator>::iterator find = server.nickdb.find(target);
	if (find == server.nickdb.end())
	{
		dispatch_packet(server, node, BUILD_ERR_NOSUCHNICK(server.servername, node->nickname, target));
		return;
	}

	Connection *targetnode = *find->second;
	if (chan->clientdb.find(targetnode->sockfd) != chan->clientdb.end())
	{
		dispatch_packet(server, node, BUILD_ERR_USERONCHANNEL(server.servername, target, channame));
		return;
	}

	if (chan->invitedb.find(targetnode->sockfd) != chan->invitedb.end())
	{
		dispatch_packet(server, node, BUILD_ERR_USERONCHANNEL(server.servername, target, channame));
		return;
	}

	chan->invitedb.insert(std::pair<int, Connection *>(targetnode->sockfd, targetnode));

	dispatch_packet(server, targetnode, ":" + node->nickname + " INVITE " + target + " " + channame + "\r\n");
	dispatch_packet(server, node, BUILD_RPL_INVITING(server.servername, node->nickname, target, channame));
}

void Executor::_execute_kick(Server &server, Connection *&node, const Message &msg)
{
	if (node->is_registered == false)
	{
		dispatch_packet(server, node, BUILD_ERR_NOTREGISTERED(server.servername, node->nickname));
        return;
	}

    if (msg.params.size() != 2 && msg.params.size() != 3)
    {
		dispatch_packet(server, node, BUILD_ERR_NEEDMOREPARAMS(server.servername, msg.command));
        return;
    }

    std::string channame = msg.params[0];
	Parser::tolower(channame);
    std::string nickname = msg.params[1];
	Parser::tolower(nickname);
    std::string comment = (msg.params.size() == 3) ? msg.params[2] : "";

	if (server.chandb.find(channame) == server.chandb.end())
	{
		dispatch_packet(server, node, BUILD_ERR_NOSUCHCHANNEL(server.servername, node->nickname, channame));
		return;
	}

	std::map<std::string, Channel *>::iterator chanit = node->chandb.find(channame);
	if (chanit == node->chandb.end())
	{
		dispatch_packet(server, node, BUILD_ERR_NOTONCHANNEL(server.servername, node->nickname, channame));
		return;
	}

    Channel *chan = chanit->second;

	std::map<std::string, std::list<Connection *>::iterator>::iterator find = server.nickdb.find(nickname);
	if (find == server.nickdb.end()) 
	{
		dispatch_packet(server, node, BUILD_ERR_USERNOTINCHANNEL(server.servername, nickname, channame));
		return;
	}

	Connection *targetnode = *find->second;
	if (chan->clientdb.find(targetnode->sockfd) == chan->clientdb.end())
	{
		dispatch_packet(server, node, BUILD_ERR_USERNOTINCHANNEL(server.servername, nickname, channame));
		return;
	}

	if (chan->privdb.find(node) == chan->privdb.end())
	{
		dispatch_packet(server, node, BUILD_ERR_CHANOPRIVSNEEDED(server.servername, channame));
		return;
	}

    Executor::broadcast(server, chan, ":" + node->nickname + " KICK " + channame + " " + nickname + " :" + comment + "\r\n");

	chan->part(targetnode);
	if (chan->clientdb.empty())	// clean up server resources if chan has been made empty
	{
		std::map<std::string, std::list<Channel *>::iterator>::iterator find = server.chandb.find(chan->name);
		server.chans.erase(find->second);
		server.chandb.erase(find);
		delete chan; // delete empty chan
	}
}

void Executor::_execute_mode(Server &server, Connection *&node, const Message &msg)
{
	if (node->is_registered == false)
	{
		dispatch_packet(server, node, BUILD_ERR_NOTREGISTERED(server.servername, node->nickname));
        return;
	}
	
    if (msg.params.size() < 2)
    {
		dispatch_packet(server, node, BUILD_ERR_NEEDMOREPARAMS(server.servername, msg.command));
        return;
    }

    std::string target = msg.params[0];
	Parser::tolower(target);
    std::string mode_changes = msg.params[1];

    bool is_channel = Parser::is_channel(target);
    if (is_channel)
    {
        std::list<Channel *>::iterator it = server.chans.begin();
        for (; it != server.chans.end(); ++it)
        {
            if ((*it)->name == target)
                break;
        }

        if (it == server.chans.end())
        {
			dispatch_packet(server, node, BUILD_ERR_NOSUCHCHANNEL(server.servername, node->nickname, target));
            return;
        }

        Channel *channel = *it;

		// check if user is in the channel
		if (channel->clientdb.find(node->sockfd) == channel->clientdb.end())
		{
			dispatch_packet(server, node, BUILD_ERR_NOTONCHANNEL(server.servername, node->nickname, target));
			return;
		}

		// check if user has the required privileges to change the mode
        if (channel->privdb.find(node) == channel->privdb.end())
        {
			dispatch_packet(server, node, BUILD_ERR_CHANOPRIVSNEEDED(server.servername, target));
            return;
        }

		size_t param_size = 0;
		for (std::string::iterator mode_it = mode_changes.begin(); mode_it != mode_changes.end(); ++mode_it)
		{
			if (*mode_it == 'k' || *mode_it == 'l' || *mode_it == 'o')
			{
				param_size++;
			}
		}

		if (mode_changes.size() - 1 < param_size)
		{
			dispatch_packet(server, node, BUILD_ERR_NEEDMOREPARAMS(server.servername, msg.command));
			return;
		}

        bool adding = true;
        size_t param_index = 2;
        for (std::string::iterator mode_it = mode_changes.begin(); mode_it != mode_changes.end(); ++mode_it)
        {
            char mode = *mode_it;

            if (mode == '+')
            {
                adding = true;
                continue;
            }
            else if (mode == '-')
            {
                adding = false;
                continue;
            }

            switch (mode)
            {
                case 'i':
                    if (adding)
                        channel->state |= Channel::ibit;
                    else
                        channel->state &= ~Channel::ibit;
                    break;
                case 't':
                    if (adding)
                        channel->state |= Channel::tbit;
                    else
                        channel->state &= ~Channel::tbit;
                    break;
                case 'k':
                    if (adding)
                    {
						std::string temp_key = msg.params[param_index++];
						if (temp_key.empty() || temp_key.size() > 32)
						{
							dispatch_packet(server, node, BUILD_ERR_NEEDMOREPARAMS(server.servername, msg.command));
							break;
						}
						std::string restricted_chars = " /\\:,";
        				if (temp_key.find_first_of(restricted_chars) != std::string::npos)
        				{
            				dispatch_packet(server, node, BUILD_ERR_NEEDMOREPARAMS(server.servername, msg.command));
							break;
        				}
                        channel->key = temp_key;
                        channel->state |= Channel::kbit;
                    }
                    else
                    {
                        channel->state &= ~Channel::kbit;
                        channel->key.clear();
                    }
                    break;
                case 'l':
                    if (adding)
                    {
						std::string temp_str = msg.params[param_index++];
						char *endptr;
						long temp = std::strtol(temp_str.c_str(), &endptr, 10);
						if (*endptr != '\0' || temp < 0)
						{
							dispatch_packet(server, node, BUILD_ERR_NEEDMOREPARAMS(server.servername, msg.command));
							break;
						}
						channel->limit = temp;
						channel->state |= Channel::lbit;
                    }
                    else
                    {
                        channel->state &= ~Channel::lbit;
                    }
                    break;
                case 'o':
                    if (msg.params.size() <= param_index)
                    {
						dispatch_packet(server, node, BUILD_ERR_NEEDMOREPARAMS(server.servername, msg.command));
                        return;
                    }
                    {
						// check if target user exists
                        std::string target_nickname = msg.params[param_index++];
                        std::map<std::string, std::list<Connection *>::iterator>::iterator user_it = server.nickdb.find(target_nickname);
                        if (user_it == server.nickdb.end())
                        {
							dispatch_packet(server, node, BUILD_ERR_NOSUCHNICK(server.servername, node->nickname, target_nickname));
                            return;
                        }
                        Connection *target_node = *(user_it->second);

						// check if target user is in the channel
						if (channel->clientdb.find(target_node->sockfd) == channel->clientdb.end())
						{
							dispatch_packet(server, node, BUILD_ERR_USERNOTINCHANNEL(server.servername, target_nickname, target));
							return;
						}

                        if (adding)
                            channel->privdb[target_node] = Channel::OPERATOR;
                        else
                            channel->privdb.erase(target_node);
                    }
                    break;
                default:
					dispatch_packet(server, node,  BUILD_ERR_UNKNOWNMODE(server.servername, mode, target));
                    return;
            }
        }
        Executor::broadcast(server, channel, ":" + node->nickname + " MODE " + target + " " + mode_changes + "\r\n");
		dispatch_packet(server, node, BUILD_RPL_CHANNELMODEIS(server.servername, channel->name, channel->get_mode_string()));
    }
    else
    {
		dispatch_packet(server, node,  BUILD_ERR_UNKNOWNMODE(server.servername, msg.command, target));
    }
}
