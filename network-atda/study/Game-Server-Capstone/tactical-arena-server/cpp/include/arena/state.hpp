#pragma once

#include <cstdint>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

#include "arena/protocol.hpp"

namespace arena {

struct ArenaConfig {
    int tick_hz{20};
    int snapshot_hz{10};
    int match_duration_ms{90'000};
    int resume_window_ms{20'000};
    float arena_width{1000.0F};
    float arena_height{1000.0F};
    float player_speed{180.0F};
    float dash_multiplier{2.4F};
    int dash_cooldown_ms{3'000};
    int fire_cooldown_ms{400};
    float projectile_speed{420.0F};
    int projectile_damage{25};
    int projectile_lifetime_ms{1'500};
    int respawn_delay_ms{3'000};
};

struct PlayerDefinition {
    std::uint32_t player_id{0};
    std::string name;
    float spawn_x{0.0F};
    float spawn_y{0.0F};
};

struct MatchResult {
    std::uint32_t winner_player_id{0};
    std::string scoreboard_blob;
    std::string result_blob;
};

class MatchState {
public:
    MatchState(
        std::string room_id,
        std::uint32_t match_id,
        ArenaConfig config,
        std::vector<PlayerDefinition> players,
        std::uint64_t start_ms
    );

    bool player_known(std::uint32_t player_id) const;
    void submit_input(const InputPacket& input);
    void mark_disconnected(std::uint32_t player_id, std::uint64_t now_ms);
    void mark_reconnected(std::uint32_t player_id);
    std::optional<MatchResult> step(std::uint64_t now_ms);
    SnapshotPacket build_snapshot_packet(std::uint32_t sequence) const;
    std::optional<EntitySnapshot> snapshot_for_player(std::uint32_t player_id) const;
    bool has_forfeited(std::uint32_t player_id) const;
    bool finished() const;
    std::uint32_t match_id() const;
    const std::string& room_id() const;

private:
    struct PlayerRuntime {
        PlayerDefinition definition;
        InputPacket latest_input;
        float x{0.0F};
        float y{0.0F};
        int hp{100};
        bool alive{true};
        bool forfeited{false};
        bool connected{true};
        std::uint64_t disconnected_at_ms{0};
        std::uint64_t respawn_at_ms{0};
        std::uint64_t dash_ready_at_ms{0};
        std::uint64_t fire_ready_at_ms{0};
        std::uint64_t recent_kill_at_ms{0};
        std::uint16_t kills{0};
        std::uint16_t deaths{0};
    };

    struct Projectile {
        std::uint32_t owner_player_id{0};
        float x{0.0F};
        float y{0.0F};
        float vx{0.0F};
        float vy{0.0F};
        std::uint64_t expires_at_ms{0};
    };

    PlayerRuntime* find_player_mut(std::uint32_t player_id);
    const PlayerRuntime* find_player(std::uint32_t player_id) const;
    void apply_inputs(std::uint64_t now_ms, float dt_seconds);
    void update_projectiles(std::uint64_t now_ms, float dt_seconds);
    void respawn_players(std::uint64_t now_ms);
    void apply_forfeit_timeouts(std::uint64_t now_ms);
    bool should_finish(std::uint64_t now_ms) const;
    MatchResult build_result() const;
    float clamp_x(float value) const;
    float clamp_y(float value) const;

    std::string room_id_;
    std::uint32_t match_id_{0};
    ArenaConfig config_;
    std::uint64_t start_ms_{0};
    std::uint64_t last_step_ms_{0};
    std::vector<PlayerRuntime> players_;
    std::vector<Projectile> projectiles_;
    bool finished_{false};
    std::uint32_t server_tick_{0};
};

}  // namespace arena
