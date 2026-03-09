#include "inc/MatchEngine.hpp"

#include <algorithm>
#include <cstdlib>
#include <cctype>
#include <sstream>
#include <stdexcept>

const int MatchEngine::board_width = 20;
const int MatchEngine::board_height = 20;
const int MatchEngine::max_players = 4;
const int MatchEngine::min_players = 2;
const int MatchEngine::max_hp = 3;
const int MatchEngine::countdown_steps = 3;
const int MatchEngine::grace_ticks = 100;
const int MatchEngine::max_round_ticks = 30;

MatchEngine::Error::Error()
    : code(), message()
{
}

MatchEngine::Error::Error(const std::string &error_code, const std::string &error_message)
    : code(error_code), message(error_message)
{
}

bool MatchEngine::Error::empty() const
{
    return this->code.empty();
}

MatchEngine::Input::Input()
    : seq(0), dx(0), dy(0), facing('N'), fire(false)
{
}

MatchEngine::Input::Input(int input_seq, int delta_x, int delta_y, char next_facing, bool fire_flag)
    : seq(input_seq), dx(delta_x), dy(delta_y), facing(next_facing), fire(fire_flag)
{
}

MatchEngine::Event::Event()
    : scope(EventScope::Room), token(), line()
{
}

MatchEngine::Event::Event(EventScope event_scope, const std::string &target_token, const std::string &payload)
    : scope(event_scope), token(target_token), line(payload)
{
}

MatchEngine::Participant::Participant()
    : token(),
      nick(),
      connected(false),
      in_room(false),
      ready(false),
      alive(false),
      hp(MatchEngine::max_hp),
      x(0),
      y(0),
      facing('N'),
      last_seq(0),
      has_pending_input(false),
      pending_input(),
      disconnect_tick(-1)
{
}

MatchEngine::Projectile::Projectile()
    : owner_token(), x(0), y(0), vx(0), vy(0)
{
}

MatchEngine::Projectile::Projectile(const std::string &owner, int pos_x, int pos_y, int vel_x, int vel_y)
    : owner_token(owner), x(pos_x), y(pos_y), vx(vel_x), vy(vel_y)
{
}

namespace
{
    std::pair<int, int> direction_delta(char facing)
    {
        switch (facing)
        {
        case 'N':
            return std::make_pair(0, -1);
        case 'E':
            return std::make_pair(1, 0);
        case 'S':
            return std::make_pair(0, 1);
        case 'W':
            return std::make_pair(-1, 0);
        default:
            return std::make_pair(0, 0);
        }
    }

    bool is_facing_token(char token)
    {
        return token == 'N' || token == 'E' || token == 'S' || token == 'W';
    }

    std::string bool_to_json(bool value)
    {
        return value ? "true" : "false";
    }
}

MatchEngine::MatchEngine()
    : participants_(),
      room_order_(),
      events_(),
      projectiles_(),
      phase_(Phase::Lobby),
      countdown_remaining_(0),
      next_token_id_(1),
      global_tick_(0),
      round_tick_(0),
      room_id_("arena-1")
{
}

bool MatchEngine::register_player(const std::string &nick, std::string &token, Error &error)
{
    error = Error();
    if (!this->is_valid_nick(nick))
    {
        error = Error("invalid_nick", "nickname must start with a letter and use [A-Za-z0-9_]{1,16}");
        return false;
    }

    for (std::map<std::string, Participant>::const_iterator it = this->participants_.begin();
         it != this->participants_.end();
         ++it)
    {
        if (it->second.nick == nick)
        {
            error = Error("duplicate_nick", "nickname already registered");
            return false;
        }
    }

    std::ostringstream oss;
    oss << "token-" << this->next_token_id_++;
    token = oss.str();

    Participant participant;
    participant.token = token;
    participant.nick = nick;
    participant.connected = true;
    this->participants_.insert(std::make_pair(token, participant));
    this->emit_single(token, "WELCOME " + token);
    return true;
}

bool MatchEngine::queue_player(const std::string &token, Error &error)
{
    error = Error();
    std::map<std::string, Participant>::iterator it = this->participants_.find(token);
    if (it == this->participants_.end())
    {
        error = Error("unknown_session", "HELLO must complete before QUEUE");
        return false;
    }
    if (this->phase_ == Phase::Countdown || this->phase_ == Phase::InRound)
    {
        error = Error("room_full", "match already locked; wait for a new server run");
        return false;
    }
    if (this->phase_ == Phase::Finished)
    {
        error = Error("bad_state", "round already finished");
        return false;
    }
    if (it->second.in_room)
    {
        error = Error("bad_state", "already queued");
        return false;
    }
    if (static_cast<int>(this->room_order_.size()) >= max_players)
    {
        error = Error("room_full", "room already has four players");
        return false;
    }

    it->second.in_room = true;
    it->second.ready = false;
    it->second.alive = true;
    it->second.hp = max_hp;
    it->second.last_seq = 0;
    it->second.disconnect_tick = -1;
    this->room_order_.push_back(token);
    this->emit_room("ROOM " + this->room_id_ + " lobby");
    return true;
}

bool MatchEngine::ready_player(const std::string &token, Error &error)
{
    error = Error();
    std::map<std::string, Participant>::iterator it = this->participants_.find(token);
    if (it == this->participants_.end() || !it->second.in_room)
    {
        error = Error("bad_state", "player is not in the room");
        return false;
    }
    if (this->phase_ != Phase::Lobby)
    {
        error = Error("bad_state", "READY is only allowed in lobby");
        return false;
    }

    it->second.ready = true;
    if (static_cast<int>(this->room_order_.size()) >= min_players && this->all_room_players_ready())
        this->start_countdown();
    return true;
}

bool MatchEngine::submit_input(const std::string &token, const Input &input, Error &error)
{
    error = Error();
    std::map<std::string, Participant>::iterator it = this->participants_.find(token);
    if (it == this->participants_.end() || !it->second.in_room)
    {
        error = Error("bad_state", "player is not in the room");
        return false;
    }
    Participant &participant = it->second;
    if (this->phase_ != Phase::InRound)
    {
        error = Error("bad_state", "match is not in progress");
        return false;
    }
    if (!participant.alive)
    {
        error = Error("bad_state", "eliminated players cannot act");
        return false;
    }
    if (input.seq <= participant.last_seq)
    {
        error = Error("stale_sequence", "input sequence must increase monotonically");
        return false;
    }
    if ((input.dx < -1 || input.dx > 1) || (input.dy < -1 || input.dy > 1) || (std::abs(input.dx) + std::abs(input.dy) > 1))
    {
        error = Error("invalid_input", "movement must be at most one orthogonal tile");
        return false;
    }
    if (!is_facing_token(input.facing))
    {
        error = Error("invalid_input", "facing must be one of N/E/S/W");
        return false;
    }

    participant.pending_input = input;
    participant.has_pending_input = true;
    participant.last_seq = input.seq;
    return true;
}

bool MatchEngine::rejoin_player(const std::string &token, Error &error)
{
    error = Error();
    std::map<std::string, Participant>::iterator it = this->participants_.find(token);
    if (it == this->participants_.end())
    {
        error = Error("expired_session", "session token is unknown");
        return false;
    }
    Participant &participant = it->second;
    if (participant.connected)
    {
        error = Error("bad_state", "session is already connected");
        return false;
    }
    if (participant.disconnect_tick < 0 || static_cast<int>(this->global_tick_) - participant.disconnect_tick > grace_ticks)
    {
        error = Error("expired_session", "reconnect grace expired");
        return false;
    }

    participant.connected = true;
    participant.disconnect_tick = -1;
    this->emit_single(token, "WELCOME " + token);
    if (participant.in_room)
    {
        this->emit_single(token, "ROOM " + this->room_id_ + " " + this->phase_name());
        if (this->phase_ == Phase::Countdown)
        {
            std::ostringstream oss;
            oss << "COUNTDOWN " << this->countdown_remaining_;
            this->emit_single(token, oss.str());
        }
        if (this->phase_ == Phase::InRound || this->phase_ == Phase::Finished)
        {
            std::ostringstream oss;
            oss << "SNAPSHOT " << this->round_tick_ << " " << this->snapshot_json();
            this->emit_single(token, oss.str());
        }
    }
    return true;
}

bool MatchEngine::leave_player(const std::string &token, Error &error)
{
    error = Error();
    std::map<std::string, Participant>::iterator it = this->participants_.find(token);
    if (it == this->participants_.end())
    {
        error = Error("unknown_session", "session token is unknown");
        return false;
    }

    this->remove_from_room(token);
    this->participants_.erase(it);
    return true;
}

void MatchEngine::disconnect_player(const std::string &token)
{
    std::map<std::string, Participant>::iterator it = this->participants_.find(token);
    if (it == this->participants_.end())
        return;

    it->second.connected = false;
    it->second.disconnect_tick = static_cast<int>(this->global_tick_);
}

void MatchEngine::advance_one_tick()
{
    ++this->global_tick_;
    this->expire_disconnected_players();

    if (this->phase_ == Phase::Countdown)
    {
        if (this->countdown_remaining_ > 1)
        {
            --this->countdown_remaining_;
            std::ostringstream oss;
            oss << "COUNTDOWN " << this->countdown_remaining_;
            this->emit_room(oss.str());
        }
        else
        {
            this->start_round();
        }
        return;
    }

    if (this->phase_ != Phase::InRound)
        return;

    ++this->round_tick_;
    this->process_inputs();
    this->move_projectiles();

    {
        std::ostringstream oss;
        oss << "SNAPSHOT " << this->round_tick_ << " " << this->snapshot_json();
        this->emit_room(oss.str());
    }

    this->maybe_finish_round();
}

std::vector<MatchEngine::Event> MatchEngine::drain_events()
{
    std::vector<Event> drained(this->events_.begin(), this->events_.end());
    this->events_.clear();
    return drained;
}

std::vector<std::string> MatchEngine::room_tokens() const
{
    return this->room_order_;
}

std::string MatchEngine::snapshot_json() const
{
    std::ostringstream oss;
    oss << "{\"room\":\"" << this->room_id_ << "\",\"phase\":\"" << this->phase_name() << "\",\"tick\":" << this->round_tick_ << ",\"players\":[";
    for (std::size_t i = 0; i < this->room_order_.size(); ++i)
    {
        std::map<std::string, Participant>::const_iterator it = this->participants_.find(this->room_order_[i]);
        if (it == this->participants_.end())
            continue;
        const Participant &participant = it->second;
        if (i != 0)
            oss << ",";
        oss << "{\"nick\":\"" << participant.nick << "\",\"x\":" << participant.x << ",\"y\":" << participant.y
            << ",\"hp\":" << participant.hp << ",\"alive\":" << bool_to_json(participant.alive)
            << ",\"connected\":" << bool_to_json(participant.connected) << ",\"facing\":\"" << participant.facing << "\"}";
    }
    oss << "],\"projectiles\":[";
    for (std::size_t i = 0; i < this->projectiles_.size(); ++i)
    {
        if (i != 0)
            oss << ",";
        oss << "{\"owner\":\"" << this->projectiles_[i].owner_token << "\",\"x\":" << this->projectiles_[i].x
            << ",\"y\":" << this->projectiles_[i].y << "}";
    }
    oss << "]}";
    return oss.str();
}

std::string MatchEngine::phase_name() const
{
    return phase_to_string(this->phase_);
}

std::uint64_t MatchEngine::global_tick() const
{
    return this->global_tick_;
}

std::uint64_t MatchEngine::round_tick() const
{
    return this->round_tick_;
}

bool MatchEngine::is_valid_nick(const std::string &nick) const
{
    if (nick.empty() || nick.size() > 16)
        return false;
    if (!std::isalpha(static_cast<unsigned char>(nick[0])))
        return false;
    for (std::size_t i = 1; i < nick.size(); ++i)
    {
        const unsigned char ch = static_cast<unsigned char>(nick[i]);
        if (!std::isalnum(ch) && ch != '_')
            return false;
    }
    return true;
}

bool MatchEngine::all_room_players_ready() const
{
    for (std::vector<std::string>::const_iterator it = this->room_order_.begin(); it != this->room_order_.end(); ++it)
    {
        std::map<std::string, Participant>::const_iterator found = this->participants_.find(*it);
        if (found == this->participants_.end() || !found->second.ready)
            return false;
    }
    return !this->room_order_.empty();
}

int MatchEngine::alive_count() const
{
    int count = 0;
    for (std::vector<std::string>::const_iterator it = this->room_order_.begin(); it != this->room_order_.end(); ++it)
    {
        std::map<std::string, Participant>::const_iterator found = this->participants_.find(*it);
        if (found != this->participants_.end() && found->second.alive)
            ++count;
    }
    return count;
}

void MatchEngine::emit_single(const std::string &token, const std::string &line)
{
    this->events_.push_back(Event(EventScope::Single, token, line));
}

void MatchEngine::emit_room(const std::string &line)
{
    this->events_.push_back(Event(EventScope::Room, std::string(), line));
}

void MatchEngine::start_countdown()
{
    if (this->phase_ != Phase::Lobby)
        return;

    this->phase_ = Phase::Countdown;
    this->countdown_remaining_ = countdown_steps;
    this->emit_room("ROOM " + this->room_id_ + " countdown");
    {
        std::ostringstream oss;
        oss << "COUNTDOWN " << this->countdown_remaining_;
        this->emit_room(oss.str());
    }
}

void MatchEngine::start_round()
{
    this->phase_ = Phase::InRound;
    this->round_tick_ = 0;
    this->countdown_remaining_ = 0;
    this->projectiles_.clear();
    this->reset_spawn_state();
    this->clear_pending_inputs();
    this->emit_room("ROOM " + this->room_id_ + " in_round");
    this->emit_room("SNAPSHOT 0 " + this->snapshot_json());
}

void MatchEngine::process_inputs()
{
    for (std::vector<std::string>::const_iterator it = this->room_order_.begin(); it != this->room_order_.end(); ++it)
    {
        Participant &participant = this->participants_[*it];
        if (!participant.alive || !participant.connected)
            continue;

        if (!participant.has_pending_input)
            continue;

        participant.facing = participant.pending_input.facing;
        const int next_x = std::max(0, std::min(board_width - 1, participant.x + participant.pending_input.dx));
        const int next_y = std::max(0, std::min(board_height - 1, participant.y + participant.pending_input.dy));
        participant.x = next_x;
        participant.y = next_y;

        if (participant.pending_input.fire)
        {
            const std::pair<int, int> delta = direction_delta(participant.facing);
            const int spawn_x = participant.x + delta.first;
            const int spawn_y = participant.y + delta.second;
            if (spawn_x >= 0 && spawn_x < board_width && spawn_y >= 0 && spawn_y < board_height)
                this->projectiles_.push_back(Projectile(participant.token, spawn_x, spawn_y, delta.first, delta.second));
        }

        participant.has_pending_input = false;
    }
}

void MatchEngine::move_projectiles()
{
    std::vector<Projectile> survivors;
    for (std::vector<Projectile>::iterator it = this->projectiles_.begin(); it != this->projectiles_.end(); ++it)
    {
        it->x += it->vx;
        it->y += it->vy;
        if (it->x < 0 || it->x >= board_width || it->y < 0 || it->y >= board_height)
            continue;

        bool hit = false;
        for (std::vector<std::string>::const_iterator room_it = this->room_order_.begin(); room_it != this->room_order_.end(); ++room_it)
        {
            Participant &target = this->participants_[*room_it];
            if (!target.alive || target.token == it->owner_token)
                continue;
            if (target.x == it->x && target.y == it->y)
            {
                hit = true;
                --target.hp;
                {
                    std::ostringstream oss;
                    oss << "HIT " << this->round_tick_ << " " << this->participants_[it->owner_token].nick << " " << target.nick << " " << target.hp;
                    this->emit_room(oss.str());
                }
                if (target.hp <= 0)
                {
                    target.alive = false;
                    std::ostringstream oss;
                    oss << "ELIM " << this->round_tick_ << " " << target.nick;
                    this->emit_room(oss.str());
                }
                break;
            }
        }

        if (!hit)
            survivors.push_back(*it);
    }
    this->projectiles_.swap(survivors);
}

void MatchEngine::maybe_finish_round()
{
    if (this->phase_ != Phase::InRound)
        return;

    const int alive = this->alive_count();
    if (alive <= 1)
    {
        const std::string winner = this->winner_nick();
        this->phase_ = Phase::Finished;
        if (winner.empty())
            this->emit_room("ROUND_END draw");
        else
            this->emit_room("ROUND_END " + winner);
        this->emit_room("ROOM " + this->room_id_ + " finished");
        return;
    }

    if (static_cast<int>(this->round_tick_) >= max_round_ticks)
    {
        this->phase_ = Phase::Finished;
        this->emit_room("ROUND_END draw");
        this->emit_room("ROOM " + this->room_id_ + " finished");
    }
}

void MatchEngine::expire_disconnected_players()
{
    for (std::vector<std::string>::const_iterator it = this->room_order_.begin(); it != this->room_order_.end(); ++it)
    {
        Participant &participant = this->participants_[*it];
        if (participant.connected || participant.disconnect_tick < 0)
            continue;
        if (static_cast<int>(this->global_tick_) - participant.disconnect_tick <= grace_ticks)
            continue;
        if (this->phase_ == Phase::InRound && participant.alive)
        {
            participant.alive = false;
            std::ostringstream oss;
            oss << "ELIM " << this->round_tick_ << " " << participant.nick;
            this->emit_room(oss.str());
        }
    }
}

void MatchEngine::reset_spawn_state()
{
    static const int spawn_table[4][3] = {
        {2, 2, 'E'},
        {5, 2, 'W'},
        {2, 5, 'E'},
        {5, 5, 'W'},
    };

    for (std::size_t i = 0; i < this->room_order_.size(); ++i)
    {
        Participant &participant = this->participants_[this->room_order_[i]];
        participant.alive = true;
        participant.hp = max_hp;
        participant.x = spawn_table[i][0];
        participant.y = spawn_table[i][1];
        participant.facing = static_cast<char>(spawn_table[i][2]);
    }
}

void MatchEngine::clear_pending_inputs()
{
    for (std::map<std::string, Participant>::iterator it = this->participants_.begin(); it != this->participants_.end(); ++it)
        it->second.has_pending_input = false;
}

void MatchEngine::remove_from_room(const std::string &token)
{
    std::vector<std::string>::iterator room_it = std::find(this->room_order_.begin(), this->room_order_.end(), token);
    if (room_it != this->room_order_.end())
        this->room_order_.erase(room_it);
    std::map<std::string, Participant>::iterator it = this->participants_.find(token);
    if (it != this->participants_.end())
    {
        it->second.in_room = false;
        it->second.ready = false;
        it->second.has_pending_input = false;
    }
}

std::string MatchEngine::winner_nick() const
{
    for (std::vector<std::string>::const_iterator it = this->room_order_.begin(); it != this->room_order_.end(); ++it)
    {
        std::map<std::string, Participant>::const_iterator found = this->participants_.find(*it);
        if (found != this->participants_.end() && found->second.alive)
            return found->second.nick;
    }
    return "";
}

std::string MatchEngine::phase_to_string(Phase phase)
{
    switch (phase)
    {
    case Phase::Lobby:
        return "lobby";
    case Phase::Countdown:
        return "countdown";
    case Phase::InRound:
        return "in_round";
    case Phase::Finished:
        return "finished";
    }
    return "unknown";
}
