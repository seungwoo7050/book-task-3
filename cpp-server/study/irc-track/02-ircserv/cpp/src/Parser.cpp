#include "inc/Parser.hpp"
#include "inc/Server.hpp"
#include "inc/debug.hpp"

void Parser::tolower(std::string &token)
{
    for (std::string::iterator it = token.begin(); it != token.end(); ++it)
    {
        *it = static_cast<char>(std::tolower(static_cast<unsigned char>(*it)));
    }
}

void Parser::toupper(std::string &token)
{
    for (std::string::iterator it = token.begin(); it != token.end(); ++it)
    {
        *it = static_cast<char>(std::toupper(static_cast<unsigned char>(*it)));
    }
}

bool Parser::isspace(const std::string &token)
{
    for (std::string::const_iterator it = token.cbegin(); it != token.cend(); ++it)
    {
        if (*it != ' ')
            return false;
    }
    return true;
}

bool Parser::is_channel(const std::string &token)
{
    static const std::string metachars = " ,"; // 공백, 쉼표(comma), control G / BELL(0x07)

    if (token.find_first_of(Server::chantypes) != 0)
        return false;
    
    if (token.find_first_of(metachars) != std::string::npos)
        return false;

    char *endptr;
    if (token.length() < 2 || token.length() > std::strtod(Server::channellen.c_str(), &endptr))
		return false;

    return true;
}

void Parser::tokenize(const std::string &stream, const std::string &delim, std::vector<std::string> &tokens)
{
    std::size_t pos = 0, find = 0;
	
	while (pos != std::string::npos)
    {
        find = stream.find(delim, pos);
        std::string token = stream.substr(pos, find - pos);
        if (!token.empty())
        {
            tokens.push_back(token);
        }
        pos = (find == std::string::npos ? std::string::npos : find + delim.size());
    }
}

void Parser::make_messages(std::string &stream, std::vector<Message> &batch)
{
    std::vector<std::string> frames;
    
	if (stream.find("\r\n") != std::string::npos)
	{
		std::clog << "msg boundary marker: [rn]";
		tokenize(stream, "\r\n", frames);
	}
	else if (stream.find("\n") != std::string::npos)
	{
		std::clog << "msg boundary marker: [n]";
		tokenize(stream, "\n", frames);
	}
	else
		tokenize(stream, Server::crlf, frames);

    for (std::vector<std::string>::iterator it = frames.begin(); it != frames.end(); ++it)
    {
        if (!it->empty() && !isspace(*it)) // 빈 메시지는 조용히 무시한다.
            batch.push_back(Message(*it));
    }

    for (std::vector<Message>::iterator it = batch.begin(); it != batch.end(); ++it)
    {
        debug::log_msg_status(*it);
    }

    stream.clear();
}
