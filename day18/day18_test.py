from testfixtures import compare

from day18.day18 import snailfish_add, can_explode, can_split, explode, split, add_at_index, find_at_index, \
    clear_at_index


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


def test__add_at_index():
    initial = [[[[[0, 1], 2], 3], [4, [[5, 6], 7]]], [8, 9]]
    add_at_index(initial, target_index=0, to_add=1)
    compare(initial, expected=[[[[[1, 1], 2], 3], [4, [[5, 6], 7]]], [8, 9]])

    initial = [[[[[0, 1], 2], 3], [4, [[5, 6], 7]]], [8, 9]]
    add_at_index(initial, target_index=1, to_add=1)
    compare(initial, expected=[[[[[0, 2], 2], 3], [4, [[5, 6], 7]]], [8, 9]])

    initial = [[[[[0, 1], 2], 3], [4, [[5, 6], 7]]], [8, 9]]
    add_at_index(initial, target_index=2, to_add=1)
    compare(initial, expected=[[[[[0, 1], 3], 3], [4, [[5, 6], 7]]], [8, 9]])

    initial = [[[[[0, 1], 2], 3], [4, [[5, 6], 7]]], [8, 9]]
    add_at_index(initial, target_index=3, to_add=1)
    compare(initial, expected=[[[[[0, 1], 2], 4], [4, [[5, 6], 7]]], [8, 9]])

    initial = [[[[[0, 1], 2], 3], [4, [[5, 6], 7]]], [8, 9]]
    add_at_index(initial, target_index=4, to_add=1)
    compare(initial, expected=[[[[[0, 1], 2], 3], [5, [[5, 6], 7]]], [8, 9]])

    initial = [[[[[0, 1], 2], 3], [4, [[5, 6], 7]]], [8, 9]]
    add_at_index(initial, target_index=5, to_add=1)
    compare(initial, expected=[[[[[0, 1], 2], 3], [4, [[6, 6], 7]]], [8, 9]])

    initial = [[[[[0, 1], 2], 3], [4, [[5, 6], 7]]], [8, 9]]
    add_at_index(initial, target_index=6, to_add=1)
    compare(initial, expected=[[[[[0, 1], 2], 3], [4, [[5, 7], 7]]], [8, 9]])

    initial = [[[[[0, 1], 2], 3], [4, [[5, 6], 7]]], [8, 9]]
    add_at_index(initial, target_index=7, to_add=1)
    compare(initial, expected=[[[[[0, 1], 2], 3], [4, [[5, 6], 8]]], [8, 9]])

    initial = [[[[[0, 1], 2], 3], [4, [[5, 6], 7]]], [8, 9]]
    add_at_index(initial, target_index=8, to_add=1)
    compare(initial, expected=[[[[[0, 1], 2], 3], [4, [[5, 6], 7]]], [9, 9]])

    initial = [[[[[0, 1], 2], 3], [4, [[5, 6], 7]]], [8, 9]]
    add_at_index(initial, target_index=9, to_add=1)
    compare(initial, expected=[[[[[0, 1], 2], 3], [4, [[5, 6], 7]]], [8, 10]])


def test__find_at_index():
    initial = [[[[[0, 1], 2], 3], [4, [[5, 6], 7]]], [8, 9]]
    compare(find_at_index(initial, 0), expected=(0, 1))
    compare(find_at_index(initial, 5), expected=(5, 6))
    compare(find_at_index(initial, 8), expected=(8, 9))


def test__clear_at_index():
    initial = [[[[[0, 1], 2], 3], [4, [[5, 6], 7]]], [8, 9]]
    clear_at_index(initial, target_index=0)
    compare(initial, expected=[[[[0, 2], 3], [4, [[5, 6], 7]]], [8, 9]])

    initial = [[[[[0, 1], 2], 3], [4, [[5, 6], 7]]], [8, 9]]
    clear_at_index(initial, target_index=5)
    compare(initial, expected=[[[[[0, 1], 2], 3], [4, [0, 7]]], [8, 9]])

    initial = [[[[[0, 1], 2], 3], [4, [[5, 6], 7]]], [8, 9]]
    clear_at_index(initial, target_index=8)
    compare(initial, expected=[[[[[0, 1], 2], 3], [4, [[5, 6], 7]]], 0])


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
