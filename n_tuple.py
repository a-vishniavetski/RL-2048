from dataclasses import dataclass
from typing import Tuple, List
import numpy as np

BOARD_DTYPE = np.int16
TUPLE_WEIGHTS_DTYPE  = np.float32

C = 15  # := maximum_power_of_two_allowed + 1
BOARD = np.array(
    [
        [2, 2, 4, 4],
        [2, 0, 4, 4],
        [0, 4, 4, 2],
        [2, 8, 4, 4],
    ], dtype=BOARD_DTYPE
)

class N_tuple():
    def __init__(self, locations: List[Tuple[int, int]], c: int = C):
        self.locations = locations  # predetermined sequence of board locations
        self._length = len(self.locations)
        self.lookup_size = c**self._length
        self.lookup_table = np.zeros(self.lookup_size, dtype=TUPLE_WEIGHTS_DTYPE)

def weight_lookup_index(board_elements: np.ndarray, c: int = C, tuple_length: int = 4):
    # we encode board values ("2", "16") into their powers of 2 (1, 4); then convert to base-c from base-10

    assert isinstance(board_elements, np.ndarray), "board values must be a NumPy ndarray"

    encoded_board_elements = np.zeros_like(board_elements, dtype=BOARD_DTYPE)
    non_zero_mask = board_elements != 0
    encoded_board_elements[non_zero_mask] = np.log2(board_elements[non_zero_mask]).astype(BOARD_DTYPE)
    precomputed_powers = c * np.arange(tuple_length)
    weight_index = encoded_board_elements @ precomputed_powers
    return weight_index

# n-tuple network of m tuples implements a function approximator f(s) :=
def state_value_function(tuple_network: List[N_tuple], board_state: np.ndarray):
    assert board_state.dtype == BOARD_DTYPE, f"Game board elements must be dtype={BOARD_DTYPE}"
    state_value = 0
    for _tuple in tuple_network:
        rows, cols = zip(*_tuple.locations)
        relevant_elements = board_state[rows, cols]
        combination_weight = _tuple.lookup_table[weight_lookup_index(relevant_elements, tuple_length=_tuple._length)]
        state_value += combination_weight
    return state_value

if __name__ == "__main__":
    n_tuple = N_tuple([(0,1), (1, 1), (2, 1), (3, 1)])
    print("Tuple locations:", n_tuple.locations)
    rows, cols = zip(*n_tuple.locations)
    relevant_elements = BOARD[rows, cols]
    print("Relevant elements", relevant_elements)
    print(f"Index of relevant elements: {weight_lookup_index(relevant_elements)}")
    print(len(n_tuple.lookup_table))  # at C = 15 and n = 4 matches the paper network 17* 15*4 = 860 625
    print(f"Weight at the index: {n_tuple.lookup_table[weight_lookup_index(relevant_elements)]}")
    board_value = state_value_function([n_tuple,], BOARD)
    print(board_value)


