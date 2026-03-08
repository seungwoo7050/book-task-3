#pragma once

#include <cstdint>
#include <optional>
#include <string>
#include <string_view>
#include <unordered_map>
#include <vector>

namespace arena {

struct ControlMessage {
    std::string verb;
    std::unordered_map<std::string, std::string> fields;
};

std::optional<ControlMessage> parse_control_line(const std::string& line);
std::string format_control_line(const ControlMessage& message);
std::string slugify(std::string_view value);
std::string make_resume_token(uint32_t player_id, uint64_t nonce);

enum class PacketKind : std::uint8_t {
    input = 1,
    snapshot = 2,
    heartbeat = 3,
};

struct InputPacket {
    std::uint8_t version{1};
    PacketKind kind{PacketKind::input};
    std::uint32_t match_id{0};
    std::uint32_t player_id{0};
    std::uint32_t sequence{0};
    std::int8_t move_x{0};
    std::int8_t move_y{0};
    std::int16_t aim_x{0};
    std::int16_t aim_y{0};
    std::uint8_t fire{0};
    std::uint8_t dash{0};
};

struct HeartbeatPacket {
    std::uint8_t version{1};
    PacketKind kind{PacketKind::heartbeat};
    std::uint32_t match_id{0};
    std::uint32_t player_id{0};
    std::uint32_t sequence{0};
};

struct EntitySnapshot {
    std::uint32_t player_id{0};
    float x{0.0F};
    float y{0.0F};
    std::uint16_t hp{0};
    std::uint16_t kills{0};
    std::uint16_t deaths{0};
    std::uint8_t alive{0};
    std::uint32_t last_input_sequence{0};
};

struct SnapshotPacket {
    std::uint8_t version{1};
    PacketKind kind{PacketKind::snapshot};
    std::uint32_t match_id{0};
    std::uint32_t player_id{0};
    std::uint32_t sequence{0};
    std::uint32_t server_tick{0};
    std::uint8_t entity_count{0};
    std::uint8_t projectile_count{0};
    std::vector<EntitySnapshot> entities;
};

std::vector<std::uint8_t> encode_input_packet(const InputPacket& packet);
std::optional<InputPacket> decode_input_packet(
    const std::uint8_t* data, std::size_t size
);

std::vector<std::uint8_t> encode_heartbeat_packet(const HeartbeatPacket& packet);
std::optional<HeartbeatPacket> decode_heartbeat_packet(
    const std::uint8_t* data, std::size_t size
);

std::vector<std::uint8_t> encode_snapshot_packet(const SnapshotPacket& packet);
std::optional<SnapshotPacket> decode_snapshot_packet(
    const std::uint8_t* data, std::size_t size
);

}  // namespace arena
