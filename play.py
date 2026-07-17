from engine import (
    move_down,  move_left, move_right, move_up, init_board, has_lost, init_board, spawn_random_tile
)

import random
from enum import Enum

class Move(Enum):
    LEFT  = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

def choose_move():
    return random.choice([Move.LEFT, Move.RIGHT, Move.UP, Move.DOWN])

def make_move(move: Move, board):
    match move:
        case Move.LEFT:
            move_score = move_left(board)
        case Move.RIGHT:
            move_score = move_right(board)
        case Move.UP:
            move_score = move_up(board)
        case Move.DOWN:
            move_score = move_down(board)
    return move_score

if __name__ == "__main__":
    board = init_board()
    total_score = 0
    lost = False
    while not lost:
        next_move = choose_move()
        move_score =  make_move(next_move, board)
        print(f"Made move: {next_move.name}")
        total_score += move_score
        spawn_random_tile(board)
        lost = has_lost(board)
        print(board)


