#include "arena/protocol.hpp"

#include <algorithm>
#include <bit>
#include <charconv>
#include <cctype>
#include <cstring>
#include <sstream>

namespace arena {
namespace {

template <typename UInt>
void append_be(std::vector<std::uint8_t>& output, UInt value) {
    for (int shift = (sizeof(UInt) - 1) * 8; shift >= 0; shift -= 8) {
        output.push_back(static_cast<std::uint8_t>((value >> shift) & 0xFFU));
    }
}

template <typename UInt>
std::optional<UInt> read_be(const std::uint8_t*& cursor, std::size_t& remaining) {
    if (remaining < sizeof(UInt)) {
        return std::nullopt;
    }
    UInt value = 0;
    for (std::size_t i = 0; i < sizeof(UInt); ++i) {
        value = static_cast<UInt>((value << 8U) | cursor[i]);
    }
    cursor += sizeof(UInt);
    remaining -= sizeof(UInt);
    return value;
}

void append_float(std::vector<std::uint8_t>& output, float value) {
    append_be(output, std::bit_cast<std::uint32_t>(value));
}

std::optional<float> read_float(const std::uint8_t*& cursor, std::size_t& remaining) {
    const auto raw = read_be<std::uint32_t>(cursor, remaining);
    if (!raw) {
        return std::nullopt;
    }
    return std::bit_cast<float>(*raw);
}

std::string trim_copy(std::string value) {
    auto is_space = [](unsigned char ch) { return std::isspace(ch) != 0; };
    value.erase(
        value.begin(),
        std::find_if(value.begin(), value.end(), [&](char ch) {
            return !is_space(static_cast<unsigned char>(ch));
        })
    );
    value.erase(
        std::find_if(value.rbegin(), value.rend(), [&](char ch) {
            return !is_space(static_cast<unsigned char>(ch));
        }).base(),
        value.end()
    );
    return value;
}

}  // namespace

std::optional<ControlMessage> parse_control_line(const std::string& raw_line) {
    std::string line = trim_copy(raw_line);
    if (line.empty()) {
        return std::nullopt;
    }

    std::istringstream stream(line);
    ControlMessage message;
    if (!(stream >> message.verb)) {
        return std::nullopt;
    }

    std::string token;
    while (stream >> token) {
        const auto pos = token.find('=');
        if (pos == std::string::npos || pos == 0 || pos == token.size() - 1) {
            return std::nullopt;
        }
        message.fields[token.substr(0, pos)] = token.substr(pos + 1);
    }
    return message;
}

std::string format_control_line(const ControlMessage& message) {
    std::ostringstream stream;
    stream << message.verb;
    for (const auto& [key, value] : message.fields) {
        stream << ' ' << key << '=' << value;
    }
    stream << '\n';
    return stream.str();
}

std::string slugify(std::string_view value) {
    std::string out;
    out.reserve(value.size());
    for (const char ch : value) {
        if (std::isalnum(static_cast<unsigned char>(ch)) != 0) {
            out.push_back(static_cast<char>(std::tolower(static_cast<unsigned char>(ch))));
        } else if (ch == '-' || ch == '_') {
            out.push_back(ch);
        }
    }
    if (out.empty()) {
        return "unnamed";
    }
    return out;
}

std::string make_resume_token(std::uint32_t player_id, std::uint64_t nonce) {
    std::ostringstream stream;
    stream << std::hex << player_id << '-' << nonce;
    return stream.str();
}

std::vector<std::uint8_t> encode_input_packet(const InputPacket& packet) {
    std::vector<std::uint8_t> output;
    output.reserve(20);
    output.push_back(packet.version);
    output.push_back(static_cast<std::uint8_t>(packet.kind));
    append_be<std::uint16_t>(output, 0);
    append_be(output, packet.match_id);
    append_be(output, packet.player_id);
    append_be(output, packet.sequence);
    output.push_back(static_cast<std::uint8_t>(packet.move_x));
    output.push_back(static_cast<std::uint8_t>(packet.move_y));
    append_be(output, static_cast<std::uint16_t>(packet.aim_x));
    append_be(output, static_cast<std::uint16_t>(packet.aim_y));
    output.push_back(packet.fire);
    output.push_back(packet.dash);
    return output;
}

std::optional<InputPacket> decode_input_packet(const std::uint8_t* data, std::size_t size) {
    if (size != 24) {
        return std::nullopt;
    }
    const auto* cursor = data;
    auto remaining = size;
    InputPacket packet;
    packet.version = *cursor++;
    remaining -= 1;
    packet.kind = static_cast<PacketKind>(*cursor++);
    remaining -= 1;
    (void)read_be<std::uint16_t>(cursor, remaining);
    packet.match_id = *read_be<std::uint32_t>(cursor, remaining);
    packet.player_id = *read_be<std::uint32_t>(cursor, remaining);
    packet.sequence = *read_be<std::uint32_t>(cursor, remaining);
    packet.move_x = static_cast<std::int8_t>(*cursor++);
    remaining -= 1;
    packet.move_y = static_cast<std::int8_t>(*cursor++);
    remaining -= 1;
    packet.aim_x = static_cast<std::int16_t>(*read_be<std::uint16_t>(cursor, remaining));
    packet.aim_y = static_cast<std::int16_t>(*read_be<std::uint16_t>(cursor, remaining));
    packet.fire = *cursor++;
    remaining -= 1;
    packet.dash = *cursor++;
    remaining -= 1;
    return packet;
}

std::vector<std::uint8_t> encode_heartbeat_packet(const HeartbeatPacket& packet) {
    std::vector<std::uint8_t> output;
    output.reserve(16);
    output.push_back(packet.version);
    output.push_back(static_cast<std::uint8_t>(packet.kind));
    append_be<std::uint16_t>(output, 0);
    append_be(output, packet.match_id);
    append_be(output, packet.player_id);
    append_be(output, packet.sequence);
    return output;
}

std::optional<HeartbeatPacket> decode_heartbeat_packet(
    const std::uint8_t* data, std::size_t size
) {
    if (size != 16) {
        return std::nullopt;
    }
    const auto* cursor = data;
    auto remaining = size;
    HeartbeatPacket packet;
    packet.version = *cursor++;
    remaining -= 1;
    packet.kind = static_cast<PacketKind>(*cursor++);
    remaining -= 1;
    (void)read_be<std::uint16_t>(cursor, remaining);
    packet.match_id = *read_be<std::uint32_t>(cursor, remaining);
    packet.player_id = *read_be<std::uint32_t>(cursor, remaining);
    packet.sequence = *read_be<std::uint32_t>(cursor, remaining);
    return packet;
}

std::vector<std::uint8_t> encode_snapshot_packet(const SnapshotPacket& packet) {
    std::vector<std::uint8_t> output;
    output.reserve(24 + packet.entities.size() * 24);
    output.push_back(packet.version);
    output.push_back(static_cast<std::uint8_t>(packet.kind));
    append_be<std::uint16_t>(output, 0);
    append_be(output, packet.match_id);
    append_be(output, packet.player_id);
    append_be(output, packet.sequence);
    append_be(output, packet.server_tick);
    output.push_back(packet.entity_count);
    output.push_back(packet.projectile_count);
    append_be<std::uint16_t>(output, 0);
    for (const auto& entity : packet.entities) {
        append_be(output, entity.player_id);
        append_float(output, entity.x);
        append_float(output, entity.y);
        append_be(output, entity.hp);
        append_be(output, entity.kills);
        append_be(output, entity.deaths);
        output.push_back(entity.alive);
        output.push_back(0);
        append_be(output, entity.last_input_sequence);
    }
    return output;
}

std::optional<SnapshotPacket> decode_snapshot_packet(
    const std::uint8_t* data, std::size_t size
) {
    if (size < 24) {
        return std::nullopt;
    }
    const auto* cursor = data;
    auto remaining = size;
    SnapshotPacket packet;
    packet.version = *cursor++;
    remaining -= 1;
    packet.kind = static_cast<PacketKind>(*cursor++);
    remaining -= 1;
    (void)read_be<std::uint16_t>(cursor, remaining);
    packet.match_id = *read_be<std::uint32_t>(cursor, remaining);
    packet.player_id = *read_be<std::uint32_t>(cursor, remaining);
    packet.sequence = *read_be<std::uint32_t>(cursor, remaining);
    packet.server_tick = *read_be<std::uint32_t>(cursor, remaining);
    packet.entity_count = *cursor++;
    remaining -= 1;
    packet.projectile_count = *cursor++;
    remaining -= 1;
    (void)read_be<std::uint16_t>(cursor, remaining);
    packet.entities.reserve(packet.entity_count);
    for (std::uint8_t i = 0; i < packet.entity_count; ++i) {
        EntitySnapshot entity;
        entity.player_id = *read_be<std::uint32_t>(cursor, remaining);
        entity.x = *read_float(cursor, remaining);
        entity.y = *read_float(cursor, remaining);
        entity.hp = *read_be<std::uint16_t>(cursor, remaining);
        entity.kills = *read_be<std::uint16_t>(cursor, remaining);
        entity.deaths = *read_be<std::uint16_t>(cursor, remaining);
        entity.alive = *cursor++;
        remaining -= 1;
        ++cursor;
        remaining -= 1;
        entity.last_input_sequence = *read_be<std::uint32_t>(cursor, remaining);
        packet.entities.push_back(entity);
    }
    return packet;
}

}  // namespace arena
