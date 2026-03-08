#include "arena/state.hpp"

#include <algorithm>
#include <cmath>
#include <sstream>

namespace arena {
namespace {

constexpr float kPlayerRadius = 18.0F;
constexpr float kProjectileRadius = 6.0F;

float length(float x, float y) {
    return std::sqrt((x * x) + (y * y));
}

}  // namespace

MatchState::MatchState(
    std::string room_id,
    std::uint32_t match_id,
    ArenaConfig config,
    std::vector<PlayerDefinition> players,
    std::uint64_t start_ms
)
    : room_id_(std::move(room_id)),
      match_id_(match_id),
      config_(config),
      start_ms_(start_ms),
      last_step_ms_(start_ms) {
    players_.reserve(players.size());
    for (const auto& player : players) {
        PlayerRuntime runtime;
        runtime.definition = player;
        runtime.x = player.spawn_x;
        runtime.y = player.spawn_y;
        players_.push_back(runtime);
    }
}

bool MatchState::player_known(std::uint32_t player_id) const {
    return find_player(player_id) != nullptr;
}

void MatchState::submit_input(const InputPacket& input) {
    if (auto* player = find_player_mut(input.player_id)) {
        if (input.sequence > player->latest_input.sequence) {
            player->latest_input = input;
        }
    }
}

void MatchState::mark_disconnected(std::uint32_t player_id, std::uint64_t now_ms) {
    if (auto* player = find_player_mut(player_id)) {
        player->connected = false;
        player->disconnected_at_ms = now_ms;
    }
}

void MatchState::mark_reconnected(std::uint32_t player_id) {
    if (auto* player = find_player_mut(player_id)) {
        player->connected = true;
        player->disconnected_at_ms = 0;
    }
}

std::optional<MatchResult> MatchState::step(std::uint64_t now_ms) {
    if (finished_) {
        return std::nullopt;
    }

    const auto delta_ms = std::max<std::uint64_t>(1, now_ms - last_step_ms_);
    const auto dt_seconds = static_cast<float>(delta_ms) / 1000.0F;
    last_step_ms_ = now_ms;
    ++server_tick_;

    apply_forfeit_timeouts(now_ms);
    respawn_players(now_ms);
    apply_inputs(now_ms, dt_seconds);
    update_projectiles(now_ms, dt_seconds);

    if (should_finish(now_ms)) {
        finished_ = true;
        return build_result();
    }
    return std::nullopt;
}

SnapshotPacket MatchState::build_snapshot_packet(std::uint32_t sequence) const {
    SnapshotPacket packet;
    packet.match_id = match_id_;
    packet.sequence = sequence;
    packet.server_tick = server_tick_;
    packet.entity_count = static_cast<std::uint8_t>(players_.size());
    packet.projectile_count = static_cast<std::uint8_t>(
        std::min<std::size_t>(255, projectiles_.size())
    );
    packet.entities.reserve(players_.size());
    for (const auto& player : players_) {
        EntitySnapshot entity;
        entity.player_id = player.definition.player_id;
        entity.x = player.x;
        entity.y = player.y;
        entity.hp = static_cast<std::uint16_t>(std::max(0, player.hp));
        entity.kills = player.kills;
        entity.deaths = player.deaths;
        entity.alive = static_cast<std::uint8_t>(player.alive ? 1 : 0);
        entity.last_input_sequence = player.latest_input.sequence;
        packet.entities.push_back(entity);
    }
    return packet;
}

std::optional<EntitySnapshot> MatchState::snapshot_for_player(std::uint32_t player_id) const {
    const auto* player = find_player(player_id);
    if (player == nullptr) {
        return std::nullopt;
    }
    EntitySnapshot entity;
    entity.player_id = player->definition.player_id;
    entity.x = player->x;
    entity.y = player->y;
    entity.hp = static_cast<std::uint16_t>(std::max(0, player->hp));
    entity.kills = player->kills;
    entity.deaths = player->deaths;
    entity.alive = static_cast<std::uint8_t>(player->alive ? 1 : 0);
    entity.last_input_sequence = player->latest_input.sequence;
    return entity;
}

bool MatchState::has_forfeited(std::uint32_t player_id) const {
    const auto* player = find_player(player_id);
    return player != nullptr && player->forfeited;
}

bool MatchState::finished() const {
    return finished_;
}

std::uint32_t MatchState::match_id() const {
    return match_id_;
}

const std::string& MatchState::room_id() const {
    return room_id_;
}

MatchState::PlayerRuntime* MatchState::find_player_mut(std::uint32_t player_id) {
    auto it = std::find_if(players_.begin(), players_.end(), [&](const auto& player) {
        return player.definition.player_id == player_id;
    });
    if (it == players_.end()) {
        return nullptr;
    }
    return &(*it);
}

const MatchState::PlayerRuntime* MatchState::find_player(std::uint32_t player_id) const {
    auto it = std::find_if(players_.begin(), players_.end(), [&](const auto& player) {
        return player.definition.player_id == player_id;
    });
    if (it == players_.end()) {
        return nullptr;
    }
    return &(*it);
}

void MatchState::apply_inputs(std::uint64_t now_ms, float dt_seconds) {
    for (auto& player : players_) {
        if (!player.alive || player.forfeited) {
            continue;
        }
        const auto move_len = length(
            static_cast<float>(player.latest_input.move_x),
            static_cast<float>(player.latest_input.move_y)
        );
        if (move_len > 0.0F) {
            const auto normalized_x =
                static_cast<float>(player.latest_input.move_x) / move_len;
            const auto normalized_y =
                static_cast<float>(player.latest_input.move_y) / move_len;
            auto speed = config_.player_speed;
            if (player.latest_input.dash != 0 && now_ms >= player.dash_ready_at_ms) {
                speed *= config_.dash_multiplier;
                player.dash_ready_at_ms = now_ms + config_.dash_cooldown_ms;
            }
            player.x = clamp_x(player.x + (normalized_x * speed * dt_seconds));
            player.y = clamp_y(player.y + (normalized_y * speed * dt_seconds));
        }

        if (player.latest_input.fire != 0 && now_ms >= player.fire_ready_at_ms) {
            float aim_x = static_cast<float>(player.latest_input.aim_x);
            float aim_y = static_cast<float>(player.latest_input.aim_y);
            if (length(aim_x, aim_y) == 0.0F) {
                aim_y = 1.0F;
            }
            const auto aim_len = length(aim_x, aim_y);
            Projectile projectile;
            projectile.owner_player_id = player.definition.player_id;
            projectile.x = player.x;
            projectile.y = player.y;
            projectile.vx = (aim_x / aim_len) * config_.projectile_speed;
            projectile.vy = (aim_y / aim_len) * config_.projectile_speed;
            projectile.expires_at_ms = now_ms + config_.projectile_lifetime_ms;
            projectiles_.push_back(projectile);
            player.fire_ready_at_ms = now_ms + config_.fire_cooldown_ms;
        }
    }
}

void MatchState::update_projectiles(std::uint64_t now_ms, float dt_seconds) {
    std::vector<Projectile> next_projectiles;
    next_projectiles.reserve(projectiles_.size());
    for (auto projectile : projectiles_) {
        projectile.x += projectile.vx * dt_seconds;
        projectile.y += projectile.vy * dt_seconds;
        if (projectile.expires_at_ms <= now_ms) {
            continue;
        }
        if (
            projectile.x < 0.0F || projectile.y < 0.0F ||
            projectile.x > config_.arena_width || projectile.y > config_.arena_height
        ) {
            continue;
        }

        bool consumed = false;
        for (auto& player : players_) {
            if (
                player.definition.player_id == projectile.owner_player_id ||
                !player.alive || player.forfeited
            ) {
                continue;
            }
            const auto dx = player.x - projectile.x;
            const auto dy = player.y - projectile.y;
            const auto distance = length(dx, dy);
            if (distance > (kPlayerRadius + kProjectileRadius)) {
                continue;
            }
            player.hp -= config_.projectile_damage;
            consumed = true;
            if (player.hp <= 0) {
                player.hp = 0;
                player.alive = false;
                player.deaths += 1;
                player.respawn_at_ms = now_ms + config_.respawn_delay_ms;
                if (auto* killer = find_player_mut(projectile.owner_player_id)) {
                    killer->kills += 1;
                    killer->recent_kill_at_ms = now_ms;
                }
            }
            break;
        }

        if (!consumed) {
            next_projectiles.push_back(projectile);
        }
    }
    projectiles_ = std::move(next_projectiles);
}

void MatchState::respawn_players(std::uint64_t now_ms) {
    for (auto& player : players_) {
        if (player.alive || player.forfeited) {
            continue;
        }
        if (player.respawn_at_ms == 0 || player.respawn_at_ms > now_ms) {
            continue;
        }
        player.alive = true;
        player.hp = 100;
        player.x = player.definition.spawn_x;
        player.y = player.definition.spawn_y;
        player.respawn_at_ms = 0;
    }
}

void MatchState::apply_forfeit_timeouts(std::uint64_t now_ms) {
    for (auto& player : players_) {
        if (player.connected || player.forfeited || player.disconnected_at_ms == 0) {
            continue;
        }
        if ((now_ms - player.disconnected_at_ms) < static_cast<std::uint64_t>(config_.resume_window_ms)) {
            continue;
        }
        player.forfeited = true;
        player.alive = false;
        player.hp = 0;
    }
}

bool MatchState::should_finish(std::uint64_t now_ms) const {
    if ((now_ms - start_ms_) >= static_cast<std::uint64_t>(config_.match_duration_ms)) {
        return true;
    }
    std::size_t non_forfeited = 0;
    for (const auto& player : players_) {
        if (!player.forfeited) {
            non_forfeited += 1;
        }
    }
    return non_forfeited <= 1;
}

MatchResult MatchState::build_result() const {
    const auto winner = std::max_element(players_.begin(), players_.end(), [](const auto& lhs, const auto& rhs) {
        if (lhs.forfeited != rhs.forfeited) {
            return lhs.forfeited && !rhs.forfeited;
        }
        if (lhs.kills != rhs.kills) {
            return lhs.kills < rhs.kills;
        }
        if (lhs.deaths != rhs.deaths) {
            return lhs.deaths > rhs.deaths;
        }
        if (lhs.recent_kill_at_ms != rhs.recent_kill_at_ms) {
            return lhs.recent_kill_at_ms < rhs.recent_kill_at_ms;
        }
        return lhs.definition.player_id > rhs.definition.player_id;
    });

    MatchResult result;
    result.winner_player_id =
        (winner != players_.end() && !winner->forfeited) ? winner->definition.player_id : 0;
    {
        std::ostringstream scoreboard;
        bool first = true;
        for (const auto& player : players_) {
            if (!first) {
                scoreboard << ',';
            }
            first = false;
            scoreboard
                << player.definition.player_id << ':'
                << player.kills << ':'
                << player.deaths;
        }
        result.scoreboard_blob = scoreboard.str();
    }

    std::ostringstream blob;
    blob << "winner=" << result.winner_player_id << ";forfeits=";
    bool first = true;
    for (const auto& player : players_) {
        if (!player.forfeited) {
            continue;
        }
        if (!first) {
            blob << ',';
        }
        first = false;
        blob << player.definition.player_id;
    }
    blob << ";scoreboard=" << result.scoreboard_blob;
    result.result_blob = blob.str();
    return result;
}

float MatchState::clamp_x(float value) const {
    return std::clamp(value, 0.0F, config_.arena_width);
}

float MatchState::clamp_y(float value) const {
    return std::clamp(value, 0.0F, config_.arena_height);
}

}  // namespace arena
