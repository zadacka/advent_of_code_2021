from copy import deepcopy

from testfixtures import compare, ShouldRaise

from day11.day11 import load_day11_data, iterate_one_step, iterate, find_sync

test_data = [
    [5, 4, 8, 3, 1, 4, 3, 2, 2, 3],
    [2, 7, 4, 5, 8, 5, 4, 7, 1, 1],
    [5, 2, 6, 4, 5, 5, 6, 1, 7, 3],
    [6, 1, 4, 1, 3, 3, 6, 1, 4, 6],
    [6, 3, 5, 7, 3, 8, 5, 4, 7, 8],
    [4, 1, 6, 7, 5, 2, 4, 6, 4, 5],
    [2, 1, 7, 6, 8, 4, 1, 7, 2, 1],
    [6, 8, 8, 2, 8, 8, 1, 1, 3, 4],
    [4, 8, 4, 6, 8, 4, 8, 5, 5, 4],
    [5, 2, 8, 3, 7, 5, 1, 5, 2, 6],
]


def test_load_data():
    compare(load_day11_data("day11_test_data.txt"), expected=test_data)


def test__iterate_one_step__one_step():
    expected = [
        [6, 5, 9, 4, 2, 5, 4, 3, 3, 4],
        [3, 8, 5, 6, 9, 6, 5, 8, 2, 2],
        [6, 3, 7, 5, 6, 6, 7, 2, 8, 4],
        [7, 2, 5, 2, 4, 4, 7, 2, 5, 7],
        [7, 4, 6, 8, 4, 9, 6, 5, 8, 9],
        [5, 2, 7, 8, 6, 3, 5, 7, 5, 6],
        [3, 2, 8, 7, 9, 5, 2, 8, 3, 2],
        [7, 9, 9, 3, 9, 9, 2, 2, 4, 5],
        [5, 9, 5, 7, 9, 5, 9, 6, 6, 5],
        [6, 3, 9, 4, 8, 6, 2, 6, 3, 7],
    ]
    compare(iterate_one_step(test_data), expected=expected)


def test__iterate_one_step__three_steps():
    expected = [
        [0, 0, 5, 0, 9, 0, 0, 8, 6, 6],
        [8, 5, 0, 0, 8, 0, 0, 5, 7, 5],
        [9, 9, 0, 0, 0, 0, 0, 0, 3, 9],
        [9, 7, 0, 0, 0, 0, 0, 0, 4, 1],
        [9, 9, 3, 5, 0, 8, 0, 0, 6, 3],
        [7, 7, 1, 2, 3, 0, 0, 0, 0, 0],
        [7, 9, 1, 1, 2, 5, 0, 0, 0, 9],
        [2, 2, 1, 1, 1, 3, 0, 0, 0, 0],
        [0, 4, 2, 1, 1, 2, 5, 0, 0, 0],
        [0, 0, 2, 1, 1, 1, 9, 0, 0, 0],
    ]
    data = deepcopy(test_data)
    for _ in range(3):
        data = iterate_one_step(data)
    compare(data, expected=expected)


def test__iterate_one_step__simple():
    simple_test_data = [
        [7, 8],
        [9, 0],
    ]
    expected_1 = [
        [0, 0],
        [0, 4],
    ]
    compare(iterate_one_step(simple_test_data), expected=expected_1)


def test__iterate_one_step__100_steps():
    expected = [
        [0, 3, 9, 7, 6, 6, 6, 8, 6, 6],
        [0, 7, 4, 9, 7, 6, 6, 9, 1, 8],
        [0, 0, 5, 3, 9, 7, 6, 9, 3, 3],
        [0, 0, 0, 4, 2, 9, 7, 8, 2, 2],
        [0, 0, 0, 4, 2, 2, 9, 8, 9, 2],
        [0, 0, 5, 3, 2, 2, 2, 8, 7, 7],
        [0, 5, 3, 2, 2, 2, 2, 9, 6, 6],
        [9, 3, 2, 2, 2, 2, 8, 9, 6, 6],
        [7, 9, 2, 2, 2, 8, 6, 8, 6, 6],
        [6, 7, 8, 9, 9, 9, 8, 7, 6, 6],
    ]
    data = deepcopy(test_data)
    for _ in range(100):
        data = iterate_one_step(data)
    compare(data, expected=expected)
    compare(data, expected=expected)

def test__count_flashes():
    compare(iterate(test_data, 100), expected=1656)

def test_find_sync():
    compare(find_sync(test_data), expected=195)