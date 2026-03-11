#pragma once

#include "Message.hpp"

#include <string>
#include <vector>

class Parser
{
    public:
    /* token을 소문자로 정규화한다. */
    static void         tolower(std::string &token);
    static void         toupper(std::string &token);
    
    /* token의 모든 문자가 공백이면 true를 반환한다. */
    static bool         isspace(const std::string &token);
    
    static bool         is_channel(const std::string &token);
    static bool         is_nickname(const std::string &token);

    static void         tokenize(const std::string &stream, const std::string &delim, std::vector<std::string> &tokens);
    static void         make_messages(std::string &stream, std::vector<Message> &batch);
};
