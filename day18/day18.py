import copy
import math
from copy import deepcopy
from itertools import permutations


def iter_flatten(iterable):
    """ stolen - credit goes to http://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html """
    it = iter(iterable)
    for e in it:
        if isinstance(e, (list, tuple)):
            for f in iter_flatten(e):
                yield f
        else:
            yield e


def can_explode(candidate):
    """If any pair is nested inside four pairs, the leftmost such pair explodes. """

    def depth(input_list):
        if isinstance(input_list, list):
            return 1 + max(depth(item) for item in input_list)
        else:
            return 0

    return depth(candidate) > 4


def can_split(candidate):
    """If any regular number is 10 or greater, the leftmost such regular number splits. """

    def recursive_max(input_list):
        if isinstance(input_list, list):
            return max(recursive_max(item) for item in input_list)
        else:
            return input_list

    return recursive_max(candidate) >= 10


def find_explode_index(candidate, global_index=0, depth=0, result=None):
    if depth == 4 and result[0] is None:  # termination condition hit for the first time
        result[0] = global_index

    for element in candidate:
        if isinstance(element, list):
            global_index = find_explode_index(element, global_index, depth + 1, result=result)
        else:
            global_index += 1

    return global_index


def element_is_two_int_list(e):
    return isinstance(e, list) and len(e) == 2 and isinstance(e[0], int) and isinstance(e[1], int)


def clear_at_index(candidate, target_index, global_index=0):
    for index, element in enumerate(candidate):
        if global_index == target_index and element_is_two_int_list(element):
            candidate[index] = 0

        if isinstance(element, list):
            global_index = clear_at_index(element, target_index, global_index)
        else:
            global_index += 1
    return global_index


def add_at_index(candidate, target_index, to_add, global_index=0):
    for local_index, element in enumerate(candidate):
        if global_index == target_index and isinstance(element, int):
            candidate[local_index] += to_add

        if isinstance(element, list):
            result = add_at_index(element, target_index, to_add, global_index)
            global_index = result  # we already count the list as one element
        else:
            global_index += 1
    return global_index


def split_at_index(candidate, target_index, global_index=0):
    for local_index, element in enumerate(candidate):
        if global_index == target_index and isinstance(element, int):
            candidate[local_index] = [math.floor(element / 2.0), math.ceil(element / 2.0)]

        if isinstance(element, list):
            result = split_at_index(element, target_index, global_index)
            global_index = result  # we already count the list as one element
        else:
            global_index += 1
    return global_index


def find_at_index(candidate, target_index, ):
    """ get the left/right index pair to be exploded from index with global_index == target_index"""
    flat = list(iter_flatten(candidate))
    flat.append(0)  # in the event that we 'explode' off the end of a list - placeholder zero (not used)
    return flat[target_index:target_index + 2]


def explode(candidate):
    """ Exploding pairs will always consist of two regular numbers.
    To explode a pair,
    * the pair's left value is added to the first regular number to the left of the exploding pair (if any),
    * the pair's right value is added to the first regular number to the right of the exploding pair (if any).
    * Then, the entire exploding pair is replaced with the regular number 0.
    """
    updated = [None]
    find_explode_index(candidate, result=updated)
    explode_index = updated[0]
    left, right = find_at_index(candidate, explode_index)
    clear_at_index(candidate, explode_index)
    add_at_index(candidate, explode_index - 1, left)
    add_at_index(candidate, explode_index + 1, right)
    return candidate


def find_split_index(candidate):
    flat = iter_flatten(candidate)

    big_values = []
    for i, v in enumerate(flat):
        if v >= 10:
            big_values.append(i)
    return big_values[0]


def split(candidate):
    local_copy = deepcopy(candidate)
    split_index = find_split_index(local_copy)
    split_at_index(local_copy, split_index)
    return local_copy


def snailfish_reduce(candidate):
    while True:
        if can_explode(candidate):
            candidate = explode(candidate)
        elif can_split(candidate):
            candidate = split(candidate)
        else:
            return candidate


def snailfish_add(first, second):
    return snailfish_reduce([first] + [second])


def final_sum(list):
    total = None
    for num in list:
        if total is None:
            total = num
        else:
            total = snailfish_add(total, num)
    return total


def magnitude(two_int_list):
    left, right = two_int_list
    return (3 * left) + (2 * right)


def _calculate_magnitude(sailfish_number):
    for index, element in enumerate(sailfish_number):
        if element_is_two_int_list(element):
            sailfish_number[index] = magnitude(element)
        elif isinstance(element, list):
            _calculate_magnitude(element)
        else:
            pass


def calculate_magnitude(sailfish_number):
    local_number = copy.deepcopy(sailfish_number)
    while True:
        _calculate_magnitude(local_number)
        if element_is_two_int_list(local_number):
            return magnitude(local_number)


def find_largest(assignment):
    results = []
    for A, B in permutations(assignment, 2):
        result = calculate_magnitude(snailfish_add(deepcopy(A), deepcopy(B)))
        results.append(result)
    return max(results)


if __name__ == '__main__':
    assignment = [
        [[[[0, 6], [8, 7]], [2, 3]], [3, [[6, 5], [0, 0]]]],
        [[2, [9, [4, 9]]], [[[3, 0], 4], [2, [4, 7]]]],
        [[[4, [5, 2]], [1, [9, 7]]], [[2, 4], [[4, 5], 4]]],
        [[[[6, 7], 8], [[6, 6], 3]], [6, [7, [4, 9]]]],
        [[[[5, 4], [7, 4]], [8, [2, 3]]], [[[9, 7], 6], [2, [4, 7]]]],
        [[[[2, 4], [0, 9]], 6], [[[7, 3], [5, 9]], [0, [2, 3]]]],
        [[6, [9, [2, 4]]], [[3, 0], [1, [0, 0]]]],
        [[3, 7], [3, [2, 0]]],
        [[0, [2, [4, 6]]], [8, 9]],
        [[[7, 5], [[3, 8], 5]], [[[9, 8], [4, 3]], [5, [1, 4]]]],
        [[9, [[4, 7], [7, 1]]], [[7, [8, 7]], [4, [2, 6]]]],
        [[[0, 4], 9], [[[5, 1], [3, 2]], 4]],
        [[[5, 9], 2], [8, [3, [2, 4]]]],
        [[[[2, 2], [9, 2]], [0, 7]], [[[3, 7], 3], 0]],
        [5, [[9, 1], [[6, 6], 9]]],
        [[5, [1, [1, 7]]], [[[2, 2], [5, 2]], [2, 0]]],
        [[[[2, 0], 5], [[6, 1], [3, 1]]], 7],
        [4, [2, [3, 3]]],
        [[[[8, 3], [3, 2]], [[4, 0], 3]], [[[2, 5], 9], 4]],
        [[[6, 4], [[0, 8], [4, 9]]], [[[7, 9], 7], [[5, 5], [7, 8]]]],
        [3, 7],
        [[1, 5], [[[3, 7], [7, 1]], [[7, 4], [9, 3]]]],
        [[3, [0, [4, 4]]], [[3, 4], [[3, 1], 0]]],
        [[1, [[1, 1], [5, 1]]], [[[8, 0], 5], 7]],
        [[[[9, 2], 0], 2], [8, 5]],
        [4, [[0, [0, 9]], [2, 2]]],
        [[[4, [2, 0]], [[5, 5], [8, 2]]], [[[5, 1], [7, 7]], [0, 9]]],
        [[5, [[0, 1], [5, 9]]], [3, [8, [8, 4]]]],
        [[1, 9], [[3, [1, 0]], [4, 3]]],
        [[[1, 6], [2, 8]], [8, [9, 3]]],
        [[[3, 4], 0], [4, [8, [5, 8]]]],
        [[8, [9, 0]], [[[6, 4], [5, 5]], [8, 3]]],
        [[[[9, 1], [3, 9]], [1, [8, 0]]], [[8, [8, 5]], [[2, 2], 0]]],
        [1, [6, [6, 7]]],
        [[[5, [5, 8]], [[0, 8], 7]], [[7, 6], [[7, 6], [3, 8]]]],
        [[8, [1, [8, 6]]], [[8, 4], [[3, 3], 1]]],
        [7, [9, [5, 7]]],
        [[[8, 9], [9, 6]], [[[6, 7], [7, 4]], [2, [2, 6]]]],
        [[[2, 0], 4], [1, [6, [6, 0]]]],
        [[8, [8, [6, 1]]], [[6, 1], [[6, 5], [2, 3]]]],
        [4, [2, [[9, 6], [3, 5]]]],
        [6, [[3, 7], [6, 9]]],
        [[[[8, 6], 9], 4], [8, [5, 0]]],
        [[[[6, 6], 3], [7, [3, 9]]], 1],
        [[1, [7, 5]], [[6, 1], [0, [9, 3]]]],
        [[[3, [6, 0]], [2, 5]], [[4, 3], 0]],
        [[[[9, 2], 7], [[3, 7], 6]], [[1, [9, 1]], [[7, 1], [7, 7]]]],
        [[[[0, 7], 4], 2], [5, [[2, 1], 3]]],
        [[[1, 2], [[6, 4], [8, 6]]], [[[7, 3], 7], [[6, 1], [2, 1]]]],
        [[[[7, 6], 8], 5], [[3, 3], [[7, 3], 9]]],
        [[5, [[6, 8], 0]], [[6, [7, 1]], 2]],
        [[[4, 8], [[8, 2], [6, 5]]], [5, [5, [8, 7]]]],
        [[6, [[4, 8], [5, 4]]], [[[1, 7], 6], [6, 9]]],
        [8, [8, [3, 1]]],
        [[8, 3], [1, [5, [0, 9]]]],
        [[2, [[8, 3], [5, 1]]], [[2, [6, 1]], [[4, 0], [9, 3]]]],
        [5, 3],
        [[[5, 3], [[1, 2], [4, 6]]], [[7, 6], [[0, 3], 0]]],
        [[[6, 5], 8], [2, [8, 3]]],
        [[[8, 6], [0, 5]], [[2, 4], 5]],
        [[[1, [4, 1]], [[9, 4], 1]], 1],
        [[[8, 6], [[1, 4], [9, 3]]], [4, [[4, 4], 1]]],
        [[[2, [4, 2]], [1, 0]], 3],
        [[0, 2], [7, [7, [8, 5]]]],
        [[[9, [9, 5]], [0, [4, 8]]], [[6, [6, 7]], [[3, 3], 1]]],
        [1, [[[3, 7], [3, 2]], 3]],
        [[0, [[1, 6], 4]], [[[2, 2], [5, 9]], 2]],
        [[5, 8], [0, 9]],
        [[[[9, 4], [8, 8]], [[7, 3], [8, 1]]], [1, [7, [7, 6]]]],
        [[[[7, 6], [4, 2]], 7], [3, [[7, 5], [0, 9]]]],
        [[[5, 6], [6, 2]], [[8, 6], [9, 6]]],
        [[4, 7], [6, 9]],
        [6, [[0, [7, 7]], [1, 4]]],
        [[[[2, 7], 2], 4], [[[1, 8], [0, 3]], 3]],
        [[7, [[1, 8], [0, 1]]], [[3, 0], [[5, 0], 9]]],
        [[[[1, 8], [0, 3]], 2], [[9, 5], 1]],
        [[[[1, 2], 3], 6], [3, [[8, 3], [8, 8]]]],
        [9, [[4, 0], 2]],
        [[[[8, 5], 6], 9], [7, [9, [3, 4]]]],
        [[[[5, 8], [8, 5]], 0], 6],
        [[[[0, 8], [9, 3]], 3], [[[6, 4], 9], [[6, 8], 5]]],
        [[[[2, 9], 2], 0], [[[9, 0], [0, 7]], [[6, 3], [9, 8]]]],
        [[[0, [0, 5]], 1], 6],
        [[[1, [0, 5]], 9], [[[6, 8], [7, 4]], [1, [1, 1]]]],
        [[[6, 1], [8, 6]], [[1, [0, 8]], [[6, 7], [1, 8]]]],
        [[5, [[9, 9], 6]], [[0, 7], [[8, 2], [4, 5]]]],
        [[5, 4], [5, [[0, 7], [5, 7]]]],
        [[5, [4, 8]], [[5, [0, 7]], [8, 6]]],
        [[[[9, 5], 2], [3, [9, 6]]], [[6, 8], [3, 8]]],
        [[[[1, 4], [2, 9]], [2, 4]], [[1, 3], [[0, 4], [9, 9]]]],
        [[0, 4], [[7, [1, 4]], 2]],
        [[6, 4], [[[2, 7], 9], 2]],
        [[[[9, 6], 6], [[4, 7], [3, 7]]], [[[4, 8], 4], [[5, 2], [4, 8]]]],
        [[[[8, 8], 0], [6, 7]], [3, [0, [7, 1]]]],
        [[[0, [0, 3]], 7], [[2, 0], [6, [4, 5]]]],
        [[[[0, 4], 5], [4, [2, 6]]], [[9, 9], 7]],
        [1, [8, 8]],
        [[[4, 2], [2, [6, 6]]], 7],
        [7, [3, [4, [2, 3]]]],
        [0, 9],
    ]
    total = final_sum(deepcopy(assignment))
    total_magnitude = calculate_magnitude(total)
    print(f"The assignment has a magnitude of {total_magnitude}")

    max_value = find_largest(deepcopy(assignment))
    print(f"The max possible magnitude is {max_value}")
