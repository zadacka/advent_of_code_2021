from testfixtures import compare

from day18.day18 import snailfish_add, can_explode, can_split, explode, split


def test__addition():
    expected = [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
    actual = snailfish_add([[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1])
    compare(actual, expected=expected)


def test__can_explode():
    compare(can_explode([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]), expected=True)
    compare(can_explode([[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]]), expected=True)
    compare(can_explode([[[[0, 7], 4], [15, [0, 13]]], [1, 1]]), expected=False)


def test__can_split():
    compare(can_split([[[[0, 7], 4], [15, [0, 13]]], [1, 1]]), expected=True)
    compare(can_split([[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]), expected=True)
    compare(can_split([[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]), expected=False)


def test__various_operations():
    v1 = [[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]  #
    v2 = [[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]]  # after explode
    compare(explode(v1), expected=v2)
    v3 = [[[[0, 7], 4], [15, [0, 13]]], [1, 1]]  # after explode
    compare(explode(v2), expected=v3)
    v4 = [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]  # after split
    compare(split(v3), expected=v4)
    v5 = [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]  # after split
    compare(split(v4), expected=v5)
    v6 = [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]  # after explode
    compare(explode(v5), expected=v6)
