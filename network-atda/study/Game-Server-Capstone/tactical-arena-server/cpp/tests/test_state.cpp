#include "arena/state.hpp"

#include <cstdlib>
#include <iostream>
#include <stdexcept>

namespace {

void expect(bool condition, const std::string& message) {
    if (!condition) {
        throw std::runtime_error(message);
    }
}

arena::MatchState make_match(arena::ArenaConfig config) {
    std::vector<arena::PlayerDefinition> players{
        {1, "alpha", 100.0F, 100.0F},
        {2, "beta", 140.0F, 100.0F},
    };
    return arena::MatchState("room-1", 1, config, players, 0);
}

}  // namespace

int main() {
    using namespace arena;

    {
        ArenaConfig config;
        config.match_duration_ms = 5'000;
        auto match = make_match(config);

        InputPacket newer;
        newer.match_id = 1;
        newer.player_id = 1;
        newer.sequence = 5;
        newer.move_x = 1;

        InputPacket older = newer;
        older.sequence = 4;
        older.move_x = -1;

        match.submit_input(newer);
        match.submit_input(older);
        match.step(100);
        const auto player = match.snapshot_for_player(1);
        expect(player.has_value(), "player snapshot missing");
        expect(player->last_input_sequence == 5, "out-of-order input should be ignored");
        expect(player->x > 100.0F, "newer move input should move player forward");
    }

    {
        ArenaConfig config;
        config.match_duration_ms = 5'000;
        config.projectile_damage = 100;
        config.fire_cooldown_ms = 0;
        auto match = make_match(config);

        InputPacket fire;
        fire.match_id = 1;
        fire.player_id = 1;
        fire.sequence = 1;
        fire.aim_x = 300;
        fire.aim_y = 0;
        fire.fire = 1;

        match.submit_input(fire);
        match.step(100);
        auto target = match.snapshot_for_player(2);
        expect(target.has_value(), "target snapshot missing");
        expect(target->alive == 0, "target should be dead after lethal projectile");
        match.step(3'300);
        target = match.snapshot_for_player(2);
        expect(target->alive == 1, "target should respawn after delay");
    }

    {
        ArenaConfig config;
        config.match_duration_ms = 5'000;
        config.resume_window_ms = 200;
        auto match = make_match(config);
        match.mark_disconnected(2, 1);
        const auto result = match.step(250);
        expect(match.has_forfeited(2), "disconnect timeout should forfeit player");
        expect(result.has_value(), "single remaining player should end match");
        expect(result->winner_player_id == 1, "remaining player should win");
        expect(result->result_blob.find("forfeits=2") != std::string::npos, "forfeit should be recorded");
    }

    {
        ArenaConfig config;
        config.match_duration_ms = 5'000;
        config.resume_window_ms = 200;
        auto match = make_match(config);
        match.mark_disconnected(1, 1);
        const auto result = match.step(250);
        expect(match.has_forfeited(1), "disconnect timeout should forfeit the disconnected player");
        expect(result.has_value(), "match should end when only one player remains");
        expect(result->winner_player_id == 2, "non-forfeited player should win regardless of player id");
    }

    std::cout << "test_state ok\n";
    return EXIT_SUCCESS;
}
