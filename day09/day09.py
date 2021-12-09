import os.path
from termcolor import cprint


def load_day09_data(filename):
    result = []
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath) as f:
        for line in f.read().split('\n'):
            row = [int(character) for character in line]
            result.append(row)
    return result


def get_value(row, col, array):
    if row < 0 or col < 0 or row >= len(array) or col >= len(array[0]):
        return None
    else:
        return array[row][col]


def is_minima(row, col, array):
    value = array[row][col]
    above = get_value(row - 1, col, array)
    left = get_value(row, col - 1, array)
    right = get_value(row, col + 1, array)
    below = get_value(row + 1, col, array)
    for neighbour in (above, left, right, below):
        if neighbour is not None and neighbour <= value:
            return False
    return True


def find_minima(array):
    minima = {}
    for row_index, row in enumerate(array):
        for column_index, entry in enumerate(row):
            if is_minima(row_index, column_index, array):
                minima[(row_index, column_index)] = entry
    return minima


def calculate_risk_level(array):
    minima = find_minima(array)
    return sum(minima.values()) + len(minima)


def get_neighbours(location):
    row, col = location
    return (row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)


def grow_basin(locations_in_basin, array):
    new_locations = set()
    for location in locations_in_basin:
        neighbours = get_neighbours(location)
        for neighbour in neighbours:
            if neighbour not in locations_in_basin:
                neighbour_value = get_value(*neighbour, array)
                if neighbour_value is not None and neighbour_value != 9:
                    new_locations.add(neighbour)
    return new_locations


def find_basin(start, array):
    locations_in_basin = {start}
    while True:
        new_locations = grow_basin(locations_in_basin, array)
        if new_locations:
            locations_in_basin.update(new_locations)
        else:
            return locations_in_basin


def find_all_basins(array):
    all_basins = []
    minima = find_minima(array)
    for minimum in minima:
        basin = find_basin(minimum, array)
        if basin not in all_basins:
            all_basins.append(basin)
    return all_basins


def find_largest_three_basins_size(array):
    all_basins = find_all_basins(array)
    basins_by_size = sorted(all_basins, key=len, reverse=True)
    return len(basins_by_size[0]) * len(basins_by_size[1]) * len(basins_by_size[2])

def print_minima_in_color(array):
    minima = find_minima(array)
    for row_index, row in enumerate(array):
        for column_index, value in enumerate(row):
            if (row_index, column_index) in minima:
                cprint(value, 'green', 'on_red', end='')
            else:
                print(value, end='')
        print('')


if __name__ == "__main__":
    array = load_day09_data("day09_real_data.txt")
    print("The risk level for the floor map is {}".format(calculate_risk_level(array)))

    print("The size of the largest three basins is {}".format(find_largest_three_basins_size(array)))
