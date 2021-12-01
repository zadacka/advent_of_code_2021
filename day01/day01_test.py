import os

import pytest
import testfixtures

from day01.day01 import count_increases, make_sliding_window


def test_make_sliding_window():
    test_input = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    expected = [607, 618, 618, 617, 647, 716, 769, 792]
    testfixtures.compare(expected, make_sliding_window(test_input))


def test_count_increases():
    test_file = os.path.join(os.path.dirname(__file__), "day01_test_data.txt")
    with open(test_file) as f:
        depths = [int(x) for x in f.readlines()]
    actual = count_increases(depths)
    testfixtures.compare(actual, 7)


def test_count_increases_guards_agains_string_sorting_issues():
    """ Ensure that count_increases() does NOT accept non-numerics
        else you run into the legographic sorting issue where "2" > "10"
    """
    with pytest.raises(AssertionError):
        _ = count_increases(["2", "10"])
