#include "arena/repository.hpp"

#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <stdexcept>

namespace {

void expect(bool condition, const std::string& message) {
    if (!condition) {
        throw std::runtime_error(message);
    }
}

}  // namespace

int main() {
    using namespace arena;

    const auto db_path = "/tmp/tactical_arena_repo_test.sqlite3";
    std::remove(db_path);

    SqliteRepository repository(db_path);
    repository.initialize();

    const auto alpha = repository.login_or_create("alpha");
    const auto beta = repository.login_or_create("beta");
    expect(alpha.player_id != beta.player_id, "players should have unique ids");

    const std::vector<EntitySnapshot> entities{
        {alpha.player_id, 0.0F, 0.0F, 100, 3, 1, 1, 10},
        {beta.player_id, 0.0F, 0.0F, 0, 1, 4, 0, 12},
    };
    repository.record_match(0, 1000, alpha.player_id, entities, "winner=1;scoreboard=1:3:1,2:1:4");

    expect(repository.match_history_count() == 1, "match history should contain one row");
    expect(
        repository.latest_result_blob().find("scoreboard=") != std::string::npos,
        "latest result blob should be stored"
    );

    const auto updated_alpha = repository.load_profile(alpha.player_id);
    const auto updated_beta = repository.load_profile(beta.player_id);
    expect(updated_alpha.wins == 1, "winner wins should increment");
    expect(updated_alpha.games_played == 1, "winner games_played should increment");
    expect(updated_alpha.kills == 3, "winner kills should increment");
    expect(updated_beta.losses == 1, "loser losses should increment");
    expect(updated_beta.deaths == 4, "loser deaths should increment");

    std::remove(db_path);
    std::cout << "test_repository ok\n";
    return EXIT_SUCCESS;
}
