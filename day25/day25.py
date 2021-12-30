import os
from copy import deepcopy

from testfixtures import ShouldRaise, compare


def string_to_state(input_string):
    input_string = input_string.strip()
    return [ [c for c in line] for line in input_string.split('\n') ]


def load_day25_data(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath) as f:
        return string_to_state(f.read())


def state_to_string(state):
    result = ""
    for row in state:
        result += ''.join(row)
        result += '\n'
    return result

def do_iterate(state):
    row_count = len(state)
    col_count = len(state[0])

    east = '>'
    result = deepcopy(state)
    for row_index, row in enumerate(state):
        for col_index, char in enumerate(row):
            next_col_index = (col_index + 1) % col_count  # wrap
            if char == east and state[row_index][next_col_index] == '.':
                result[row_index][col_index] = '.'
                result[row_index][next_col_index] = east

    south = 'v'
    intermediate_state = deepcopy(result)
    for row_index, row in enumerate(intermediate_state):
        for col_index, char in enumerate(row):
            next_row_index = (row_index + 1) % row_count  # wrap
            if char == south and intermediate_state[next_row_index][col_index] == '.':
                result[row_index][col_index] = '.'
                result[next_row_index][col_index] = south
    return result

def find_stable_state(state):
    count = 1
    start_of_turn = deepcopy(state)
    while True:
        result = do_iterate(start_of_turn)
        try:
            compare(start_of_turn, result)
        except AssertionError:
            start_of_turn = result
            count += 1
            continue
        else:
            return count

if __name__ == '__main__':
    initial_state = load_day25_data("day25_real_data.txt")
    iterations = find_stable_state(initial_state)
    print(f"Everything stops after {iterations} iterations.")