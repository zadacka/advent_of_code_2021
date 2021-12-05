import os.path
from itertools import zip_longest, chain


def parse_vent_input_file(filename):
    file_path = os.path.join(os.path.dirname(__file__), filename)
    result = []
    with open(file_path) as f:
        for line in f.readlines():
            start, arrow, end = line.split()
            x1, y1 = start.split(',')
            x2, y2 = end.split(',')
            result.append({"x1": int(x1), "y1": int(y1), "x2": int(x2), "y2": int(y2)})
    return result


def generate_blank_grid(lines):
    columns = max(*(start["x1"] for start in lines), *(start["x2"] for start in lines)) + 1
    rows = max(*(start["y1"] for start in lines), *(start["y2"] for start in lines)) + 1
    return [[0] * columns for _ in range(rows)]


def print_map(test_grid):
    map = ""
    for line in test_grid:
        map += ''.join([str(c) if c != 0 else '.' for c in line])
        map += '\n'
    return map


def line_to_points(line):
    x_step = 1 if line["x2"] >= line["x1"] else -1
    y_step = 1 if line["y2"] >= line["y1"] else -1
    x_values = list(range(line["x1"], line["x2"] + x_step, x_step))
    y_values = list(range(line["y1"], line["y2"] + y_step, y_step))

    fill_value = line["x1"] if len(x_values) == 1 else line["y1"]  # a line of one value = not changing
    return [(x, y) for x, y in zip_longest(x_values, y_values, fillvalue=fill_value)]


def is_diagonal(line):
    if (line["x1"] != line["x2"]) and (line["y1"] != line["y2"]):
        return True
    return False


def add_line_to_grid(line, grid):
    for point in line_to_points(line):
        x, y = point
        grid[y][x] += 1


def generate_grid(lines, skip_diagonals=True):
    grid = generate_blank_grid(lines)
    for line in lines:
        if skip_diagonals and is_diagonal(line):
            pass
        else:
            add_line_to_grid(line, grid)
    return grid


def calculate_overlap_count(grid):
    return sum(x >= 2 for x in chain(*grid))


if __name__ == "__main__":
    input = parse_vent_input_file("day05_real_data.txt")
    grid = generate_grid(input)
    overlap = calculate_overlap_count(grid)
    print("The grid has {} points where two or more vent lines overlap".format(overlap))

    grid_with_diagonals = generate_grid(input, skip_diagonals=False)
    overlap2 = calculate_overlap_count(grid_with_diagonals)
    print("The grid has {} points where two or more vent lines overlap when we include diagonals".format(overlap2))
