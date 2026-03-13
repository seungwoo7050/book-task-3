#include "inc/RollbackSession.hpp"

#include <iostream>
#include <stdexcept>

namespace
{
    void expect(bool condition, const std::string &message)
    {
        if (!condition)
            throw std::runtime_error(message);
    }

    void test_future_input_buffers_without_rollback()
    {
        RollbackSession session;
        session.add_player("alpha", 0, 0);

        ResimResult result = session.submit_input("alpha", PlayerInput(1, 1, 0, false));
        expect(!result.rolled_back, "future input should not rollback immediately");

        session.advance_to_frame(3);
        WorldState world = session.world();
        expect(world.frame == 3, "expected frame 3");
        expect(world.players["alpha"].x == 3, "prediction should carry movement forward");
    }

    void test_late_input_triggers_rollback_and_replay()
    {
        RollbackSession session;
        session.add_player("alpha", 0, 0);

        session.submit_input("alpha", PlayerInput(1, 1, 0, false));
        session.advance_to_frame(3);
        expect(session.world().players["alpha"].x == 3, "expected predicted x=3 before rollback");

        ResimResult late = session.submit_input("alpha", PlayerInput(2, 0, 0, false));
        expect(late.rolled_back, "late input should trigger rollback");
        expect(late.rollback_from_frame == 2, "rollback should start at frame 2");
        expect(late.replayed_through_frame == 3, "rollback should replay through frame 3");
        expect(late.frames_replayed == 2, "should replay exactly two frames");
        expect(late.converged, "replay should converge");
        expect(session.world().players["alpha"].x == 1, "late idle input should change final x");
    }

    void test_identical_late_input_is_fast_path()
    {
        RollbackSession session;
        session.add_player("alpha", 0, 0);

        session.submit_input("alpha", PlayerInput(1, 1, 0, false));
        session.advance_to_frame(2);

        ResimResult same = session.submit_input("alpha", PlayerInput(1, 1, 0, false));
        expect(!same.rolled_back, "identical late input should be a no-op");
        expect(session.world().players["alpha"].x == 2, "world should remain unchanged");
    }

    void test_snapshot_and_resimulation_with_two_players()
    {
        RollbackSession session;
        session.add_player("alpha", 0, 0);
        session.add_player("bravo", 5, 0);

        session.submit_input("alpha", PlayerInput(1, 1, 0, false));
        session.submit_input("bravo", PlayerInput(1, -1, 0, false));
        session.advance_to_frame(3);

        ResimResult late = session.submit_input("bravo", PlayerInput(2, 0, 0, false));
        StateSnapshot snapshot = session.snapshot_at(2);

        expect(late.rolled_back, "late bravo input should rollback");
        expect(late.converged, "rollback replay should converge");
        expect(snapshot.world.players["alpha"].x == 2, "alpha should keep predicted forward movement");
        expect(snapshot.world.players["bravo"].x == 4, "bravo should stop at frame 2 after correction");
        expect(session.world().players["bravo"].x == 4, "frame 3 should predict bravo idle after correction");
    }
}

int main()
{
    try
    {
        test_future_input_buffers_without_rollback();
        test_late_input_triggers_rollback_and_replay();
        test_identical_late_input_is_fast_path();
        test_snapshot_and_resimulation_with_two_players();
        std::cout << "rollbacklab tests passed." << std::endl;
        return 0;
    }
    catch (const std::exception &e)
    {
        std::cerr << "rollbacklab tests failed: " << e.what() << std::endl;
        return 1;
    }
}
