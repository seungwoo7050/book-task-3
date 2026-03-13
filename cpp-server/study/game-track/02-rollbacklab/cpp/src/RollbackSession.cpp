#include "inc/RollbackSession.hpp"

const int RollbackSession::board_min = 0;
const int RollbackSession::board_max = 12;
const int RollbackSession::default_stamina = 3;

PlayerInput::PlayerInput()
    : frame(0), dx(0), dy(0), boost(false)
{
}

PlayerInput::PlayerInput(int next_frame, int delta_x, int delta_y, bool boost_flag)
    : frame(next_frame), dx(delta_x), dy(delta_y), boost(boost_flag)
{
}

bool PlayerInput::operator==(const PlayerInput &other) const
{
    return this->frame == other.frame &&
           this->dx == other.dx &&
           this->dy == other.dy &&
           this->boost == other.boost;
}

bool PlayerInput::operator!=(const PlayerInput &other) const
{
    return !(*this == other);
}

PlayerState::PlayerState()
    : x(0), y(0), stamina(RollbackSession::default_stamina)
{
}

PlayerState::PlayerState(int pos_x, int pos_y, int next_stamina)
    : x(pos_x), y(pos_y), stamina(next_stamina)
{
}

WorldState::WorldState()
    : frame(0), players()
{
}

StateSnapshot::StateSnapshot()
    : frame(0), world()
{
}

StateSnapshot::StateSnapshot(int next_frame, const WorldState &next_world)
    : frame(next_frame), world(next_world)
{
}

ResimResult::ResimResult()
    : rolled_back(false),
      rollback_from_frame(0),
      replayed_through_frame(0),
      frames_replayed(0),
      converged(true)
{
}

void FrameInputBuffer::submit(const std::string &player_id, const PlayerInput &input)
{
    this->frames_[input.frame][player_id] = input;
}

bool FrameInputBuffer::try_get(const std::string &player_id, int frame, PlayerInput &input) const
{
    std::map<int, std::map<std::string, PlayerInput> >::const_iterator frame_it = this->frames_.find(frame);
    if (frame_it == this->frames_.end())
        return false;
    std::map<std::string, PlayerInput>::const_iterator player_it = frame_it->second.find(player_id);
    if (player_it == frame_it->second.end())
        return false;
    input = player_it->second;
    return true;
}

RollbackSession::RollbackSession()
    : world_(), buffer_(), snapshots_(), applied_inputs_()
{
    this->snapshots_.insert(std::make_pair(0, StateSnapshot(0, this->world_)));
}

void RollbackSession::add_player(const std::string &player_id, int x, int y)
{
    this->world_.players[player_id] = PlayerState(clamp_to_board(x), clamp_to_board(y), default_stamina);
    this->snapshots_[0] = StateSnapshot(0, this->world_);
}

ResimResult RollbackSession::submit_input(const std::string &player_id, const PlayerInput &input)
{
    this->ensure_player_exists(player_id);
    this->buffer_.submit(player_id, input);

    ResimResult result;
    result.replayed_through_frame = this->world_.frame;
    if (input.frame > this->world_.frame)
        return result;

    PlayerInput applied = this->applied_input(player_id, input.frame);
    if (applied == input)
        return result;

    const int replay_to = this->world_.frame;
    this->restore_snapshot(input.frame - 1);
    for (int frame = input.frame; frame <= replay_to; ++frame)
        this->simulate_frame(frame);

    result.rolled_back = true;
    result.rollback_from_frame = input.frame;
    result.replayed_through_frame = replay_to;
    result.frames_replayed = replay_to - input.frame + 1;
    result.converged = this->verify_replay(input.frame, replay_to, this->world_);
    return result;
}

void RollbackSession::advance_to_frame(int target_frame)
{
    if (target_frame <= this->world_.frame)
        return;
    for (int frame = this->world_.frame + 1; frame <= target_frame; ++frame)
        this->simulate_frame(frame);
}

WorldState RollbackSession::world() const
{
    return this->world_;
}

StateSnapshot RollbackSession::snapshot_at(int frame) const
{
    std::map<int, StateSnapshot>::const_iterator it = this->snapshots_.find(frame);
    if (it == this->snapshots_.end())
        throw std::runtime_error("snapshot missing");
    return it->second;
}

PlayerInput RollbackSession::applied_input(const std::string &player_id, int frame) const
{
    std::map<int, std::map<std::string, PlayerInput> >::const_iterator frame_it = this->applied_inputs_.find(frame);
    if (frame_it == this->applied_inputs_.end())
        return PlayerInput(frame, 0, 0, false);
    std::map<std::string, PlayerInput>::const_iterator player_it = frame_it->second.find(player_id);
    if (player_it == frame_it->second.end())
        return PlayerInput(frame, 0, 0, false);
    return player_it->second;
}

void RollbackSession::ensure_player_exists(const std::string &player_id) const
{
    if (this->world_.players.find(player_id) == this->world_.players.end())
        throw std::runtime_error("unknown player");
}

void RollbackSession::simulate_frame(int frame)
{
    std::map<std::string, PlayerInput> inputs = this->resolve_inputs_for_frame(frame);
    this->world_ = simulate_once(this->world_, frame, inputs);
    this->applied_inputs_[frame] = inputs;
    this->snapshots_[frame] = StateSnapshot(frame, this->world_);
}

std::map<std::string, PlayerInput> RollbackSession::resolve_inputs_for_frame(int frame) const
{
    std::map<std::string, PlayerInput> resolved;
    for (std::map<std::string, PlayerState>::const_iterator it = this->world_.players.begin();
         it != this->world_.players.end();
         ++it)
    {
        PlayerInput input;
        if (this->buffer_.try_get(it->first, frame, input))
            resolved[it->first] = input;
        else
            resolved[it->first] = this->predicted_input_for(it->first, frame);
    }
    return resolved;
}

PlayerInput RollbackSession::predicted_input_for(const std::string &player_id, int frame) const
{
    if (frame <= 1)
        return PlayerInput(frame, 0, 0, false);

    std::map<int, std::map<std::string, PlayerInput> >::const_iterator prev_frame = this->applied_inputs_.find(frame - 1);
    if (prev_frame == this->applied_inputs_.end())
        return PlayerInput(frame, 0, 0, false);

    std::map<std::string, PlayerInput>::const_iterator it = prev_frame->second.find(player_id);
    if (it == prev_frame->second.end())
        return PlayerInput(frame, 0, 0, false);

    PlayerInput predicted = it->second;
    predicted.frame = frame;
    return predicted;
}

WorldState RollbackSession::simulate_once(
    const WorldState &base,
    int frame,
    const std::map<std::string, PlayerInput> &inputs
)
{
    WorldState next = base;
    next.frame = frame;

    for (std::map<std::string, PlayerState>::iterator it = next.players.begin(); it != next.players.end(); ++it)
    {
        const PlayerInput &input = inputs.find(it->first)->second;
        int                stride = 1;
        if (input.boost && it->second.stamina > 0)
        {
            stride = 2;
            it->second.stamina -= 1;
        }
        it->second.x = clamp_to_board(it->second.x + (input.dx * stride));
        it->second.y = clamp_to_board(it->second.y + (input.dy * stride));
    }

    return next;
}

void RollbackSession::restore_snapshot(int frame)
{
    if (frame < 0)
        frame = 0;

    std::map<int, StateSnapshot>::const_iterator snapshot = this->snapshots_.find(frame);
    if (snapshot == this->snapshots_.end())
        throw std::runtime_error("rollback snapshot missing");

    this->world_ = snapshot->second.world;

    for (std::map<int, StateSnapshot>::iterator it = this->snapshots_.begin(); it != this->snapshots_.end(); )
    {
        if (it->first > frame)
            it = this->snapshots_.erase(it);
        else
            ++it;
    }
    for (std::map<int, std::map<std::string, PlayerInput> >::iterator it = this->applied_inputs_.begin();
         it != this->applied_inputs_.end();)
    {
        if (it->first > frame)
            it = this->applied_inputs_.erase(it);
        else
            ++it;
    }
}

bool RollbackSession::verify_replay(int rollback_from, int replay_to, const WorldState &expected_final) const
{
    if (rollback_from > replay_to)
        return true;

    StateSnapshot           base_snapshot = this->snapshot_at(rollback_from - 1 < 0 ? 0 : rollback_from - 1);
    WorldState              replayed = base_snapshot.world;
    for (int frame = rollback_from; frame <= replay_to; ++frame)
    {
        std::map<int, std::map<std::string, PlayerInput> >::const_iterator inputs = this->applied_inputs_.find(frame);
        if (inputs == this->applied_inputs_.end())
            return false;
        replayed = simulate_once(replayed, frame, inputs->second);
    }
    return states_equal(replayed, expected_final);
}

bool RollbackSession::states_equal(const WorldState &left, const WorldState &right)
{
    if (left.frame != right.frame || left.players.size() != right.players.size())
        return false;

    for (std::map<std::string, PlayerState>::const_iterator it = left.players.begin(); it != left.players.end(); ++it)
    {
        std::map<std::string, PlayerState>::const_iterator other = right.players.find(it->first);
        if (other == right.players.end())
            return false;
        if (it->second.x != other->second.x ||
            it->second.y != other->second.y ||
            it->second.stamina != other->second.stamina)
        {
            return false;
        }
    }
    return true;
}

int RollbackSession::clamp_to_board(int value)
{
    if (value < board_min)
        return board_min;
    if (value > board_max)
        return board_max;
    return value;
}
