#pragma once

#include <map>
#include <stdexcept>
#include <string>

struct PlayerInput
{
    int  frame;
    int  dx;
    int  dy;
    bool boost;

    PlayerInput();
    PlayerInput(int next_frame, int delta_x, int delta_y, bool boost_flag);
    bool operator==(const PlayerInput &other) const;
    bool operator!=(const PlayerInput &other) const;
};

struct PlayerState
{
    int x;
    int y;
    int stamina;

    PlayerState();
    PlayerState(int pos_x, int pos_y, int next_stamina);
};

struct WorldState
{
    int                                frame;
    std::map<std::string, PlayerState> players;

    WorldState();
};

struct StateSnapshot
{
    int        frame;
    WorldState world;

    StateSnapshot();
    StateSnapshot(int next_frame, const WorldState &next_world);
};

struct ResimResult
{
    bool rolled_back;
    int  rollback_from_frame;
    int  replayed_through_frame;
    int  frames_replayed;
    bool converged;

    ResimResult();
};

class FrameInputBuffer
{
public:
    void submit(const std::string &player_id, const PlayerInput &input);
    bool try_get(const std::string &player_id, int frame, PlayerInput &input) const;

private:
    std::map<int, std::map<std::string, PlayerInput> > frames_;
};

class RollbackSession
{
public:
    static const int board_min;
    static const int board_max;
    static const int default_stamina;

    RollbackSession();

    void          add_player(const std::string &player_id, int x, int y);
    ResimResult   submit_input(const std::string &player_id, const PlayerInput &input);
    void          advance_to_frame(int target_frame);
    WorldState    world() const;
    StateSnapshot snapshot_at(int frame) const;
    PlayerInput   applied_input(const std::string &player_id, int frame) const;

private:
    WorldState                                              world_;
    FrameInputBuffer                                        buffer_;
    std::map<int, StateSnapshot>                            snapshots_;
    std::map<int, std::map<std::string, PlayerInput> >      applied_inputs_;

    void                                           ensure_player_exists(const std::string &player_id) const;
    void                                           simulate_frame(int frame);
    std::map<std::string, PlayerInput>             resolve_inputs_for_frame(int frame) const;
    PlayerInput                                    predicted_input_for(const std::string &player_id, int frame) const;
    static WorldState                              simulate_once(
        const WorldState &base,
        int frame,
        const std::map<std::string, PlayerInput> &inputs
    );
    void                                           restore_snapshot(int frame);
    bool                                           verify_replay(int rollback_from, int replay_to, const WorldState &expected_final) const;
    static bool                                    states_equal(const WorldState &left, const WorldState &right);
    static int                                     clamp_to_board(int value);
};
