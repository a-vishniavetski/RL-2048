import numpy as np
from numpy import ndarray, array

from enum import Enum

class Move(Enum):
    LEFT  = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


rng = np.random.default_rng(0)


def init_board():
    board = np.zeros((4, 4), dtype=np.int32)
    spawn_random_tile(board)
    spawn_random_tile(board)
    return board

def check_wincon(board):
    if board[board == 2048].any():
        return True
    return False

def move_row(row, _reversed: bool = False):
    """Move and merge row to the left. Set reversed for right.
    Returns (new_row, move_score)"""
    compressed_row = row[row != 0]

    row_moving_score = 0

    if _reversed:
        compressed_row = compressed_row[::-1]

    column_index = 0
    while column_index < len(compressed_row) - 1:
        if compressed_row[column_index] == compressed_row[column_index + 1]:
            compressed_row[column_index] *= 2
            compressed_row[column_index + 1] = 0
            row_moving_score += compressed_row[column_index]
            column_index += 2
        else:
            column_index += 1

    compressed_row = compressed_row[compressed_row != 0]
    cells_to_pad = 4 - len(compressed_row)
    if _reversed:
        compressed_row = compressed_row[::-1]
        new_row = np.pad(compressed_row, (cells_to_pad, 0))
    else:
        new_row = np.pad(compressed_row, (0, cells_to_pad))

    row_has_changed = (not np.array_equal(row, new_row))
    return new_row, row_moving_score, row_has_changed

def move_left_or_right(board: ndarray, direction: Move):
    _reversed = False if direction is Move.LEFT else True
    move_score = 0
    board_has_changed = False
    for row_index in range(0, 4):
        board[row_index], row_moving_score, row_has_changed = move_row(board[row_index], _reversed=_reversed)
        move_score += row_moving_score
        if row_has_changed:
            board_has_changed = True
    return move_score, board_has_changed


def move_up_or_down(board: ndarray, direction: Move):
    transposed_board = np.transpose(board)
    if direction is Move.UP:
        move_score, board_has_changed = move_left_or_right(transposed_board, Move.LEFT)
    else:
        move_score, board_has_changed = move_left_or_right(transposed_board, Move.RIGHT)
    board = transposed_board
    return move_score, board_has_changed


def has_moves(board):
    return (
        (board == 0).any() or
        (board[:, :-1] == board[:, 1:]).any() or
        (board[:-1, :] == board[1:, :]).any()
    )

def spawn_random_tile(board: ndarray):
    empty = np.flatnonzero(board == 0)
    if empty.size:
        idx = rng.choice(empty)
        board.flat[idx] = 2 if rng.random() < 0.9 else 4


def has_lost(board):
    return not has_moves(board)

if __name__ == "__main__":
    board = init_board()
    print(board)
    spawn_random_tile(board)
    print(board)
    spawn_random_tile(board)
    print(board)
    spawn_random_tile(board)
    print(board)

