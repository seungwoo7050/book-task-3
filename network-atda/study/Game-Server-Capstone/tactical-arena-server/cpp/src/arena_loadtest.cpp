#include "arena/protocol.hpp"

#include <boost/asio.hpp>

#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <exception>
#include <iostream>
#include <mutex>
#include <optional>
#include <random>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

namespace {

using tcp = boost::asio::ip::tcp;
using udp = boost::asio::ip::udp;
using namespace std::chrono_literals;

struct Options {
    std::string host{"127.0.0.1"};
    std::uint16_t tcp_port{39001};
    int room_count{2};
    int bots_per_room{4};
};

struct BotSpec {
    std::string name;
    std::string room_name;
    std::string role;
    int max_players{4};
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

Options parse_args(int argc, char** argv) {
    Options options;
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
        } else if (arg == "--room-count") {
            options.room_count = std::stoi(require_value("--room-count"));
        } else if (arg == "--bots-per-room") {
            options.bots_per_room = std::stoi(require_value("--bots-per-room"));
        }
    }
    return options;
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
        if (room_name == desired_room_name) {
            return room_id;
        }
        if (comma == std::string::npos) {
            break;
        }
        offset = comma + 1;
    }
    return room_count == 1 ? first_room_id : std::string{};
}

void run_bot_worker(const Options& options, const BotSpec& spec) {
    boost::asio::io_context io;
    tcp::resolver resolver(io);
    tcp::socket tcp_socket(io);
    boost::asio::connect(
        tcp_socket, resolver.resolve(options.host, std::to_string(options.tcp_port))
    );
    boost::asio::streambuf buffer;

    send_line(tcp_socket, arena::ControlMessage{
        "LOGIN",
        {{"name", spec.name}},
    });
    auto login = arena::parse_control_line(read_line(tcp_socket, buffer));
    if (!login || login->verb != "LOGIN_OK") {
        throw std::runtime_error("LOGIN failed for " + spec.name);
    }
    const auto player_id = static_cast<std::uint32_t>(std::stoul(login->fields.at("player")));
    const auto token = login->fields.at("token");

    if (spec.role == "host") {
        send_line(tcp_socket, arena::ControlMessage{
            "CREATE_ROOM",
            {
                {"name", spec.room_name},
                {"max", std::to_string(spec.max_players)},
            },
        });
    } else {
        while (true) {
            send_line(tcp_socket, arena::ControlMessage{"LIST_ROOMS", {}});
            const auto list = arena::parse_control_line(read_line(tcp_socket, buffer));
            if (!list || list->verb != "ROOM_LIST") {
                continue;
            }
            const auto rooms = list->fields.count("rooms") != 0 ? list->fields.at("rooms") : "";
            const auto room_id = find_room_id(rooms, spec.room_name);
            if (room_id.empty()) {
                std::this_thread::sleep_for(75ms);
                continue;
            }
            send_line(tcp_socket, arena::ControlMessage{
                "JOIN_ROOM",
                {{"room", room_id}},
            });
            break;
        }
    }

    bool ready_sent = false;
    std::optional<std::uint32_t> match_id;
    std::optional<std::uint16_t> udp_port;
    std::atomic<bool> match_done{false};

    while (!match_id.has_value()) {
        const auto message = arena::parse_control_line(read_line(tcp_socket, buffer));
        if (!message) {
            continue;
        }
        if (message->verb == "ROOM_UPDATE" && !ready_sent) {
            send_line(tcp_socket, arena::ControlMessage{
                "READY",
                {{"value", "1"}},
            });
            ready_sent = true;
        } else if (message->verb == "MATCH_START") {
            match_id = static_cast<std::uint32_t>(std::stoul(message->fields.at("match")));
            udp_port = static_cast<std::uint16_t>(std::stoi(message->fields.at("udp_port")));
        } else if (message->verb == "ERROR") {
            throw std::runtime_error(
                "control error for " + spec.name + ": " + arena::format_control_line(*message)
            );
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

    udp::socket udp_socket(io, udp::v4());
    udp_socket.connect(
        udp::endpoint(boost::asio::ip::make_address(options.host), *udp_port)
    );

    std::thread udp_thread([&]() {
        std::mt19937 rng(static_cast<std::uint32_t>(player_id * 97U + spec.name.size()));
        std::uniform_int_distribution<int> move_dist(-1, 1);
        std::uniform_int_distribution<int> fire_dist(0, 5);
        std::uint32_t sequence = 1;
        while (!match_done.load()) {
            arena::InputPacket packet;
            packet.match_id = *match_id;
            packet.player_id = player_id;
            packet.sequence = sequence++;
            packet.move_x = static_cast<std::int8_t>(move_dist(rng));
            packet.move_y = static_cast<std::int8_t>(move_dist(rng));
            packet.aim_x = static_cast<std::int16_t>(200 + move_dist(rng) * 150);
            packet.aim_y = static_cast<std::int16_t>(200 + move_dist(rng) * 150);
            packet.fire = static_cast<std::uint8_t>(fire_dist(rng) == 0 ? 1 : 0);
            packet.dash = static_cast<std::uint8_t>(fire_dist(rng) == 1 ? 1 : 0);
            const auto bytes = arena::encode_input_packet(packet);
            boost::system::error_code ec;
            udp_socket.send(boost::asio::buffer(bytes), 0, ec);
            if (ec) {
                break;
            }
            std::this_thread::sleep_for(50ms);
        }
    });

    while (!match_done.load()) {
        const auto message = arena::parse_control_line(read_line(tcp_socket, buffer));
        if (!message) {
            continue;
        }
        if (message->verb == "MATCH_RESULT") {
            match_done.store(true);
            break;
        }
        if (message->verb == "ERROR") {
            throw std::runtime_error(
                "match error for " + spec.name + ": " + arena::format_control_line(*message)
            );
        }
    }

    if (udp_thread.joinable()) {
        udp_thread.join();
    }
}

}  // namespace

int main(int argc, char** argv) {
    try {
        const auto options = parse_args(argc, argv);
        std::vector<std::thread> workers;
        std::atomic<int> failures{0};
        std::mutex error_mutex;
        std::vector<std::string> errors;

        for (int room = 0; room < options.room_count; ++room) {
            const auto room_name = "load-room-" + std::to_string(room + 1);
            for (int bot = 0; bot < options.bots_per_room; ++bot) {
                BotSpec spec;
                spec.name =
                    "load-bot-" + std::to_string(room + 1) + "-" + std::to_string(bot + 1);
                spec.room_name = room_name;
                spec.role = bot == 0 ? "host" : "join";
                spec.max_players = options.bots_per_room;
                workers.emplace_back([&, spec]() {
                    try {
                        run_bot_worker(options, spec);
                    } catch (const std::exception& ex) {
                        failures.fetch_add(1);
                        std::scoped_lock lock(error_mutex);
                        errors.push_back(spec.name + ": " + ex.what());
                    }
                });
                std::this_thread::sleep_for(75ms);
            }
        }

        for (auto& worker : workers) {
            if (worker.joinable()) {
                worker.join();
            }
        }

        if (failures.load() != 0) {
            for (const auto& error : errors) {
                std::cerr << "[arena_loadtest] " << error << '\n';
            }
            return 1;
        }

        std::cout
            << "loadtest rooms=" << options.room_count
            << " bots_per_room=" << options.bots_per_room
            << " mode=in-process"
            << " status=ok\n";
        return 0;
    } catch (const std::exception& ex) {
        std::cerr << "[arena_loadtest] " << ex.what() << '\n';
        return 1;
    }
}
