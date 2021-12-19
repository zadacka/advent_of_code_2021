from copy import deepcopy

from testfixtures import compare

from day18.day18 import snailfish_add, can_explode, can_split, explode, split, add_at_index, find_at_index, \
    clear_at_index, final_sum, find_explode_index, calculate_magnitude, find_largest


def test__addition():
    expected = [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
    compare(snailfish_add([[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]), expected=expected)


def test__can_explode():
    compare(can_explode([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]), expected=True)
    compare(can_explode([[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]]), expected=True)
    compare(can_explode([[[[0, 7], 4], [15, [0, 13]]], [1, 1]]), expected=False)


def test__find_explode_index():
    result = [None]
    find_explode_index([[[[[9, 8], 1], 2], 3], 4], result=result)
    compare(result[0], expected=0)

    result = [None]
    find_explode_index([7, [6, [5, [4, [3, 2]]]]], result=result)
    compare(result[0], expected=4)

    result = [None]
    find_explode_index([[6, [5, [4, [3, 2]]]], 1], result=result)
    compare(result[0], expected=3)

    result = [None]
    find_explode_index([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]], result=result)
    compare(result[0], expected=3)

    result = [None]
    find_explode_index([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]], result=result)
    compare(result[0], expected=7)


def test__explode():
    compare(explode([[[[[9, 8], 1], 2], 3], 4]), expected=[[[[0, 9], 2], 3], 4])
    compare(explode([7, [6, [5, [4, [3, 2]]]]]), expected=[7, [6, [5, [7, 0]]]])
    compare(explode([[6, [5, [4, [3, 2]]]], 1]), expected=[[6, [5, [7, 0]]], 3])
    compare(explode([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]), expected=[[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]])
    compare(explode([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]), expected=[[3, [2, [8, 0]]], [9, [5, [7, 0]]]])


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


def test__split():
    compare(
        split([[[[[11, 1], 2], 3], [4, [[5, 6], 7]]], [8, 9]]),
        expected=[[[[[[5, 6], 1], 2], 3], [4, [[5, 6], 7]]], [8, 9]]
    )

    compare(
        split([[[[[0, 1], 2], 3], [11, [[5, 6], 7]]], [8, 9]]),
        expected=[[[[[0, 1], 2], 3], [[5, 6], [[5, 6], 7]]], [8, 9]]
    )

    compare(
        split([[[[[0, 1], 2], 3], [4, [[5, 6], 7]]], [8, 11]]),
        expected=[[[[[0, 1], 2], 3], [4, [[5, 6], 7]]], [8, [5, 6]]]
    )


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
    v1 = [[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]
    v2 = [[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]]
    compare(explode(v1), expected=v2)
    v3 = [[[[0, 7], 4], [15, [0, 13]]], [1, 1]]
    compare(explode(v2), expected=v3)
    v4 = [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]
    compare(split(v3), expected=v4)
    v5 = [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]
    compare(split(v4), expected=v5)
    v6 = [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
    compare(explode(v5), expected=v6)


def test_various():
    compare(final_sum([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]), expected=[[[[1, 1], [2, 2]], [3, 3]], [4, 4]])
    compare(final_sum([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]), expected=[[[[3, 0], [5, 3]], [4, 4]], [5, 5]])
    compare(final_sum([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]]), expected=[[[[5, 0], [7, 4]], [5, 5]], [6, 6]])


def test_calculate_magnitude():
    compare(calculate_magnitude([[1, 2], [[3, 4], 5]]), expected=143)
    compare(calculate_magnitude([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]), expected=1384)
    compare(calculate_magnitude([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]), expected=445)
    compare(calculate_magnitude([[[[3, 0], [5, 3]], [4, 4]], [5, 5]]), expected=791)
    compare(calculate_magnitude([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]), expected=1137)
    compare(calculate_magnitude([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]), expected=3488)


test_assignment = [
    [[[0, [5, 8]], [[1, 7], [9, 6]]], [[4, [1, 2]], [[1, 4], 2]]],
    [[[5, [2, 8]], 4], [5, [[9, 9], 0]]],
    [6, [[[6, 2], [5, 6]], [[7, 6], [4, 7]]]],
    [[[6, [0, 7]], [0, 9]], [4, [9, [9, 0]]]],
    [[[7, [6, 4]], [3, [1, 3]]], [[[5, 5], 1], 9]],
    [[6, [[7, 3], [3, 2]]], [[[3, 8], [5, 7]], 4]],
    [[[[5, 4], [7, 7]], 8], [[8, 3], 8]],
    [[9, 3], [[9, 9], [6, [4, 9]]]],
    [[2, [[7, 7], 7]], [[5, 8], [[9, 3], [0, 2]]]],
    [[[[5, 2], 5], [8, [3, 7]]], [[5, [7, 5]], [4, 4]]],
]


def test__sample_homework():
    compare(final_sum(deepcopy(test_assignment)), [[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]])
    compare(calculate_magnitude([[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]]),
            expected=4140)


def test_find_largest():
    max_value = find_largest(test_assignment)
    compare(max_value, expected=3993)
