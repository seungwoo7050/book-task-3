#pragma once

#include <cstdint>
#include <mutex>
#include <string>
#include <vector>

#include "arena/protocol.hpp"

struct sqlite3;

namespace arena {

struct PersistentProfile {
    std::uint32_t player_id{0};
    std::string name;
    int games_played{0};
    int wins{0};
    int losses{0};
    int kills{0};
    int deaths{0};
};

class SqliteRepository {
public:
    explicit SqliteRepository(std::string db_path);
    ~SqliteRepository();

    SqliteRepository(const SqliteRepository&) = delete;
    SqliteRepository& operator=(const SqliteRepository&) = delete;

    void initialize();
    PersistentProfile login_or_create(const std::string& player_name);
    PersistentProfile load_profile(std::uint32_t player_id);
    void record_match(
        std::uint64_t started_at_ms,
        std::uint64_t ended_at_ms,
        std::uint32_t winner_player_id,
        const std::vector<EntitySnapshot>& entities,
        const std::string& result_blob
    );
    int match_history_count() const;
    std::string latest_result_blob() const;

private:
    sqlite3* db_{nullptr};
    std::string db_path_;
    mutable std::mutex mutex_;

    void exec_or_throw(const std::string& sql) const;
    PersistentProfile load_profile_locked(std::uint32_t player_id) const;
    static std::string now_iso8601();
};

}  // namespace arena
