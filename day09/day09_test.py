from testfixtures import compare

from day09.day09 import load_day09_data, find_minima, calculate_risk_level, find_basin, find_all_basins, \
    find_largest_three_basins_size

test_data = [[2, 1, 9, 9, 9, 4, 3, 2, 1, 0],
             [3, 9, 8, 7, 8, 9, 4, 9, 2, 1],
             [9, 8, 5, 6, 7, 8, 9, 8, 9, 2],
             [8, 7, 6, 7, 8, 9, 6, 7, 8, 9],
             [9, 8, 9, 9, 9, 6, 5, 6, 7, 8]]

test_data2 = [[9, 9],
              [9, 0]]


def test_load_data():
    compare(load_day09_data("day09_test_data.txt"), expected=test_data)


def test_find_minima():
    expected = {(0, 1): 1, (0, 9): 0, (2, 2): 5, (4, 6): 5}
    compare(find_minima(test_data), expected)


def test_find_minima__check_equal_neighbours_do_not_count_as_minima():
    expected = {(1, 1): 0}
    compare(find_minima(test_data2), expected)


def test_calculate_risk_level():
    compare(calculate_risk_level(test_data), expected=15)


def test_find_basin():
    array = test_data
    start = (0, 1)
    basin = find_basin(start, array)
    compare(basin, expected={(0, 0), (0, 1), (1, 0)})

def test_find_all_basins():
    array = test_data
    all_basins = find_all_basins(array)
    compare(len(all_basins), expected=4)

def test_find_largest_three_basins_size():
    compare(find_largest_three_basins_size(test_data), expected=1134)