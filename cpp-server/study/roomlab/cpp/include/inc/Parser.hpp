#pragma once

#include "Message.hpp"

#include <string>
#include <vector>

class Parser
{
    public:
    /* convert token into lowercase equivalent */
    static void         tolower(std::string &token);
    static void         toupper(std::string &token);
    
    /* true if every char in token is a space */
    static bool         isspace(const std::string &token);
    
    static bool         is_channel(const std::string &token);
    static bool         is_nickname(const std::string &token);

    static void         tokenize(const std::string &stream, const std::string &delim, std::vector<std::string> &tokens);
    static void         make_messages(std::string &stream, std::vector<Message> &batch);
};
