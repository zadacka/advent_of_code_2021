import os

import testfixtures

from day01.day01 import count_increases, make_sliding_window


def test_make_sliding_window():
    test_input = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    expected = [607, 618, 618, 617, 647, 716, 769, 792]
    testfixtures.compare(expected, make_sliding_window(test_input))


def test_count_depth():
    test_file = os.path.join(os.path.dirname(__file__), "day01_test_data.txt")
    with open(test_file) as f:
        depths = f.readlines()
    actual = count_increases(depths)
    testfixtures.compare(actual, 7)
