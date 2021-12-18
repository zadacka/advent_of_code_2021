import math
from copy import deepcopy

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


def find_explode_index(candidate, index_so_far=0, depth=0):
    if depth == 4:  # termination condition - we have found the 'absolute' index where depth == 4
        return index_so_far

    for index, element in enumerate(candidate):
        if isinstance(element, list):
            location = find_explode_index(element, index_so_far + index, depth + 1)
            if location is not None:
                return location
        index_so_far += 1


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
            candidate[local_index] = [math.floor(element/2.0), math.ceil(element/2.0)]

        if isinstance(element, list):
            result = split_at_index(element, target_index, global_index)
            global_index = result  # we already count the list as one element
        else:
            global_index += 1
    return global_index


def find_at_index(candidate, target_index, ):
    """ get the left/right index pair to be exploded from index with global_index == target_index"""
    flat = list(iter_flatten(candidate))
    return flat[target_index:target_index+2]


def explode(candidate):
    """ Exploding pairs will always consist of two regular numbers.
    To explode a pair,
    * the pair's left value is added to the first regular number to the left of the exploding pair (if any),
    * the pair's right value is added to the first regular number to the right of the exploding pair (if any).
    * Then, the entire exploding pair is replaced with the regular number 0.
    """
    explode_index = find_explode_index(candidate)
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
