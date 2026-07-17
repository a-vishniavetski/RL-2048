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


def evaluate():
    return random.choice([Move.LEFT, Move.RIGHT, Move.UP, Move.DOWN])


def make_move(move: Move, board):
    move_function = move_left_or_right if move in (Move.LEFT, Move.RIGHT) else move_up_or_down

    reward, board_has_changed = move_function(board, move)  # board is in afterstate s'
    afterstate = board.copy()
    if board_has_changed:
        spawn_random_tile(board, rng)  # board is in the next state, s''
    return reward, afterstate


def learn_evaluation(state, action, reward, afterstate, new_state):
    pass

class Env():
    pass


if __name__ == "__main__":
    number_of_games = 1000
    games_played = 0
    reward_all_games = 0
    highest_tile = 2

    while games_played < number_of_games:
        rng = np.random.default_rng(0)
        history: list[tuple[Move, np.ndarray]] = []
        state = init_board(rng)
        episode_reward = 0
        terminal_state = False
        history.append((None, state.copy()))
        training = False
        while not terminal_state:
            old_state = state.copy()
            action = evaluate()
            reward, afterstate = make_move(action, state)  # board is in new state s''

            if training:
                learn_evaluation(old_state, action, reward, afterstate, state)

            # print("\n")
            # print("State s:")
            # print(old_state)
            # print(f"Action: {action.name}")
            # print(f"Afterstate s':")
            # print(afterstate)
            # print(f"New state s'':")
            # print(state)

            episode_reward += reward
            history.append((action, state.copy()))

            terminal_state = has_lost(state)
            # if terminal_state:
            #     print(f"GAME OVER; Total reward: {episode_reward}")

        games_played += 1
        reward_all_games += episode_reward
        this_game_highest_tile = state.max()
        if this_game_highest_tile > highest_tile:
            highest_tile = this_game_highest_tile

        _average =reward_all_games / games_played
        print(f"Played {games_played} games, total reward: {reward_all_games}, Avg.: {_average:.2f}, Highest tile: {highest_tile}")

        # for last_action, _state in history:
        #     print(f"Last action: {last_action}")
        #     print(_state, end="\n\n")
