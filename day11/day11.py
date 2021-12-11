import os.path
from copy import deepcopy
from itertools import chain


class AdventSyntaxError(Exception):
    def __init__(self, bad_character, *args: object) -> None:
        super().__init__(*args)
        self.bad_character = bad_character


def load_day11_data(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    result = []
    with open(filepath) as f:
        for line in f.readlines():
            this_line = [int(c) for c in line.strip()]
            result.append(this_line)
    return result


def neighbours(row_index, column_index):
    neighbours = (
        (row_index - 1, column_index - 1),
        (row_index - 1, column_index),
        (row_index - 1, column_index + 1),
        (row_index, column_index - 1),
        (row_index, column_index + 1),
        (row_index + 1, column_index - 1),
        (row_index + 1, column_index),
        (row_index + 1, column_index + 1),
    )
    return neighbours


def increase_neighbours(row_index, column_index, data):
    local_data = deepcopy(data)
    max_row = len(local_data)
    max_col = len(local_data[0])
    for r, c in neighbours(row_index, column_index):
        if (0 <= r < max_row) and (0 <= c < max_col):
            if local_data[r][c] != 0:  # can only flash once per cycle
                local_data[r][c] += 1
    return local_data


def iterate_one_step(data):
    local_data = deepcopy(data)

    # increase everything by 1
    local_data = [[value + 1 for value in row] for row in local_data]

    while any(value > 9 for value in chain(*local_data)):
        for row_index in range(len(local_data)):
            for column_index in range(len(local_data[0])):
                if local_data[row_index][column_index] > 9:
                    local_data[row_index][column_index] = 0
                    local_data = increase_neighbours(row_index, column_index, local_data)
    return local_data


def iterate(data, steps):
    flashes = 0
    local_data = deepcopy(data)
    for step in range(steps):
        local_data = iterate_one_step(local_data)
        flashes_this_cycle = sum(c == 0 for row in local_data for c in row)
        flashes += flashes_this_cycle
    return flashes


def find_sync(data):
    cycles = 0
    octopi = len(data) * len(data[0])
    while True:
        data = iterate_one_step(data)
        cycles += 1
        if sum(c == 0 for row in data for c in row) == octopi:
            return cycles


if __name__ == "__main__":
    data = load_day11_data("day11_real_data.txt")
    print("After 100 cycles there are {} flashes".format(iterate(data, 100)))
    print("The first sync happens after {} cycles".format(find_sync(data)))
