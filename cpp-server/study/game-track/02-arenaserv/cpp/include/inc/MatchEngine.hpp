#pragma once

#include <cstdint>
#include <deque>
#include <map>
#include <string>
#include <vector>

class MatchEngine
{
public:
    struct Error
    {
        std::string code;
        std::string message;

        Error();
        Error(const std::string &error_code, const std::string &error_message);
        bool empty() const;
    };

    struct Input
    {
        int  seq;
        int  dx;
        int  dy;
        char facing;
        bool fire;

        Input();
        Input(int input_seq, int delta_x, int delta_y, char next_facing, bool fire_flag);
    };

    enum class EventScope
    {
        Single,
        Room
    };

    struct Event
    {
        EventScope   scope;
        std::string  token;
        std::string  line;

        Event();
        Event(EventScope event_scope, const std::string &target_token, const std::string &payload);
    };

    static const int board_width;
    static const int board_height;
    static const int max_players;
    static const int min_players;
    static const int max_hp;
    static const int countdown_steps;
    static const int grace_ticks;
    static const int max_round_ticks;

    MatchEngine();

    bool register_player(const std::string &nick, std::string &token, Error &error);
    bool queue_player(const std::string &token, Error &error);
    bool ready_player(const std::string &token, Error &error);
    bool submit_input(const std::string &token, const Input &input, Error &error);
    bool rejoin_player(const std::string &token, Error &error);
    bool leave_player(const std::string &token, Error &error);
    void disconnect_player(const std::string &token);

    void advance_one_tick();

    std::vector<Event> drain_events();
    std::vector<std::string> room_tokens() const;
    std::string snapshot_json() const;
    std::string phase_name() const;
    std::uint64_t global_tick() const;
    std::uint64_t round_tick() const;

private:
    enum class Phase
    {
        Lobby,
        Countdown,
        InRound,
        Finished
    };

    struct Participant
    {
        std::string token;
        std::string nick;
        bool        connected;
        bool        in_room;
        bool        ready;
        bool        alive;
        int         hp;
        int         x;
        int         y;
        char        facing;
        int         last_seq;
        bool        has_pending_input;
        Input       pending_input;
        int         disconnect_tick;

        Participant();
    };

    struct Projectile
    {
        std::string owner_token;
        int         x;
        int         y;
        int         vx;
        int         vy;

        Projectile();
        Projectile(const std::string &owner, int pos_x, int pos_y, int vel_x, int vel_y);
    };

    bool is_valid_nick(const std::string &nick) const;
    bool all_room_players_ready() const;
    int  alive_count() const;
    void emit_single(const std::string &token, const std::string &line);
    void emit_room(const std::string &line);
    void start_countdown();
    void start_round();
    void process_inputs();
    void move_projectiles();
    void maybe_finish_round();
    void expire_disconnected_players();
    void reset_spawn_state();
    void clear_pending_inputs();
    void remove_from_room(const std::string &token);
    std::string winner_nick() const;
    static std::string phase_to_string(Phase phase);

    std::map<std::string, Participant> participants_;
    std::vector<std::string>           room_order_;
    std::deque<Event>                  events_;
    std::vector<Projectile>            projectiles_;
    Phase                              phase_;
    int                                countdown_remaining_;
    std::uint64_t                      next_token_id_;
    std::uint64_t                      global_tick_;
    std::uint64_t                      round_tick_;
    std::string                        room_id_;
};
