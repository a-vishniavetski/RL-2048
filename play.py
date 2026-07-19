from copy import deepcopy
from typing import List
import random
import numpy as np
from engine import (
    move_left_or_right,
    move_up_or_down,
    init_board,
    has_lost,
    init_board,
    spawn_random_tile,
    Move,
)

from n_tuple_network import NTupleNetwork, N_tuple, BOARD_DTYPE


def make_move(move: Move, board, rng):
    move_function = (
        move_left_or_right if move in (Move.LEFT, Move.RIGHT) else move_up_or_down
    )

    reward, board_has_changed = move_function(board, move)  # board is in afterstate s'
    afterstate = board.copy()
    if board_has_changed:
        spawn_random_tile(board, rng)  # board is in the next state, s''
    else:
        # don't spawn random tile
        reward = -10000  # punish actions without any effects
    return reward, afterstate


def evaluate(state: np.ndarray):
    return random.choice([Move.LEFT, Move.RIGHT, Move.UP, Move.DOWN])


def learn_evaluation(state, action, reward, afterstate, new_state):
    pass


class Env:
    pass

# class Policy():

#     def __init__(self, networks: List[NTupleNetwork], learning_rate: float = 0.2):
#         self.networks = networks
#         self.leaning_rate = learning_rate

class ActionEvaluationPolicy():

    def __init__(self, networks: List[NTupleNetwork], learning_rate: float = 0.2):
        # super().__init__(networks, learning_rate)
        self.networks = networks
        self.learning_rate = learning_rate

    def determine_action(self, state: np.ndarray):
        action_values = [self.evaluate(state, _action) for _action in Move]
        return Move(int(np.argmax(action_values)) + 1)  # returns int respective for a Move

    def evaluate(self, state: np.ndarray, action: Move):
        network_id = action.value - 1  # Enum goes from 1 to 4, list idx from 0 to 3; LEFT corresponds to networks[0]
        network_for_action = self.networks[network_id]  # V_a(s)
        action_value = network_for_action.state_value_function(state)
        return action_value  # returns the value of state value function specific for a given action

    def learn_evaluation(self, old_state: np.ndarray, action: Move, reward: float, afterstate: np.ndarray, state: np.ndarray):
        # best_next_action = None
        # best_next_action_value = -np.inf
        # for next_action in (Move.LEFT, Move.RIGHT, Move.UP, Move.DOWN):
        #     next_action_value = self.evaluate(state, next_action)
        #     if next_action_value > best_next_action_value:
        #         best_next_action_value  = next_action_value
        #         best_next_action = next_action
        next_action_values = [self.evaluate(state, next_action) for next_action in Move]
        best_next_action_value = np.max(next_action_values)
        best_next_action = Move(int(np.argmax(next_action_values)) + 1)
        network_id = best_next_action.value - 1
        network_for_action = self.networks[network_id]

        old_state_action_value = network_for_action.state_value_function(state)
        oldstate_newstate_delta = best_next_action_value - old_state_action_value
        new_state_value = old_state_action_value + self.learning_rate * (reward + oldstate_newstate_delta)
        network_for_action.update_value_function(old_state, new_state_value)


def play_episode(policy: ActionEvaluationPolicy, debug_game_num: int = None):
    rng = np.random.default_rng(0)
    history: list[tuple[Move, np.ndarray]] = []
    state = init_board(rng)
    score = 0
    is_terminal_state = False
    history.append((None, state.copy()))
    training = True
    action_counter = 1  # debug
    while not is_terminal_state:
        old_state = state.copy()
        action = policy.determine_action(state)
        print(f"Game [{debug_game_num}] Action [{action_counter}]: {action.name}")
        action_counter += 1
        reward, afterstate = make_move(action, state, rng)  # board is in new state s''

        if training:
            policy.learn_evaluation(old_state, action, reward, afterstate, state)

        score += reward
        history.append((action, state.copy()))
        print(state)
        is_terminal_state = has_lost(state)

    highest_tile = state.max()
    return score, highest_tile


def state_evaluation_function():
    pass  # uses a single state value function


def afterstate_evaluation_function():
    pass  # uses a single state value function


if __name__ == "__main__":

    number_of_games = 10
    games_played = 0
    score_all_games = 0
    highest_tile = 2

    tuples = []
    # 4 vertical 4-tuples
    for j in range(4):
        n_tuple = N_tuple(
            [
                (i, j) for i in range(4)
            ]
        )
        tuples.append(n_tuple)

    # 4 horizontal 4-tuples
    for i in range(4):
        n_tuple = N_tuple(
            [
                (i, j) for j in range(4)
            ]
        )
        tuples.append(n_tuple)


    network = NTupleNetwork(tuples)
    networks = [deepcopy(network) for _ in range(4)]

    policy = ActionEvaluationPolicy(networks)

    while games_played < number_of_games:
        episode_score, this_game_highest_tile = play_episode(policy, games_played + 1)
        games_played += 1
        score_all_games += episode_score
        if this_game_highest_tile > highest_tile:
            highest_tile = this_game_highest_tile

    _average = score_all_games / games_played
    print(
        f"Played {games_played} games, Avg. Reward: {_average:.2f}, Highest tile: {highest_tile}"
    )



    # ToDo: logging total score and highest tile each game; abstraction layer to set experiment hyperparams; RL implementation
