#include "arena/repository.hpp"

#include <ctime>
#include <iomanip>
#include <sstream>
#include <stdexcept>

#include <sqlite3.h>

namespace arena {
namespace {

class Statement final {
public:
    Statement(sqlite3* db, const char* sql) {
        if (sqlite3_prepare_v2(db, sql, -1, &stmt_, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(db));
        }
    }

    ~Statement() {
        if (stmt_ != nullptr) {
            sqlite3_finalize(stmt_);
        }
    }

    sqlite3_stmt* get() { return stmt_; }

private:
    sqlite3_stmt* stmt_{nullptr};
};

PersistentProfile read_profile_row(sqlite3_stmt* stmt) {
    PersistentProfile profile;
    profile.player_id = static_cast<std::uint32_t>(sqlite3_column_int(stmt, 0));
    profile.name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
    profile.games_played = sqlite3_column_int(stmt, 2);
    profile.wins = sqlite3_column_int(stmt, 3);
    profile.losses = sqlite3_column_int(stmt, 4);
    profile.kills = sqlite3_column_int(stmt, 5);
    profile.deaths = sqlite3_column_int(stmt, 6);
    return profile;
}

}  // namespace

SqliteRepository::SqliteRepository(std::string db_path) : db_path_(std::move(db_path)) {
    if (sqlite3_open(db_path_.c_str(), &db_) != SQLITE_OK) {
        throw std::runtime_error("failed to open sqlite database");
    }
}

SqliteRepository::~SqliteRepository() {
    if (db_ != nullptr) {
        sqlite3_close(db_);
    }
}

void SqliteRepository::initialize() {
    std::scoped_lock lock(mutex_);
    exec_or_throw(
        "CREATE TABLE IF NOT EXISTS players ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name TEXT UNIQUE NOT NULL, "
        "created_at TEXT NOT NULL, "
        "last_login_at TEXT NOT NULL"
        ");"
    );
    exec_or_throw(
        "CREATE TABLE IF NOT EXISTS player_stats ("
        "player_id INTEGER PRIMARY KEY, "
        "games_played INTEGER NOT NULL DEFAULT 0, "
        "wins INTEGER NOT NULL DEFAULT 0, "
        "losses INTEGER NOT NULL DEFAULT 0, "
        "kills INTEGER NOT NULL DEFAULT 0, "
        "deaths INTEGER NOT NULL DEFAULT 0, "
        "FOREIGN KEY(player_id) REFERENCES players(id)"
        ");"
    );
    exec_or_throw(
        "CREATE TABLE IF NOT EXISTS match_history ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "started_at TEXT NOT NULL, "
        "ended_at TEXT NOT NULL, "
        "winner_player_id INTEGER NOT NULL, "
        "result_blob TEXT NOT NULL"
        ");"
    );
}

PersistentProfile SqliteRepository::login_or_create(const std::string& player_name) {
    std::scoped_lock lock(mutex_);
    const auto now = now_iso8601();

    {
        Statement insert(db_,
            "INSERT OR IGNORE INTO players(name, created_at, last_login_at) VALUES (?, ?, ?)"
        );
        sqlite3_bind_text(insert.get(), 1, player_name.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(insert.get(), 2, now.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(insert.get(), 3, now.c_str(), -1, SQLITE_TRANSIENT);
        if (sqlite3_step(insert.get()) == SQLITE_ERROR) {
            throw std::runtime_error(sqlite3_errmsg(db_));
        }
    }

    std::uint32_t player_id = 0;
    {
        Statement select(db_, "SELECT id FROM players WHERE name = ?");
        sqlite3_bind_text(select.get(), 1, player_name.c_str(), -1, SQLITE_TRANSIENT);
        if (sqlite3_step(select.get()) != SQLITE_ROW) {
            throw std::runtime_error("player lookup failed");
        }
        player_id = static_cast<std::uint32_t>(sqlite3_column_int(select.get(), 0));
    }

    {
        Statement update(db_, "UPDATE players SET last_login_at = ? WHERE id = ?");
        sqlite3_bind_text(update.get(), 1, now.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_int(update.get(), 2, static_cast<int>(player_id));
        if (sqlite3_step(update.get()) == SQLITE_ERROR) {
            throw std::runtime_error(sqlite3_errmsg(db_));
        }
    }

    {
        Statement stats(db_,
            "INSERT OR IGNORE INTO player_stats(player_id, games_played, wins, losses, kills, deaths) "
            "VALUES (?, 0, 0, 0, 0, 0)"
        );
        sqlite3_bind_int(stats.get(), 1, static_cast<int>(player_id));
        if (sqlite3_step(stats.get()) == SQLITE_ERROR) {
            throw std::runtime_error(sqlite3_errmsg(db_));
        }
    }

    return load_profile_locked(player_id);
}

PersistentProfile SqliteRepository::load_profile(std::uint32_t player_id) {
    std::scoped_lock lock(mutex_);
    return load_profile_locked(player_id);
}

PersistentProfile SqliteRepository::load_profile_locked(std::uint32_t player_id) const {
    Statement stmt(db_,
        "SELECT players.id, players.name, player_stats.games_played, player_stats.wins, "
        "player_stats.losses, player_stats.kills, player_stats.deaths "
        "FROM players JOIN player_stats ON players.id = player_stats.player_id "
        "WHERE players.id = ?"
    );
    sqlite3_bind_int(stmt.get(), 1, static_cast<int>(player_id));
    if (sqlite3_step(stmt.get()) != SQLITE_ROW) {
        throw std::runtime_error("profile not found");
    }
    return read_profile_row(stmt.get());
}

void SqliteRepository::record_match(
    std::uint64_t /*started_at_ms*/,
    std::uint64_t /*ended_at_ms*/,
    std::uint32_t winner_player_id,
    const std::vector<EntitySnapshot>& entities,
    const std::string& result_blob
) {
    std::scoped_lock lock(mutex_);
    exec_or_throw("BEGIN TRANSACTION");
    try {
        {
            Statement insert(db_,
                "INSERT INTO match_history(started_at, ended_at, winner_player_id, result_blob) "
                "VALUES (?, ?, ?, ?)"
            );
            const auto now = now_iso8601();
            sqlite3_bind_text(insert.get(), 1, now.c_str(), -1, SQLITE_TRANSIENT);
            sqlite3_bind_text(insert.get(), 2, now.c_str(), -1, SQLITE_TRANSIENT);
            sqlite3_bind_int(insert.get(), 3, static_cast<int>(winner_player_id));
            sqlite3_bind_text(insert.get(), 4, result_blob.c_str(), -1, SQLITE_TRANSIENT);
            if (sqlite3_step(insert.get()) == SQLITE_ERROR) {
                throw std::runtime_error(sqlite3_errmsg(db_));
            }
        }

        for (const auto& entity : entities) {
            Statement update(db_,
                "UPDATE player_stats SET games_played = games_played + 1, "
                "wins = wins + ?, losses = losses + ?, kills = kills + ?, deaths = deaths + ? "
                "WHERE player_id = ?"
            );
            sqlite3_bind_int(update.get(), 1, entity.player_id == winner_player_id ? 1 : 0);
            sqlite3_bind_int(update.get(), 2, entity.player_id == winner_player_id ? 0 : 1);
            sqlite3_bind_int(update.get(), 3, entity.kills);
            sqlite3_bind_int(update.get(), 4, entity.deaths);
            sqlite3_bind_int(update.get(), 5, static_cast<int>(entity.player_id));
            if (sqlite3_step(update.get()) == SQLITE_ERROR) {
                throw std::runtime_error(sqlite3_errmsg(db_));
            }
        }

        exec_or_throw("COMMIT");
    } catch (...) {
        exec_or_throw("ROLLBACK");
        throw;
    }
}

int SqliteRepository::match_history_count() const {
    std::scoped_lock lock(mutex_);
    Statement stmt(db_, "SELECT COUNT(*) FROM match_history");
    if (sqlite3_step(stmt.get()) != SQLITE_ROW) {
        throw std::runtime_error("match_history_count failed");
    }
    return sqlite3_column_int(stmt.get(), 0);
}

std::string SqliteRepository::latest_result_blob() const {
    std::scoped_lock lock(mutex_);
    Statement stmt(db_,
        "SELECT result_blob FROM match_history ORDER BY id DESC LIMIT 1"
    );
    if (sqlite3_step(stmt.get()) != SQLITE_ROW) {
        return {};
    }
    return reinterpret_cast<const char*>(sqlite3_column_text(stmt.get(), 0));
}

void SqliteRepository::exec_or_throw(const std::string& sql) const {
    char* error_message = nullptr;
    if (sqlite3_exec(db_, sql.c_str(), nullptr, nullptr, &error_message) != SQLITE_OK) {
        const std::string message = error_message != nullptr ? error_message : "sqlite error";
        sqlite3_free(error_message);
        throw std::runtime_error(message);
    }
}

std::string SqliteRepository::now_iso8601() {
    const auto now = std::time(nullptr);
    std::tm tm{};
#if defined(_WIN32)
    gmtime_s(&tm, &now);
#else
    gmtime_r(&now, &tm);
#endif
    std::ostringstream stream;
    stream << std::put_time(&tm, "%Y-%m-%dT%H:%M:%SZ");
    return stream.str();
}

}  // namespace arena
