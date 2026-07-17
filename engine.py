import numpy as np
from numpy import ndarray, array


rng = np.random.default_rng(0)


def init_board():
    board = np.zeros((4, 4), dtype=np.int16)
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
    return new_row, row_moving_score


def move_left(board: ndarray):
    move_score = 0
    for row_index in range(0, 4):
        board[row_index], row_moving_score = move_row(board[row_index])
        move_score += row_moving_score
    return move_score


def move_right(board: ndarray):
    move_score = 0
    for row_index in range(0, 4):
        board[row_index], row_moving_score = move_row(board[row_index], _reversed=True)
        move_score += row_moving_score
    return move_score


def move_up(board: ndarray):
    move_score = 0
    transposed_board = np.transpose(board)
    move_left(transposed_board)
    board = transposed_board
    return move_score


def move_down(board: ndarray):
    move_score = 0
    transposed_board = np.transpose(board)
    move_right(transposed_board)
    board = transposed_board
    return move_score


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

