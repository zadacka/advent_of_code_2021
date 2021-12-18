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


def explode(candidate):
    return candidate


def split(candidate):
    return candidate


def snailfish_reduce(candidate):
    while True:
        if can_explode(candidate):
            candidate = explode(candidate)
        elif can_split(candidate):
            candidate = split(candidate)
        else:
            return candidate


def snailfish_add(first, second):
    return snailfish_reduce(first + second)
