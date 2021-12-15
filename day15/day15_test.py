from testfixtures import compare

from day15.day15 import load_risks, get_path, score_path

test_risks = [
    [1, 1, 6, 3, 7, 5, 1, 7, 4, 2, ],
    [1, 3, 8, 1, 3, 7, 3, 6, 7, 2, ],
    [2, 1, 3, 6, 5, 1, 1, 3, 2, 8, ],
    [3, 6, 9, 4, 9, 3, 1, 5, 6, 9, ],
    [7, 4, 6, 3, 4, 1, 7, 1, 1, 1, ],
    [1, 3, 1, 9, 1, 2, 8, 1, 3, 7, ],
    [1, 3, 5, 9, 9, 1, 2, 4, 2, 1, ],
    [3, 1, 2, 5, 4, 2, 1, 6, 3, 9, ],
    [1, 2, 9, 3, 1, 3, 8, 5, 2, 1, ],
    [2, 3, 1, 1, 9, 4, 4, 5, 8, 1, ],
]

test_shortest_path_with_diagonals = [
    (0, 0),
    (1, 0),
    (2, 1),
    (2, 2),
    (1, 3),
    (1, 4),
    (2, 5),
    (3, 6),
    (4, 7),
    (5, 7),
    (6, 8),
    (7, 8),
    (8, 9),
    (9, 9),
]

test_shortest_path = [
    (0, 0),
    (1, 0),
    (2, 0),
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 6),
    (3, 6),
    (3, 7),
    (4, 7),
    (5, 7),
    (5, 8),
    (6, 8),
    (7, 8),
    (8, 8),
    (8, 9),
    (9, 9),
]


def test_load_risks():
    compare(load_risks("day15_test_data.txt"), expected=test_risks)


def test_find_path():
    path = get_path(test_risks)
    compare(path, expected=test_shortest_path)


def test_score_shortest_path():
    compare(score_path(test_shortest_path, test_risks), expected=40)
