#include "arena/protocol.hpp"

#include <boost/asio.hpp>

#include <atomic>
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <optional>
#include <random>
#include <sstream>
#include <string>
#include <thread>

namespace {

using tcp = boost::asio::ip::tcp;
using udp = boost::asio::ip::udp;
using namespace std::chrono_literals;

struct BotOptions {
    std::string host{"127.0.0.1"};
    std::uint16_t tcp_port{39001};
    std::string name{"bot"};
    std::string mode{"scripted"};
    std::string role{"join"};
    std::string room_name{"arena-room"};
    std::string room_id;
    int max_players{2};
};

std::string read_line(tcp::socket& socket, boost::asio::streambuf& buffer) {
    boost::asio::read_until(socket, buffer, '\n');
    std::istream stream(&buffer);
    std::string line;
    std::getline(stream, line);
    return line;
}

void send_line(tcp::socket& socket, const arena::ControlMessage& message) {
    const auto line = arena::format_control_line(message);
    boost::asio::write(socket, boost::asio::buffer(line));
}

BotOptions parse_args(int argc, char** argv) {
    BotOptions options;
    for (int i = 1; i < argc; ++i) {
        const std::string arg = argv[i];
        auto require_value = [&](const char* name) {
            if ((i + 1) >= argc) {
                throw std::runtime_error(std::string("missing value for ") + name);
            }
            return std::string(argv[++i]);
        };
        if (arg == "--host") {
            options.host = require_value("--host");
        } else if (arg == "--tcp-port") {
            options.tcp_port = static_cast<std::uint16_t>(std::stoi(require_value("--tcp-port")));
        } else if (arg == "--name") {
            options.name = require_value("--name");
        } else if (arg == "--mode") {
            options.mode = require_value("--mode");
        } else if (arg == "--role") {
            options.role = require_value("--role");
        } else if (arg == "--room-name") {
            options.room_name = require_value("--room-name");
        } else if (arg == "--room-id") {
            options.room_id = require_value("--room-id");
        } else if (arg == "--max-players") {
            options.max_players = std::stoi(require_value("--max-players"));
        }
    }
    return options;
}

bool trace_enabled() {
    const char* value = std::getenv("ARENA_BOT_TRACE");
    return value != nullptr && std::string(value) == "1";
}

void trace(const std::string& message) {
    if (trace_enabled()) {
        std::cerr << "[arena_bot] " << message << '\n';
    }
}

std::string find_room_id(
    const std::string& rooms_field,
    const std::string& desired_room_name
) {
    if (rooms_field.empty()) {
        return {};
    }
    std::string first_room_id;
    std::size_t room_count = 0;
    std::size_t offset = 0;
    while (offset < rooms_field.size()) {
        room_count += 1;
        const auto comma = rooms_field.find(',', offset);
        const auto entry = rooms_field.substr(
            offset,
            comma == std::string::npos ? std::string::npos : (comma - offset)
        );
        const auto first_colon = entry.find(':');
        if (first_colon == std::string::npos) {
            break;
        }
        const auto second_colon = entry.find(':', first_colon + 1);
        if (second_colon == std::string::npos) {
            break;
        }

        const auto room_id = entry.substr(0, first_colon);
        const auto room_name = entry.substr(first_colon + 1, second_colon - first_colon - 1);
        if (first_room_id.empty()) {
            first_room_id = room_id;
        }
        if (!desired_room_name.empty() && room_name == desired_room_name) {
            return room_id;
        }

        if (comma == std::string::npos) {
            break;
        }
        offset = comma + 1;
    }
    if (desired_room_name.empty()) {
        return first_room_id;
    }
    return room_count == 1 ? first_room_id : std::string{};
}

int run_scripted(const BotOptions& options) {
    boost::asio::io_context io;
    tcp::resolver resolver(io);
    tcp::socket tcp_socket(io);
    boost::asio::connect(
        tcp_socket, resolver.resolve(options.host, std::to_string(options.tcp_port))
    );
    boost::asio::streambuf buffer;

    send_line(tcp_socket, arena::ControlMessage{
        "LOGIN",
        {{"name", options.name}},
    });
    trace(options.name + " -> LOGIN");
    auto login = arena::parse_control_line(read_line(tcp_socket, buffer));
    if (!login || login->verb != "LOGIN_OK") {
        throw std::runtime_error("LOGIN failed");
    }
    trace(options.name + " <- LOGIN_OK");
    const auto player_id = static_cast<std::uint32_t>(std::stoul(login->fields.at("player")));
    const auto token = login->fields.at("token");

    if (options.role == "host") {
        send_line(tcp_socket, arena::ControlMessage{
            "CREATE_ROOM",
            {
                {"name", options.room_name},
                {"max", std::to_string(options.max_players)},
            },
        });
        trace(options.name + " -> CREATE_ROOM");
    } else {
        while (true) {
            send_line(tcp_socket, arena::ControlMessage{"LIST_ROOMS", {}});
            trace(options.name + " -> LIST_ROOMS");
            auto list = arena::parse_control_line(read_line(tcp_socket, buffer));
            if (list && list->verb == "ROOM_LIST") {
                trace(options.name + " <- ROOM_LIST");
                const auto rooms = list->fields.count("rooms") ? list->fields.at("rooms") : "";
                const auto room_id = options.room_id.empty()
                    ? find_room_id(rooms, options.room_name)
                    : options.room_id;
                if (!room_id.empty()) {
                    send_line(tcp_socket, arena::ControlMessage{
                        "JOIN_ROOM",
                        {{"room", room_id}},
                    });
                    trace(options.name + " -> JOIN_ROOM room=" + room_id);
                    break;
                }
            }
            std::this_thread::sleep_for(100ms);
        }
    }

    std::optional<std::uint32_t> match_id;
    std::optional<std::uint16_t> udp_port;
    std::atomic<bool> match_done{false};
    std::string match_result_line;
    bool ready_sent = false;

    while (!match_id.has_value()) {
        const auto message = arena::parse_control_line(read_line(tcp_socket, buffer));
        if (!message) {
            continue;
        }
        trace(options.name + " <- " + message->verb);
        if (message->verb == "ROOM_UPDATE" && !ready_sent) {
            send_line(tcp_socket, arena::ControlMessage{
                "READY",
                {{"value", "1"}},
            });
            trace(options.name + " -> READY");
            ready_sent = true;
        } else if (message->verb == "MATCH_START") {
            match_id = static_cast<std::uint32_t>(std::stoul(message->fields.at("match")));
            udp_port = static_cast<std::uint16_t>(std::stoi(message->fields.at("udp_port")));
            trace(options.name + " matched on " + std::to_string(*match_id));
        }
    }

    const auto nonce = static_cast<std::uint32_t>(std::hash<std::string>{}(token) & 0xFFFFFFFFU);
    send_line(tcp_socket, arena::ControlMessage{
        "UDP_BIND",
        {
            {"match", std::to_string(*match_id)},
            {"nonce", std::to_string(nonce)},
        },
    });
    trace(options.name + " -> UDP_BIND");

    udp::socket udp_socket(io, udp::v4());
    udp_socket.connect(
        udp::endpoint(boost::asio::ip::make_address(options.host), *udp_port)
    );

    std::thread udp_thread([&]() {
        std::mt19937 rng(static_cast<std::uint32_t>(player_id * 17U + 11U));
        std::uniform_int_distribution<int> move_dist(-1, 1);
        std::uniform_int_distribution<int> fire_dist(0, 4);
        std::uint32_t sequence = 1;
        while (!match_done.load()) {
            arena::InputPacket packet;
            packet.match_id = *match_id;
            packet.player_id = player_id;
            packet.sequence = sequence++;
            packet.move_x = static_cast<std::int8_t>(move_dist(rng));
            packet.move_y = static_cast<std::int8_t>(move_dist(rng));
            packet.aim_x = static_cast<std::int16_t>(300 + move_dist(rng) * 50);
            packet.aim_y = static_cast<std::int16_t>(200 + move_dist(rng) * 50);
            packet.fire = static_cast<std::uint8_t>(fire_dist(rng) == 0 ? 1 : 0);
            packet.dash = static_cast<std::uint8_t>(fire_dist(rng) == 1 ? 1 : 0);
            const auto bytes = arena::encode_input_packet(packet);
            udp_socket.send(boost::asio::buffer(bytes));
            std::this_thread::sleep_for(50ms);
        }
    });

    while (!match_done.load()) {
        const auto message = arena::parse_control_line(read_line(tcp_socket, buffer));
        if (!message) {
            continue;
        }
        trace(options.name + " <- " + message->verb);
        if (message->verb == "MATCH_RESULT") {
            match_result_line = arena::format_control_line(*message);
            match_done.store(true);
            break;
        }
    }

    if (udp_thread.joinable()) {
        udp_thread.join();
    }

    std::cout << options.name << ' ' << match_result_line;
    return 0;
}

int run_interactive(const BotOptions& options) {
    boost::asio::io_context io;
    tcp::resolver resolver(io);
    tcp::socket tcp_socket(io);
    boost::asio::connect(
        tcp_socket, resolver.resolve(options.host, std::to_string(options.tcp_port))
    );
    boost::asio::streambuf buffer;

    send_line(tcp_socket, arena::ControlMessage{
        "LOGIN",
        {{"name", options.name}},
    });
    std::cout << read_line(tcp_socket, buffer) << '\n';
    std::cout << "commands: list | create <name> <max> | join <room> | ready <0|1> | quit\n";

    std::thread reader([&]() {
        try {
            while (true) {
                std::cout << read_line(tcp_socket, buffer) << '\n';
            }
        } catch (...) {
        }
    });

    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream stream(line);
        std::string verb;
        stream >> verb;
        if (verb == "quit") {
            break;
        }
        if (verb == "list") {
            send_line(tcp_socket, arena::ControlMessage{"LIST_ROOMS", {}});
        } else if (verb == "create") {
            std::string name;
            int max_players = 2;
            stream >> name >> max_players;
            send_line(tcp_socket, arena::ControlMessage{
                "CREATE_ROOM",
                {{"name", name}, {"max", std::to_string(max_players)}},
            });
        } else if (verb == "join") {
            std::string room;
            stream >> room;
            send_line(tcp_socket, arena::ControlMessage{"JOIN_ROOM", {{"room", room}}});
        } else if (verb == "ready") {
            std::string value{"1"};
            stream >> value;
            send_line(tcp_socket, arena::ControlMessage{"READY", {{"value", value}}});
        } else {
            std::cout << "unknown command\n";
        }
    }
    if (reader.joinable()) {
        reader.detach();
    }
    return 0;
}

}  // namespace

int main(int argc, char** argv) {
    try {
        const auto options = parse_args(argc, argv);
        if (options.mode == "interactive") {
            return run_interactive(options);
        }
        return run_scripted(options);
    } catch (const std::exception& ex) {
        std::cerr << "[arena_bot] " << ex.what() << '\n';
        return 1;
    }
}
