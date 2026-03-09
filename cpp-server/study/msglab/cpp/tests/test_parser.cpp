#include "inc/Message.hpp"
#include "inc/Parser.hpp"

#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace
{
    void expect(bool condition, const std::string &message)
    {
        if (!condition)
            throw std::runtime_error(message);
    }

    void test_prefix_and_trailing()
    {
        Message msg(":nick!user@host PRIVMSG #cpp :hello world");
        expect(msg.prefix == "nick!user@host", "prefix parsing failed");
        expect(msg.comm == Message::PRIVMSG, "command translation failed");
        expect(msg.params.size() == 2, "trailing parameter parsing failed");
        expect(msg.params[0] == "#cpp", "target parameter parsing failed");
        expect(msg.params[1] == "hello world", "trailing text parsing failed");
    }

    void test_validators()
    {
        expect(Parser::is_nickname("alice"), "valid nickname rejected");
        expect(Parser::is_nickname("[bot]-1"), "special nickname rejected");
        expect(!Parser::is_nickname("1alice"), "nickname starting with digit accepted");
        expect(!Parser::is_nickname("bad nick"), "nickname with space accepted");

        expect(Parser::is_channel("#cpp"), "valid channel rejected");
        expect(Parser::is_channel("&local"), "ampersand channel rejected");
        expect(!Parser::is_channel("cpp"), "channel without prefix accepted");
        expect(!Parser::is_channel("#bad,name"), "channel with comma accepted");
    }

    void test_make_messages_keeps_partial_line()
    {
        std::string stream = "PING one\r\nJOIN #cpp\r\nPART #cpp";
        std::vector<Message> batch;
        Parser::make_messages(stream, batch);

        expect(batch.size() == 2, "message batch size mismatch");
        expect(batch[0].comm == Message::PING, "PING frame missing");
        expect(batch[1].comm == Message::JOIN, "JOIN frame missing");
        expect(stream == "PART #cpp", "partial line was not preserved");
    }

    void test_golden_transcripts()
    {
        struct Case
        {
            const char     *line;
            Message::label expected;
            std::size_t    param_count;
        };

        const Case cases[] = {
            {"PASS hunter2", Message::PASS, 1},
            {"NICK alice", Message::NICK, 1},
            {"USER alice 0 * :Alice", Message::USER, 4},
            {"JOIN #cpp", Message::JOIN, 1},
            {"PRIVMSG #cpp :hello", Message::PRIVMSG, 2},
            {"TOPIC #cpp :topic", Message::TOPIC, 2},
            {"MODE #cpp +i", Message::MODE, 2},
            {"KICK #cpp bob :bye", Message::KICK, 3},
            {"INVITE bob #cpp", Message::INVITE, 2},
        };

        for (std::size_t i = 0; i < sizeof(cases) / sizeof(cases[0]); ++i)
        {
            Message msg(cases[i].line);
            expect(msg.comm == cases[i].expected, std::string("unexpected command label for: ") + cases[i].line);
            expect(msg.params.size() == cases[i].param_count, std::string("unexpected param count for: ") + cases[i].line);
        }
    }

    void test_arena_commands()
    {
        Message hello("HELLO alpha");
        expect(hello.comm == Message::UNK, "arena HELLO should stay generic");
        expect(hello.command == "HELLO", "HELLO command should be preserved");
        expect(hello.params.size() == 1 && hello.params[0] == "alpha", "HELLO params mismatch");

        Message input("INPUT 42 1 0 E 1");
        expect(input.command == "INPUT", "INPUT command should be preserved");
        expect(input.params.size() == 5, "INPUT params mismatch");
        expect(Parser::is_integer(input.params[0]), "INPUT seq should be numeric");
        expect(Parser::is_integer(input.params[1]), "INPUT dx should be numeric");
        expect(Parser::is_integer(input.params[2]), "INPUT dy should be numeric");
        expect(Parser::is_facing(input.params[3]), "INPUT facing should be validated");
        expect(Parser::is_binary_flag(input.params[4]), "INPUT fire flag should be binary");

        Message rejoin("REJOIN token-7");
        expect(rejoin.command == "REJOIN", "REJOIN command should be preserved");
        expect(rejoin.params.size() == 1 && rejoin.params[0] == "token-7", "REJOIN params mismatch");

        expect(!Parser::is_integer("seq42"), "non-numeric seq accepted");
        expect(!Parser::is_facing("Q"), "invalid facing accepted");
        expect(!Parser::is_binary_flag("2"), "non-binary flag accepted");
    }
}

int main()
{
    try
    {
        test_prefix_and_trailing();
        test_validators();
        test_make_messages_keeps_partial_line();
        test_golden_transcripts();
        test_arena_commands();
        std::cout << "msglab parser tests passed." << std::endl;
        return 0;
    }
    catch (const std::exception &e)
    {
        std::cerr << "msglab parser tests failed: " << e.what() << std::endl;
        return 1;
    }
}
