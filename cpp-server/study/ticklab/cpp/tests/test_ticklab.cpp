#include "inc/MatchEngine.hpp"

#include <fstream>
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

    std::vector<MatchEngine::Event> drain(MatchEngine &engine)
    {
        return engine.drain_events();
    }

    bool contains_line(const std::vector<MatchEngine::Event> &events, const std::string &needle)
    {
        for (std::vector<MatchEngine::Event>::const_iterator it = events.begin(); it != events.end(); ++it)
        {
            if (it->line.find(needle) != std::string::npos)
                return true;
        }
        return false;
    }

    void advance_ticks(MatchEngine &engine, int count)
    {
        for (int i = 0; i < count; ++i)
            engine.advance_one_tick();
    }

    void test_transcript_fixture()
    {
        MatchEngine engine;
        MatchEngine::Error error;
        std::string alpha;
        std::string bravo;

        std::ifstream fixture("../problem/data/arena-transcript.txt");
        expect(fixture.good(), "fixture file is missing");

        std::string line;
        while (std::getline(fixture, line))
        {
            if (line == "HELLO alpha")
                expect(engine.register_player("alpha", alpha, error), "alpha registration failed");
            else if (line == "HELLO bravo")
                expect(engine.register_player("bravo", bravo, error), "bravo registration failed");
            else if (line == "QUEUE alpha")
                expect(engine.queue_player(alpha, error), "alpha queue failed");
            else if (line == "QUEUE bravo")
                expect(engine.queue_player(bravo, error), "bravo queue failed");
            else if (line == "READY alpha")
                expect(engine.ready_player(alpha, error), "alpha ready failed");
            else if (line == "READY bravo")
                expect(engine.ready_player(bravo, error), "bravo ready failed");
            else if (line == "INPUT alpha 1 0 0 E 1")
                expect(engine.submit_input(alpha, MatchEngine::Input(1, 0, 0, 'E', true), error), "alpha input seq1 failed");
            else if (line == "INPUT alpha 2 0 0 E 1")
                expect(engine.submit_input(alpha, MatchEngine::Input(2, 0, 0, 'E', true), error), "alpha input seq2 failed");
            else if (line == "INPUT alpha 3 0 0 E 1")
                expect(engine.submit_input(alpha, MatchEngine::Input(3, 0, 0, 'E', true), error), "alpha input seq3 failed");
            else if (line == "TICK")
                engine.advance_one_tick();
        }

        std::vector<MatchEngine::Event> events = drain(engine);
        expect(contains_line(events, "COUNTDOWN 3"), "countdown start missing");
        expect(contains_line(events, "ROOM arena-1 in_round"), "room did not enter in_round");
        expect(contains_line(events, "HIT"), "hit event missing");
        expect(contains_line(events, "ROUND_END alpha"), "winner event missing");
    }

    void test_stale_sequence_and_validation()
    {
        MatchEngine engine;
        MatchEngine::Error error;
        std::string alpha;
        std::string bravo;

        expect(engine.register_player("alpha", alpha, error), "alpha registration failed");
        expect(engine.register_player("bravo", bravo, error), "bravo registration failed");
        expect(engine.queue_player(alpha, error), "alpha queue failed");
        expect(engine.queue_player(bravo, error), "bravo queue failed");
        expect(engine.ready_player(alpha, error), "alpha ready failed");
        expect(engine.ready_player(bravo, error), "bravo ready failed");
        advance_ticks(engine, 3);
        drain(engine);

        expect(engine.submit_input(alpha, MatchEngine::Input(1, 1, 0, 'E', false), error), "first input should pass");
        expect(!engine.submit_input(alpha, MatchEngine::Input(1, 0, 0, 'E', false), error), "stale sequence should fail");
        expect(error.code == "stale_sequence", "stale sequence code mismatch");
        expect(!engine.submit_input(alpha, MatchEngine::Input(2, 1, 1, 'E', false), error), "diagonal move should fail");
        expect(error.code == "invalid_input", "invalid input code mismatch");
    }

    void test_rejoin_grace_window()
    {
        MatchEngine engine;
        MatchEngine::Error error;
        std::string alpha;

        expect(engine.register_player("alpha", alpha, error), "alpha registration failed");
        engine.disconnect_player(alpha);
        advance_ticks(engine, 50);
        expect(engine.rejoin_player(alpha, error), "rejoin within grace should pass");
        drain(engine);

        engine.disconnect_player(alpha);
        advance_ticks(engine, MatchEngine::grace_ticks + 1);
        expect(!engine.rejoin_player(alpha, error), "rejoin after grace should fail");
        expect(error.code == "expired_session", "expired session code mismatch");
    }

    void test_draw_timeout()
    {
        MatchEngine engine;
        MatchEngine::Error error;
        std::string alpha;
        std::string bravo;

        expect(engine.register_player("alpha", alpha, error), "alpha registration failed");
        expect(engine.register_player("bravo", bravo, error), "bravo registration failed");
        expect(engine.queue_player(alpha, error), "alpha queue failed");
        expect(engine.queue_player(bravo, error), "bravo queue failed");
        expect(engine.ready_player(alpha, error), "alpha ready failed");
        expect(engine.ready_player(bravo, error), "bravo ready failed");
        advance_ticks(engine, 3);
        drain(engine);
        advance_ticks(engine, MatchEngine::max_round_ticks);
        std::vector<MatchEngine::Event> events = drain(engine);
        expect(contains_line(events, "ROUND_END draw"), "draw timeout event missing");
    }
}

int main()
{
    try
    {
        test_transcript_fixture();
        test_stale_sequence_and_validation();
        test_rejoin_grace_window();
        test_draw_timeout();
        std::cout << "ticklab tests passed." << std::endl;
        return 0;
    }
    catch (const std::exception &e)
    {
        std::cerr << "ticklab tests failed: " << e.what() << std::endl;
        return 1;
    }
}
