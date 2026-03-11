#include "inc/Parser.hpp"

#include <cctype>
#include <cstdlib>

const std::string Parser::channel_types = "#&";
const std::size_t Parser::max_channel_length = 32U;
const std::size_t Parser::max_nick_length = 30U;

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

    if (token.find_first_of(Parser::channel_types) != 0)
        return false;
    
    if (token.find_first_of(metachars) != std::string::npos)
        return false;

    if (token.length() < 2 || token.length() > Parser::max_channel_length)
		return false;

    return true;
}

bool Parser::is_nickname(const std::string &token)
{
    static const std::string special_chars = "[]\\{}|-";

    if (token.empty() || token.length() > Parser::max_nick_length)
        return false;
    if (!std::isalpha(static_cast<unsigned char>(token[0]))
        && special_chars.find(token[0]) == std::string::npos)
        return false;

    for (std::size_t i = 1; i < token.size(); ++i)
    {
        const unsigned char ch = static_cast<unsigned char>(token[i]);
        if (!std::isalnum(ch) && special_chars.find(static_cast<char>(ch)) == std::string::npos)
            return false;
    }
    return true;
}

bool Parser::is_integer(const std::string &token)
{
    if (token.empty())
        return false;

    std::size_t start = 0;
    if (token[0] == '-' || token[0] == '+')
    {
        if (token.size() == 1)
            return false;
        start = 1;
    }

    for (std::size_t i = start; i < token.size(); ++i)
    {
        if (!std::isdigit(static_cast<unsigned char>(token[i])))
            return false;
    }
    return true;
}

bool Parser::is_facing(const std::string &token)
{
    return token == "N" || token == "E" || token == "S" || token == "W";
}

bool Parser::is_binary_flag(const std::string &token)
{
    return token == "0" || token == "1";
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
    std::size_t line_end = stream.find('\n');
    while (line_end != std::string::npos)
    {
        std::string frame = stream.substr(0, line_end);
        stream.erase(0, line_end + 1);
        if (!frame.empty() && frame[frame.size() - 1] == '\r')
            frame.erase(frame.size() - 1);
        if (!frame.empty() && !isspace(frame))
            batch.push_back(Message(frame));
        line_end = stream.find('\n');
    }
}
