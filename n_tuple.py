import numpy as np

board = np.array(
    [
        [2, 2, 4, 4],
        [2, 0, 4, 4],
        [0, 4, 4, 2],
        [2, 8, 4, 4],
    ]
)

_tuple = np.array([(0, 1), (1, 1), (2, 1), (3, 1)])

for _row, _col in _tuple:
    print(board[_row][_col])

# all_combinations =
# _tuple_weights = np.array(  # LUT mapping all possible combinations of 4 consequtive powers of 2 up to 2**15; need to encode board values with log;

# )

powers_of_two = [0,] + [2**_pow for _pow in range(1, 15)]
board_states = [(i, j) for j in powers_of_two for i in powers_of_two]
# print(board_states)


def lut_index(n_tuple: np.ndarray, c: int = 15, n: int = 2):
    assert isinstance(n_tuple, np.ndarray), "n_tuple must be a NumPy ndarray"

    encoded_tuple = np.zeros_like(n_tuple)
    mask = n_tuple != 0
    encoded_tuple[mask] = np.log2(n_tuple[mask]).astype(np.int32)
    _index = 0
    for tuple_element_position in range(0, n):
        value = encoded_tuple[tuple_element_position]
        _index += value * (c ** (tuple_element_position))
    return _index


for _state in board_states[:17]:
    print(_state, lut_index(np.asarray(_state)))
