#include "arena/protocol.hpp"

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

    const auto parsed = parse_control_line("LOGIN name=alpha");
    expect(parsed.has_value(), "control line should parse");
    expect(parsed->verb == "LOGIN", "verb mismatch");
    expect(parsed->fields.at("name") == "alpha", "field mismatch");

    const auto formatted = format_control_line(ControlMessage{
        "PING",
        {{"ts", "100"}},
    });
    expect(formatted.find("PING") == 0, "format prefix mismatch");
    expect(formatted.back() == '\n', "format should end with newline");

    InputPacket input;
    input.match_id = 7;
    input.player_id = 9;
    input.sequence = 11;
    input.move_x = 1;
    input.move_y = -1;
    input.aim_x = 320;
    input.aim_y = -120;
    input.fire = 1;
    input.dash = 0;
    const auto input_bytes = encode_input_packet(input);
    const auto decoded_input = decode_input_packet(input_bytes.data(), input_bytes.size());
    expect(decoded_input.has_value(), "input packet decode failed");
    expect(decoded_input->sequence == input.sequence, "input sequence mismatch");
    expect(decoded_input->aim_x == input.aim_x, "input aim_x mismatch");

    SnapshotPacket snapshot;
    snapshot.match_id = 8;
    snapshot.sequence = 13;
    snapshot.server_tick = 17;
    snapshot.entity_count = 2;
    snapshot.projectile_count = 1;
    snapshot.entities.push_back(EntitySnapshot{
        1, 120.0F, 130.0F, 100, 3, 1, 1, 7
    });
    snapshot.entities.push_back(EntitySnapshot{
        2, 220.0F, 330.0F, 75, 1, 4, 0, 9
    });
    const auto snapshot_bytes = encode_snapshot_packet(snapshot);
    const auto decoded_snapshot = decode_snapshot_packet(
        snapshot_bytes.data(), snapshot_bytes.size()
    );
    expect(decoded_snapshot.has_value(), "snapshot decode failed");
    expect(decoded_snapshot->entity_count == 2, "snapshot entity_count mismatch");
    expect(decoded_snapshot->entities[1].player_id == 2, "snapshot player_id mismatch");
    expect(decoded_snapshot->entities[1].alive == 0, "snapshot alive mismatch");

    HeartbeatPacket heartbeat;
    heartbeat.match_id = 15;
    heartbeat.player_id = 3;
    heartbeat.sequence = 99;
    const auto heartbeat_bytes = encode_heartbeat_packet(heartbeat);
    const auto decoded_heartbeat = decode_heartbeat_packet(
        heartbeat_bytes.data(), heartbeat_bytes.size()
    );
    expect(decoded_heartbeat.has_value(), "heartbeat decode failed");
    expect(decoded_heartbeat->sequence == heartbeat.sequence, "heartbeat sequence mismatch");

    std::cout << "test_protocol ok\n";
    return EXIT_SUCCESS;
}
