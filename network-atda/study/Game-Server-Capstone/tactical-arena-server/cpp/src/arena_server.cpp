#include "arena/protocol.hpp"
#include "arena/repository.hpp"
#include "arena/state.hpp"

#include <boost/asio.hpp>

#include <array>
#include <chrono>
#include <deque>
#include <functional>
#include <iostream>
#include <memory>
#include <mutex>
#include <optional>
#include <random>
#include <sstream>
#include <thread>
#include <unordered_map>

namespace arena {
namespace {

using tcp = boost::asio::ip::tcp;
using udp = boost::asio::ip::udp;
using error_code = boost::system::error_code;

std::uint64_t steady_now_ms() {
    return static_cast<std::uint64_t>(
        std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::steady_clock::now().time_since_epoch()
        ).count()
    );
}

std::uint64_t unix_now_ms() {
    return static_cast<std::uint64_t>(
        std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::system_clock::now().time_since_epoch()
        ).count()
    );
}

struct LaunchOptions {
    std::uint16_t tcp_port{39001};
    std::uint16_t udp_port{39002};
    std::string bind_host{"127.0.0.1"};
    std::string db_path{"problem/data/arena.sqlite3"};
    int thread_count{4};
    ArenaConfig arena_config{};
};

class ArenaServer;

class TcpSession : public std::enable_shared_from_this<TcpSession> {
public:
    TcpSession(tcp::socket socket, ArenaServer& server);

    void start();
    void deliver(const std::string& line);
    void set_player_id(std::uint32_t player_id);
    std::optional<std::uint32_t> player_id() const;
    tcp::socket& socket();

private:
    void do_read();
    void do_write();
    void on_closed();

    tcp::socket socket_;
    boost::asio::strand<tcp::socket::executor_type> strand_;
    ArenaServer& server_;
    boost::asio::streambuf read_buffer_;
    std::deque<std::string> write_queue_;
    std::optional<std::uint32_t> player_id_;
};

struct PlayerSessionState {
    PersistentProfile profile;
    std::string token;
    std::weak_ptr<TcpSession> session;
    std::optional<std::string> room_id;
    std::optional<std::uint32_t> match_id;
    std::uint64_t disconnected_at_ms{0};
    bool udp_bind_armed{false};
    std::uint32_t udp_bind_nonce{0};
};

struct RoomContext : public std::enable_shared_from_this<RoomContext> {
    RoomContext(
        boost::asio::io_context& io,
        std::string room_id,
        std::string room_name,
        std::size_t max_players
    )
        : room_id(std::move(room_id)),
          room_name(std::move(room_name)),
          max_players(max_players),
          strand(boost::asio::make_strand(io)),
          tick_timer(io) {}

    std::string room_id;
    std::string room_name;
    std::size_t max_players{4};
    std::vector<std::uint32_t> players;
    std::unordered_map<std::uint32_t, bool> ready;
    bool in_match{false};
    std::uint32_t match_id{0};
    std::uint32_t snapshot_sequence{1};
    std::uint64_t started_at_ms{0};
    boost::asio::strand<boost::asio::io_context::executor_type> strand;
    boost::asio::steady_timer tick_timer;
    std::unique_ptr<MatchState> match_state;
    std::unordered_map<std::uint32_t, udp::endpoint> udp_endpoints;
};

class ArenaServer {
public:
    explicit ArenaServer(LaunchOptions options)
        : options_(std::move(options)),
          io_context_(),
          acceptor_(io_context_),
          udp_socket_(io_context_),
          signals_(io_context_, SIGINT, SIGTERM),
          repository_(options_.db_path),
          random_engine_(std::random_device{}()) {}

    void run() {
        repository_.initialize();

        const auto bind_address = boost::asio::ip::make_address(options_.bind_host);
        acceptor_.open(tcp::v4());
        acceptor_.set_option(tcp::acceptor::reuse_address(true));
        acceptor_.bind(tcp::endpoint(bind_address, options_.tcp_port));
        acceptor_.listen();

        udp_socket_.open(udp::v4());
        udp_socket_.bind(udp::endpoint(bind_address, options_.udp_port));

        signals_.async_wait([this](const error_code&, int) {
            io_context_.stop();
        });

        do_accept();
        do_receive_udp();

        std::vector<std::thread> threads;
        const auto count = std::max(1, options_.thread_count);
        threads.reserve(static_cast<std::size_t>(count));
        for (int i = 0; i < count; ++i) {
            threads.emplace_back([this]() { io_context_.run(); });
        }
        for (auto& thread : threads) {
            thread.join();
        }
    }

    void handle_line(const std::shared_ptr<TcpSession>& session, const std::string& line) {
        const auto parsed = parse_control_line(line);
        if (!parsed) {
            send_error(session, "bad_request", "parse_failed");
            return;
        }

        const auto& message = *parsed;
        if (message.verb == "PING") {
            send_message(session, ControlMessage{
                "PONG",
                {{"ts", std::to_string(unix_now_ms())}},
            });
            return;
        }

        if (message.verb == "LOGIN") {
            const auto it = message.fields.find("name");
            if (it == message.fields.end()) {
                send_error(session, "bad_request", "missing_name");
                return;
            }
            handle_login(session, it->second);
            return;
        }

        if (message.verb == "RESUME") {
            const auto it = message.fields.find("token");
            if (it == message.fields.end()) {
                send_error(session, "bad_request", "missing_token");
                return;
            }
            handle_resume(session, it->second);
            return;
        }

        if (!session->player_id().has_value()) {
            send_error(session, "auth_required", "login_first");
            return;
        }

        const auto player_id = *session->player_id();
        if (message.verb == "LIST_ROOMS") {
            handle_list_rooms(session);
        } else if (message.verb == "CREATE_ROOM") {
            handle_create_room(
                session,
                player_id,
                message.fields.count("name") != 0 ? message.fields.at("name") : "arena-room",
                message.fields.count("max") != 0 ? std::stoi(message.fields.at("max")) : 4
            );
        } else if (message.verb == "JOIN_ROOM") {
            const auto it = message.fields.find("room");
            if (it == message.fields.end()) {
                send_error(session, "bad_request", "missing_room");
                return;
            }
            handle_join_room(session, player_id, it->second);
        } else if (message.verb == "LEAVE_ROOM") {
            handle_leave_room(session, player_id);
        } else if (message.verb == "READY") {
            const auto value = message.fields.count("value") != 0 ? message.fields.at("value") : "0";
            handle_ready(session, player_id, value == "1");
        } else if (message.verb == "UDP_BIND") {
            const auto match_it = message.fields.find("match");
            const auto nonce_it = message.fields.find("nonce");
            if (match_it == message.fields.end() || nonce_it == message.fields.end()) {
                send_error(session, "bad_request", "missing_udp_bind_fields");
                return;
            }
            handle_udp_bind(player_id, static_cast<std::uint32_t>(std::stoul(match_it->second)),
                static_cast<std::uint32_t>(std::stoul(nonce_it->second)));
        } else {
            send_error(session, "bad_request", "unknown_verb");
        }
    }

    void handle_disconnect(const std::shared_ptr<TcpSession>& session) {
        if (!session->player_id().has_value()) {
            return;
        }

        std::shared_ptr<RoomContext> room;
        {
            std::scoped_lock lock(state_mutex_);
            auto player_it = players_.find(*session->player_id());
            if (player_it == players_.end()) {
                return;
            }
            player_it->second.session.reset();
            player_it->second.disconnected_at_ms = steady_now_ms();
            if (player_it->second.room_id) {
                auto room_it = rooms_.find(*player_it->second.room_id);
                if (room_it != rooms_.end()) {
                    room = room_it->second;
                }
            }
        }

        if (room && room->in_match && room->match_state) {
            boost::asio::post(room->strand, [room, player_id = *session->player_id()]() {
                if (room->match_state) {
                    room->match_state->mark_disconnected(player_id, steady_now_ms());
                }
            });
        }
    }

private:
    void do_accept() {
        acceptor_.async_accept([this](error_code ec, tcp::socket socket) {
            if (!ec) {
                std::make_shared<TcpSession>(std::move(socket), *this)->start();
            }
            do_accept();
        });
    }

    void do_receive_udp() {
        udp_socket_.async_receive_from(
            boost::asio::buffer(udp_receive_buffer_),
            udp_remote_endpoint_,
            [this](error_code ec, std::size_t bytes_received) {
                if (!ec) {
                    handle_udp_datagram(bytes_received, udp_remote_endpoint_);
                }
                do_receive_udp();
            }
        );
    }

    void handle_udp_datagram(std::size_t bytes_received, const udp::endpoint& endpoint) {
        if (bytes_received < 2) {
            return;
        }

        const auto kind = static_cast<PacketKind>(udp_receive_buffer_[1]);
        if (kind == PacketKind::input) {
            const auto parsed = decode_input_packet(udp_receive_buffer_.data(), bytes_received);
            if (!parsed) {
                return;
            }
            std::shared_ptr<RoomContext> room;
            {
                std::scoped_lock lock(state_mutex_);
                auto match_it = matches_.find(parsed->match_id);
                if (match_it == matches_.end()) {
                    return;
                }
                room = match_it->second;
            }
            boost::asio::post(room->strand, [this, room, endpoint, packet = *parsed]() {
                if (!room->match_state || room->match_id != packet.match_id) {
                    return;
                }
                {
                    std::scoped_lock lock(state_mutex_);
                    auto player_it = players_.find(packet.player_id);
                    if (player_it == players_.end()) {
                        return;
                    }
                    if (!player_it->second.match_id || *player_it->second.match_id != packet.match_id) {
                        return;
                    }
                    if (player_it->second.udp_bind_armed || room->udp_endpoints.count(packet.player_id) != 0) {
                        room->udp_endpoints[packet.player_id] = endpoint;
                        player_it->second.udp_bind_armed = false;
                    }
                }
                room->match_state->submit_input(packet);
            });
        } else if (kind == PacketKind::heartbeat) {
            const auto parsed = decode_heartbeat_packet(udp_receive_buffer_.data(), bytes_received);
            if (!parsed) {
                return;
            }
            std::shared_ptr<RoomContext> room;
            {
                std::scoped_lock lock(state_mutex_);
                auto match_it = matches_.find(parsed->match_id);
                if (match_it == matches_.end()) {
                    return;
                }
                room = match_it->second;
            }
            boost::asio::post(room->strand, [this, room, endpoint, packet = *parsed]() {
                if (!room->match_state || !room->match_state->player_known(packet.player_id)) {
                    return;
                }
                std::scoped_lock lock(state_mutex_);
                room->udp_endpoints[packet.player_id] = endpoint;
                if (auto player_it = players_.find(packet.player_id); player_it != players_.end()) {
                    player_it->second.udp_bind_armed = false;
                }
            });
        }
    }

    void send_error(
        const std::shared_ptr<TcpSession>& session,
        const std::string& code,
        const std::string& message
    ) {
        send_message(session, ControlMessage{
            "ERROR",
            {{"code", code}, {"message", message}},
        });
    }

    void send_message(const std::shared_ptr<TcpSession>& session, const ControlMessage& message) {
        session->deliver(format_control_line(message));
    }

    void send_to_player(std::uint32_t player_id, const ControlMessage& message) {
        std::shared_ptr<TcpSession> session;
        {
            std::scoped_lock lock(state_mutex_);
            auto it = players_.find(player_id);
            if (it == players_.end()) {
                return;
            }
            session = it->second.session.lock();
        }
        if (session) {
            send_message(session, message);
        }
    }

    void handle_login(const std::shared_ptr<TcpSession>& session, const std::string& player_name) {
        const auto profile = repository_.login_or_create(player_name);
        const auto token = make_resume_token(profile.player_id, random_engine_());

        {
            std::scoped_lock lock(state_mutex_);
            auto& state = players_[profile.player_id];
            if (!state.token.empty()) {
                tokens_.erase(state.token);
            }
            state.profile = profile;
            state.token = token;
            state.session = session;
            state.disconnected_at_ms = 0;
            tokens_[token] = profile.player_id;
        }

        session->set_player_id(profile.player_id);
        send_message(session, ControlMessage{
            "LOGIN_OK",
            {
                {"player", std::to_string(profile.player_id)},
                {"token", token},
                {"wins", std::to_string(profile.wins)},
                {"losses", std::to_string(profile.losses)},
                {"kills", std::to_string(profile.kills)},
                {"deaths", std::to_string(profile.deaths)},
            },
        });
    }

    void handle_resume(const std::shared_ptr<TcpSession>& session, const std::string& token) {
        std::shared_ptr<RoomContext> room;
        PersistentProfile profile;
        std::optional<std::uint32_t> match_id;
        {
            std::scoped_lock lock(state_mutex_);
            const auto token_it = tokens_.find(token);
            if (token_it == tokens_.end()) {
                send_error(session, "not_found", "resume_token_missing");
                return;
            }
            auto player_it = players_.find(token_it->second);
            if (player_it == players_.end()) {
                send_error(session, "not_found", "resume_player_missing");
                return;
            }
            const auto now_ms = steady_now_ms();
            if (
                player_it->second.disconnected_at_ms != 0 &&
                (now_ms - player_it->second.disconnected_at_ms) >
                    static_cast<std::uint64_t>(options_.arena_config.resume_window_ms)
            ) {
                send_error(session, "expired", "resume_window_elapsed");
                return;
            }
            player_it->second.session = session;
            player_it->second.disconnected_at_ms = 0;
            player_it->second.udp_bind_armed = false;
            profile = player_it->second.profile;
            match_id = player_it->second.match_id;
            if (player_it->second.room_id) {
                auto room_it = rooms_.find(*player_it->second.room_id);
                if (room_it != rooms_.end()) {
                    room = room_it->second;
                }
            }
        }

        session->set_player_id(profile.player_id);
        send_message(session, ControlMessage{
            "LOGIN_OK",
            {
                {"player", std::to_string(profile.player_id)},
                {"token", token},
                {"wins", std::to_string(profile.wins)},
                {"losses", std::to_string(profile.losses)},
                {"kills", std::to_string(profile.kills)},
                {"deaths", std::to_string(profile.deaths)},
            },
        });

        if (room && room->in_match && room->match_state && match_id) {
            boost::asio::post(room->strand, [this, room, player_id = profile.player_id]() {
                if (!room->match_state) {
                    return;
                }
                room->match_state->mark_reconnected(player_id);
                const auto snapshot = room->match_state->snapshot_for_player(player_id);
                const auto spawn_field = snapshot
                    ? (std::to_string(snapshot->x) + ":" + std::to_string(snapshot->y))
                    : "0:0";
                send_to_player(player_id, ControlMessage{
                    "MATCH_START",
                    {
                        {"match", std::to_string(room->match_id)},
                        {"udp_port", std::to_string(options_.udp_port)},
                        {"tick_hz", std::to_string(options_.arena_config.tick_hz)},
                        {"snapshot_hz", std::to_string(options_.arena_config.snapshot_hz)},
                        {"spawn", spawn_field},
                    },
                });
            });
        } else if (room) {
            broadcast_room_update(room);
        }
    }

    void handle_list_rooms(const std::shared_ptr<TcpSession>& session) {
        std::ostringstream rooms;
        bool first = true;
        {
            std::scoped_lock lock(state_mutex_);
            for (const auto& [room_id, room] : rooms_) {
                if (!first) {
                    rooms << ',';
                }
                first = false;
                rooms
                    << room_id << ':' << room->room_name << ':'
                    << room->players.size() << ':' << room->max_players;
            }
        }
        send_message(session, ControlMessage{
            "ROOM_LIST",
            {{"rooms", rooms.str()}},
        });
    }

    void handle_create_room(
        const std::shared_ptr<TcpSession>& session,
        std::uint32_t player_id,
        const std::string& room_name,
        int max_players
    ) {
        std::shared_ptr<RoomContext> room;
        {
            std::scoped_lock lock(state_mutex_);
            auto& player = players_[player_id];
            if (player.room_id) {
                send_error(session, "conflict", "already_in_room");
                return;
            }
            const auto room_id = "room-" + std::to_string(next_room_id_++);
            room = std::make_shared<RoomContext>(
                io_context_, room_id, slugify(room_name), static_cast<std::size_t>(std::clamp(max_players, 2, 4))
            );
            room->players.push_back(player_id);
            room->ready[player_id] = false;
            rooms_[room_id] = room;
            player.room_id = room_id;
        }
        broadcast_room_update(room);
    }

    void handle_join_room(
        const std::shared_ptr<TcpSession>& session,
        std::uint32_t player_id,
        const std::string& room_id
    ) {
        std::shared_ptr<RoomContext> room;
        {
            std::scoped_lock lock(state_mutex_);
            auto& player = players_[player_id];
            if (player.room_id) {
                send_error(session, "conflict", "already_in_room");
                return;
            }
            auto room_it = rooms_.find(room_id);
            if (room_it == rooms_.end()) {
                send_error(session, "not_found", "room_missing");
                return;
            }
            room = room_it->second;
            if (room->players.size() >= room->max_players || room->in_match) {
                send_error(session, "conflict", "room_unavailable");
                return;
            }
            room->players.push_back(player_id);
            room->ready[player_id] = false;
            player.room_id = room_id;
        }
        broadcast_room_update(room);
    }

    void handle_leave_room(const std::shared_ptr<TcpSession>& session, std::uint32_t player_id) {
        std::shared_ptr<RoomContext> room;
        {
            std::scoped_lock lock(state_mutex_);
            auto& player = players_[player_id];
            if (!player.room_id) {
                send_error(session, "not_found", "room_missing");
                return;
            }
            auto room_it = rooms_.find(*player.room_id);
            if (room_it == rooms_.end()) {
                player.room_id.reset();
                return;
            }
            room = room_it->second;
            if (room->in_match) {
                send_error(session, "conflict", "match_running");
                return;
            }
            room->players.erase(
                std::remove(room->players.begin(), room->players.end(), player_id),
                room->players.end()
            );
            room->ready.erase(player_id);
            player.room_id.reset();
            if (room->players.empty()) {
                rooms_.erase(room->room_id);
                room.reset();
            }
        }
        if (room) {
            broadcast_room_update(room);
        }
    }

    void handle_ready(
        const std::shared_ptr<TcpSession>& session, std::uint32_t player_id, bool ready
    ) {
        std::shared_ptr<RoomContext> room;
        bool changed = false;
        {
            std::scoped_lock lock(state_mutex_);
            auto& player = players_[player_id];
            if (!player.room_id) {
                send_error(session, "not_found", "room_missing");
                return;
            }
            auto room_it = rooms_.find(*player.room_id);
            if (room_it == rooms_.end()) {
                send_error(session, "not_found", "room_missing");
                return;
            }
            room = room_it->second;
            const auto current = room->ready.count(player_id) != 0 && room->ready.at(player_id);
            changed = current != ready;
            room->ready[player_id] = ready;
        }
        if (changed) {
            broadcast_room_update(room);
        }
        try_start_match(room);
    }

    void handle_udp_bind(
        std::uint32_t player_id, std::uint32_t match_id, std::uint32_t nonce
    ) {
        std::scoped_lock lock(state_mutex_);
        auto it = players_.find(player_id);
        if (it == players_.end()) {
            return;
        }
        if (!it->second.match_id || *it->second.match_id != match_id) {
            return;
        }
        it->second.udp_bind_armed = true;
        it->second.udp_bind_nonce = nonce;
    }

    std::string roster_field(
        const std::vector<std::uint32_t>& players,
        const std::unordered_map<std::uint32_t, bool>& ready
    ) const {
        std::ostringstream stream;
        bool first = true;
        for (const auto player_id : players) {
            if (!first) {
                stream << ',';
            }
            first = false;
            const auto is_ready = ready.count(player_id) != 0 && ready.at(player_id);
            stream << player_id << ':' << (is_ready ? 1 : 0);
        }
        return stream.str();
    }

    void broadcast_room_update(const std::shared_ptr<RoomContext>& room) {
        if (!room) {
            return;
        }
        std::vector<std::uint32_t> recipients;
        std::vector<std::uint32_t> players;
        std::unordered_map<std::uint32_t, bool> ready;
        std::string owner;
        {
            std::scoped_lock lock(state_mutex_);
            recipients = room->players;
            players = room->players;
            ready = room->ready;
            owner = players.empty() ? "0" : std::to_string(players.front());
        }
        const auto roster = roster_field(players, ready);
        for (const auto player_id : recipients) {
            send_to_player(player_id, ControlMessage{
                "ROOM_UPDATE",
                {
                    {"room", room->room_id},
                    {"owner", owner},
                    {"roster", roster},
                },
            });
        }
    }

    std::vector<PlayerDefinition> make_spawns(const std::shared_ptr<RoomContext>& room) const {
        std::vector<PlayerDefinition> players;
        const std::array<std::pair<float, float>, 4> spawn_positions{{
            {120.0F, 120.0F},
            {880.0F, 120.0F},
            {120.0F, 880.0F},
            {880.0F, 880.0F},
        }};
        players.reserve(room->players.size());
        for (std::size_t index = 0; index < room->players.size(); ++index) {
            PlayerDefinition definition;
            definition.player_id = room->players[index];
            definition.spawn_x = spawn_positions[index % spawn_positions.size()].first;
            definition.spawn_y = spawn_positions[index % spawn_positions.size()].second;
            definition.name = players_.at(definition.player_id).profile.name;
            players.push_back(definition);
        }
        return players;
    }

    void try_start_match(const std::shared_ptr<RoomContext>& room) {
        std::vector<std::uint32_t> players;
        {
            std::scoped_lock lock(state_mutex_);
            if (!room || room->in_match || room->players.size() < room->max_players) {
                return;
            }
            for (const auto player_id : room->players) {
                if (room->ready.count(player_id) == 0 || !room->ready.at(player_id)) {
                    return;
                }
            }
            room->in_match = true;
            room->match_id = next_match_id_++;
            room->started_at_ms = steady_now_ms();
            room->snapshot_sequence = 1;
            room->udp_endpoints.clear();
            room->match_state = std::make_unique<MatchState>(
                room->room_id,
                room->match_id,
                options_.arena_config,
                make_spawns(room),
                room->started_at_ms
            );
            matches_[room->match_id] = room;
            players = room->players;
            for (const auto player_id : players) {
                auto& state = players_[player_id];
                state.match_id = room->match_id;
                state.udp_bind_armed = false;
                state.udp_bind_nonce = 0;
            }
        }

        for (const auto player_id : players) {
            const auto snapshot = room->match_state->snapshot_for_player(player_id);
            const auto spawn = snapshot
                ? (std::to_string(snapshot->x) + ":" + std::to_string(snapshot->y))
                : "0:0";
            send_to_player(player_id, ControlMessage{
                "MATCH_START",
                {
                    {"match", std::to_string(room->match_id)},
                    {"udp_port", std::to_string(options_.udp_port)},
                    {"tick_hz", std::to_string(options_.arena_config.tick_hz)},
                    {"snapshot_hz", std::to_string(options_.arena_config.snapshot_hz)},
                    {"spawn", spawn},
                },
            });
        }

        schedule_tick(room);
    }

    void schedule_tick(const std::shared_ptr<RoomContext>& room) {
        if (!room || !room->match_state) {
            return;
        }
        room->tick_timer.expires_after(
            std::chrono::milliseconds(1000 / std::max(1, options_.arena_config.tick_hz))
        );
        room->tick_timer.async_wait(
            boost::asio::bind_executor(room->strand, [this, room](error_code ec) {
                if (ec || !room->match_state) {
                    return;
                }

                const auto now_ms = steady_now_ms();
                if (const auto result = room->match_state->step(now_ms); result.has_value()) {
                    finish_match(room, *result, now_ms);
                    return;
                }

                const auto snapshot_interval =
                    std::max(1, options_.arena_config.tick_hz / std::max(1, options_.arena_config.snapshot_hz));
                if ((room->snapshot_sequence % static_cast<std::uint32_t>(snapshot_interval)) == 0) {
                    auto packet = room->match_state->build_snapshot_packet(room->snapshot_sequence);
                    const auto bytes = encode_snapshot_packet(packet);
                    for (const auto& [player_id, endpoint] : room->udp_endpoints) {
                        error_code send_ec;
                        udp_socket_.send_to(boost::asio::buffer(bytes), endpoint, 0, send_ec);
                        (void)player_id;
                    }
                }
                room->snapshot_sequence += 1;
                schedule_tick(room);
            })
        );
    }

    void finish_match(
        const std::shared_ptr<RoomContext>& room,
        const MatchResult& result,
        std::uint64_t ended_at_ms
    ) {
        if (!room || !room->match_state) {
            return;
        }
        const auto snapshot = room->match_state->build_snapshot_packet(0);
        {
            std::scoped_lock repo_lock(repository_mutex_);
            repository_.record_match(
                room->started_at_ms,
                ended_at_ms,
                result.winner_player_id,
                snapshot.entities,
                result.result_blob
            );
        }

        for (const auto player_id : room->players) {
            send_to_player(player_id, ControlMessage{
                "MATCH_RESULT",
                {
                    {"winner", std::to_string(result.winner_player_id)},
                    {"scoreboard", result.scoreboard_blob},
                },
            });
        }

        std::scoped_lock lock(state_mutex_);
        matches_.erase(room->match_id);
        for (const auto player_id : room->players) {
            auto& player = players_[player_id];
            player.match_id.reset();
            player.room_id.reset();
            player.udp_bind_armed = false;
        }
        rooms_.erase(room->room_id);
    }

    LaunchOptions options_;
    boost::asio::io_context io_context_;
    tcp::acceptor acceptor_;
    udp::socket udp_socket_;
    boost::asio::signal_set signals_;
    std::array<std::uint8_t, 2048> udp_receive_buffer_{};
    udp::endpoint udp_remote_endpoint_;
    SqliteRepository repository_;
    std::mutex repository_mutex_;
    std::mutex state_mutex_;
    std::unordered_map<std::uint32_t, PlayerSessionState> players_;
    std::unordered_map<std::string, std::uint32_t> tokens_;
    std::unordered_map<std::string, std::shared_ptr<RoomContext>> rooms_;
    std::unordered_map<std::uint32_t, std::shared_ptr<RoomContext>> matches_;
    std::uint32_t next_room_id_{1};
    std::uint32_t next_match_id_{1};
    std::mt19937_64 random_engine_;
};

TcpSession::TcpSession(tcp::socket socket, ArenaServer& server)
    : socket_(std::move(socket)),
      strand_(boost::asio::make_strand(socket_.get_executor())),
      server_(server) {}

void TcpSession::start() {
    do_read();
}

void TcpSession::deliver(const std::string& line) {
    const auto self = shared_from_this();
    boost::asio::post(strand_, [this, self, line]() {
        const auto writing = !write_queue_.empty();
        write_queue_.push_back(line);
        if (!writing) {
            do_write();
        }
    });
}

void TcpSession::set_player_id(std::uint32_t player_id) {
    player_id_ = player_id;
}

std::optional<std::uint32_t> TcpSession::player_id() const {
    return player_id_;
}

tcp::socket& TcpSession::socket() {
    return socket_;
}

void TcpSession::do_read() {
    const auto self = shared_from_this();
    boost::asio::async_read_until(
        socket_,
        read_buffer_,
        '\n',
        boost::asio::bind_executor(strand_, [this, self](error_code ec, std::size_t /*bytes_transferred*/) {
            if (ec) {
                on_closed();
                return;
            }
            std::istream stream(&read_buffer_);
            std::string line;
            std::getline(stream, line);
            server_.handle_line(self, line);
            do_read();
        })
    );
}

void TcpSession::do_write() {
    const auto self = shared_from_this();
    boost::asio::async_write(
        socket_,
        boost::asio::buffer(write_queue_.front()),
        boost::asio::bind_executor(strand_, [this, self](error_code ec, std::size_t /*bytes_transferred*/) {
            if (ec) {
                on_closed();
                return;
            }
            write_queue_.pop_front();
            if (!write_queue_.empty()) {
                do_write();
            }
        })
    );
}

void TcpSession::on_closed() {
    error_code ignored;
    socket_.close(ignored);
    server_.handle_disconnect(shared_from_this());
}

LaunchOptions parse_args(int argc, char** argv) {
    LaunchOptions options;
    for (int i = 1; i < argc; ++i) {
        const std::string arg = argv[i];
        auto require_value = [&](const char* name) -> std::string {
            if ((i + 1) >= argc) {
                throw std::runtime_error(std::string("missing value for ") + name);
            }
            return argv[++i];
        };
        if (arg == "--tcp-port") {
            options.tcp_port = static_cast<std::uint16_t>(std::stoi(require_value("--tcp-port")));
        } else if (arg == "--udp-port") {
            options.udp_port = static_cast<std::uint16_t>(std::stoi(require_value("--udp-port")));
        } else if (arg == "--db-path") {
            options.db_path = require_value("--db-path");
        } else if (arg == "--thread-count") {
            options.thread_count = std::stoi(require_value("--thread-count"));
        } else if (arg == "--match-duration-ms") {
            options.arena_config.match_duration_ms = std::stoi(require_value("--match-duration-ms"));
        } else if (arg == "--resume-window-ms") {
            options.arena_config.resume_window_ms = std::stoi(require_value("--resume-window-ms"));
        } else if (arg == "--tick-hz") {
            options.arena_config.tick_hz = std::stoi(require_value("--tick-hz"));
        } else if (arg == "--snapshot-hz") {
            options.arena_config.snapshot_hz = std::stoi(require_value("--snapshot-hz"));
        } else if (arg == "--bind-host") {
            options.bind_host = require_value("--bind-host");
        } else if (arg == "--help") {
            std::cout
                << "arena_server --tcp-port <port> --udp-port <port> --db-path <file> "
                << "--match-duration-ms <ms> --resume-window-ms <ms>\n";
            std::exit(0);
        }
    }
    return options;
}

}  // namespace
}  // namespace arena

int main(int argc, char** argv) {
    try {
        auto options = arena::parse_args(argc, argv);
        arena::ArenaServer server(std::move(options));
        server.run();
    } catch (const std::exception& ex) {
        std::cerr << "[arena_server] " << ex.what() << '\n';
        return 1;
    }
    return 0;
}
