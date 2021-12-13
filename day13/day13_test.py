from testfixtures import compare

from day13.day13 import load_instructions, make_dot_array, draw_dots, fold, count_dots

test_dots = [
    (6, 10),
    (0, 14),
    (9, 10),
    (0, 3),
    (10, 4),
    (4, 11),
    (6, 0),
    (6, 12),
    (4, 1),
    (0, 13),
    (10, 12),
    (3, 4),
    (3, 0),
    (8, 4),
    (1, 10),
    (2, 14),
    (8, 10),
    (9, 0),
]
test_folds = [
    ("y", 7),
    ("x", 5),
]
test_dot_array = [
    [".", ".", ".", "#", ".", ".", "#", ".", ".", "#", ".", ],
    [".", ".", ".", ".", "#", ".", ".", ".", ".", ".", ".", ],
    [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ],
    ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ],
    [".", ".", ".", "#", ".", ".", ".", ".", "#", ".", "#", ],
    [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ],
    [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ],
    [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ],
    [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ],
    [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ],
    [".", "#", ".", ".", ".", ".", "#", ".", "#", "#", ".", ],
    [".", ".", ".", ".", "#", ".", ".", ".", ".", ".", ".", ],
    [".", ".", ".", ".", ".", ".", "#", ".", ".", ".", "#", ],
    ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ],
    ["#", ".", "#", ".", ".", ".", ".", ".", ".", ".", ".", ],
]


def test_load_instructions():
    expected = test_dots, test_folds
    compare(load_instructions("day13_test_data.txt"), expected=expected)


def test_make_dot_array():
    compare(make_dot_array(test_dots), expected=test_dot_array)


def test_draw_dots():
    expected = """\
...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........
"""
    compare(draw_dots(test_dot_array), expected=expected)


def test_do_fold():
    array = make_dot_array(test_dots)
    folded_array = fold(array, "y", 7)
    first_fold = """\
#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
...........
"""
    compare(draw_dots(folded_array), expected=first_fold)
    folded_array = fold(folded_array, "x", 5)
    second_fold = """\
#####
#...#
#...#
#...#
#####
.....
.....
"""
    compare(draw_dots(folded_array), expected=second_fold)


def test_count_dots():
    compare(count_dots(test_dot_array), expected=18)

def test_integration():
    dots, instructions = load_instructions("day13_test_data.txt")
    array = make_dot_array(dots)
    for axis, fold_position in instructions:
        array = fold(array, axis, fold_position)
    compare(count_dots(array), expected=16)


