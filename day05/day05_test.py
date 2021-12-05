from textwrap import dedent

from testfixtures import compare

from day05.day05 import parse_vent_input_file, line_to_points, print_map, generate_grid, calculate_overlap_count

test_lines = [
    {"x1": 0, "y1": 9, "x2": 5, "y2": 9},
    {"x1": 8, "y1": 0, "x2": 0, "y2": 8},
    {"x1": 9, "y1": 4, "x2": 3, "y2": 4},
    {"x1": 2, "y1": 2, "x2": 2, "y2": 1},
    {"x1": 7, "y1": 0, "x2": 7, "y2": 4},
    {"x1": 6, "y1": 4, "x2": 2, "y2": 0},
    {"x1": 0, "y1": 9, "x2": 2, "y2": 9},
    {"x1": 3, "y1": 4, "x2": 1, "y2": 4},
    {"x1": 0, "y1": 0, "x2": 8, "y2": 8},
    {"x1": 5, "y1": 5, "x2": 8, "y2": 2},
]

test_grid = [
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 2, 1, 1, 1, 2, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 1, 1, 1, 0, 0, 0, 0],
]


def test_parse_vent_input_file():
    actual = parse_vent_input_file("day05_test_data.txt")
    compare(test_lines, actual=actual)


def test_line_to_points():
    point = line_to_points({"x1": 0, "y1": 0, "x2": 0, "y2": 0})
    compare(point, expected=[(0, 0)])

    vertical = line_to_points({"x1": 0, "y1": 0, "x2": 0, "y2": 1})
    compare(vertical, expected=[(0, 0), (0, 1)])

    horizontal = line_to_points({"x1": 0, "y1": 0, "x2": 1, "y2": 0})
    compare(horizontal, expected=[(0, 0), (1, 0)])

    diagonal1 = line_to_points({"x1": 0, "y1": 0, "x2": 1, "y2": 1})
    compare(diagonal1, expected=[(0, 0), (1, 1)])

    diagonal2 = line_to_points({"x1": 0, "y1": 1, "x2": 1, "y2": 0})
    compare(diagonal2, expected=[(0, 1), (1, 0)])


def test_generate_simple_grid():
    test_lines = [
        {"x1": 0, "y1": 0, "x2": 2, "y2": 0},
        {"x1": 0, "y1": 2, "x2": 2, "y2": 2},
        {"x1": 0, "y1": 0, "x2": 0, "y2": 2},
    ]
    expected = [
        [2, 1, 1],
        [1, 0, 0],
        [2, 1, 1],
    ]
    compare(expected, actual=generate_grid(test_lines))


def test_generate_grid():
    compare(test_grid, actual=generate_grid(test_lines))


def test_print_map():
    expected = dedent("""\
    .......1..
    ..1....1..
    ..1....1..
    .......1..
    .112111211
    ..........
    ..........
    ..........
    ..........
    222111....
    """)
    compare(expected, actual=(print_map(test_grid)))


def test_calculate_overlap_count():
    compare(5, actual=calculate_overlap_count(test_grid))

def test_part_two():
    expected = dedent("""\
        1.1....11.
        .111...2..
        ..2.1.111.
        ...1.2.2..
        .112313211
        ...1.2....
        ..1...1...
        .1.....1..
        1.......1.
        222111....
    """)
    grid = generate_grid(test_lines, skip_diagonals=False)
    compare(expected, actual=(print_map(grid)))