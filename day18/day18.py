import copy
import json
import math
import os
from copy import deepcopy
from itertools import permutations

def load_day18_data(filename):
    """ Open a file with content like:
    [[[0, [5, 8]], [[1, 7], [9, 6]]], [[4, [1, 2]], [[1, 4], 2]]],
    [[[5, [2, 8]], 4], [5, [[9, 9], 0]]],
    ... and return a list of all the lists.
    """
    filepath = os.path.join(os.path.dirname(__file__), filename)
    result = []
    with open(filepath) as f:
        for line in f.readlines():
            result.append(json.loads(line))
    return result

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
    assignment = load_day18_data("day18_real_data.txt")
    total = final_sum(deepcopy(assignment))
    total_magnitude = calculate_magnitude(total)
    print(f"The assignment has a magnitude of {total_magnitude}")

    max_value = find_largest(deepcopy(assignment))
    print(f"The max possible magnitude is {max_value}")
