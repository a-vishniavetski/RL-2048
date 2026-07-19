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


def make_move(move: Move, board, rng):
    move_function = (
        move_left_or_right if move in (Move.LEFT, Move.RIGHT) else move_up_or_down
    )

    reward, board_has_changed = move_function(board, move)  # board is in afterstate s'
    afterstate = board.copy()
    if board_has_changed:
        spawn_random_tile(board, rng)  # board is in the next state, s''
    return reward, afterstate


def evaluate(state: np.ndarray):
    return random.choice([Move.LEFT, Move.RIGHT, Move.UP, Move.DOWN])


def learn_evaluation(state, action, reward, afterstate, new_state):
    pass


class Env:
    pass


def play_episode(evaluation_function, evaluation_learning_function):
    rng = np.random.default_rng(0)
    history: list[tuple[Move, np.ndarray]] = []
    state = init_board(rng)
    score = 0
    terminal_state = False
    history.append((None, state.copy()))
    training = False
    while not terminal_state:
        old_state = state.copy()
        action = evaluation_function(state)
        reward, afterstate = make_move(action, state, rng)  # board is in new state s''

        if training:
            evaluation_learning_function(old_state, action, reward, afterstate, state)

        score += reward
        history.append((action, state.copy()))

        terminal_state = has_lost(state)

    highest_tile = state.max()
    return score, highest_tile


def action_evaluation_function():
    pass  # returns the value of state value function specific for a given action


def state_evaluation_function():
    pass  # uses a single state value function


def afterstate_evaluation_function():
    pass  # uses a single state value function


if __name__ == "__main__":
    number_of_games = 300
    games_played = 0
    score_all_games = 0
    highest_tile = 2

    while games_played < number_of_games:
        episode_score, this_game_highest_tile = play_episode(
            evaluation_function=evaluate, evaluation_learning_function=learn_evaluation
        )
        games_played += 1
        score_all_games += episode_score
        if this_game_highest_tile > highest_tile:
            highest_tile = this_game_highest_tile

    _average = score_all_games / games_played
    print(
        f"Played {games_played} games, Avg. Reward: {_average:.2f}, Highest tile: {highest_tile}"
    )

    # ToDo: logging total score and highest tile each game; abstraction layer to set experiment hyperparams; RL implementation
