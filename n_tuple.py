from dataclasses import dataclass
from typing import Tuple, List
import numpy as np

C = 15  # := maximum_power_of_two_allowed - 1
BOARD = np.array(
    [
        [2, 2, 4, 4],
        [2, 0, 4, 4],
        [0, 4, 4, 2],
        [2, 8, 4, 4],
    ]
)

class N_tuple():
    def __init__(self, locations: List[Tuple[int, int]], c: int = C, tuple_length: int = 4):
        self.locations = locations  # predetermined sequence of board locations
        rng = np.random.default_rng()
        self.lookup_size = C**tuple_length
        self.lookup_table = np.random.rand(self.lookup_size)

def weight_lookup_index(board_elements: np.ndarray, c: int = C, n: int = 4):
    # we encode board values ("2", "16") into their powers of 2 (1, 4); then convert to base-c from base-10

    assert isinstance(board_elements, np.ndarray), "board values must be a NumPy ndarray"

    encoded_board_elements = np.zeros_like(board_elements)
    non_zero_mask = board_elements != 0
    encoded_board_elements[non_zero_mask] = np.log2(board_elements[non_zero_mask]).astype(np.int32)
    weight_index = 0
    for tuple_element_position in range(0, n):
        value = encoded_board_elements[tuple_element_position]
        weight_index += value * (c ** (tuple_element_position))
    return weight_index

# n-tuple network of m tuples implements a function approximator f(s) :=
def state_value_function(tuple_network: List[N_tuple], board_state: np.ndarray):
    state_value = 0
    for _tuple in tuple_network:
        rows, cols = zip(*_tuple.locations)
        relevant_elements = board_state[rows, cols]
        combination_weight = _tuple.lookup_table[weight_lookup_index(relevant_elements)]
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


