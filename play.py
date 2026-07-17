from engine import (
    move_left_or_right, move_up_or_down, init_board, has_lost, init_board, spawn_random_tile, Move
)

import random
from enum import Enum


def choose_move():
    return random.choice([Move.LEFT, Move.RIGHT, Move.UP, Move.DOWN])

def make_move(move: Move, board):
    if move in (Move.LEFT, Move.RIGHT):
        move_score, board_has_changed = move_left_or_right(board, move)
        return move_score, board_has_changed
    move_score, board_has_changed = move_up_or_down(board, move)
    return move_score, board_has_changed


if __name__ == "__main__":
    board = init_board()
    total_score = 0
    lost = False
    while not lost:
        next_move = choose_move()
        move_score, board_has_changed =  make_move(next_move, board)
        print(f"Made move: {next_move.name}")
        print(f"Board has changed: {board_has_changed}")
        total_score += move_score
        spawn_random_tile(board)
        lost = has_lost(board)
        print(f"GAME OVER; Total score: {total_score}")
        print(board)



