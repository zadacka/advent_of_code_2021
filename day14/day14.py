import collections
import os
from copy import deepcopy
from itertools import islice, zip_longest, groupby


def load_instructions(filename):
    instructions_file = os.path.join(os.path.dirname(__file__), filename)

    with open(instructions_file) as f:
        template = f.readline().strip()
        _ = f.readline()
        rules = {l[0:2]: l[-2:].strip() for l in f.readlines()}

    return template, rules


def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield ''.join(list(window))
    for x in it:
        window.append(x)
        yield ''.join(list(window))


def polymerize(template, map):
    new_elements = []
    for pair in sliding_window(template, 2):
        new_element = map[pair]
        new_elements.append(new_element)
    result = ''.join([val for pair in zip_longest(template, new_elements, fillvalue="") for val in pair])
    return result


def polymerize_industrial(template, map, cycles):
    unit_counts = collections.defaultdict(int)
    for pair in sliding_window(template, 2):
        unit_counts[pair] += 1

    for _ in range(cycles):
        starting_count = deepcopy(unit_counts)
        for pair, current_count in starting_count.items():
            new = polymerize(pair, map)
            for new_pair in sliding_window(new, 2):
                unit_counts[new_pair] += current_count
            unit_counts[pair] -= current_count  # original pair has gone!
    element_counts = collections.defaultdict(int)
    for pair, occurrences in unit_counts.items():
        for element in pair:
            element_counts[element] += occurrences

    element_counts[template[0]] += 1
    element_counts[template[-1]] += 1

    # counting pairs is actually double counting
    for key in element_counts:
        element_counts[key] //= 2

    return element_counts

def score_element_counts(element_counts):
    lengths = [v for k, v in element_counts.items()]
    lengths.sort(reverse=True)
    return lengths[0] - lengths[-1]


def score_polymer(polymer):
    lengths = [len(list(g)) for k, g in groupby(sorted(polymer))]
    lengths.sort(reverse=True)
    return lengths[0] - lengths[-1]


if __name__ == '__main__':
    template, map = load_instructions("day14_real_data.txt")
    for _ in range(10):
        template = polymerize(template, map)
    print("After ten iterations, the polymer has a score of {}".format(score_polymer(template)))

    template, map = load_instructions("day14_real_data.txt")
    element_counts = polymerize_industrial(template, map, 40)
    print("After forty iterations, the polymer has a score of {}".format(score_element_counts(element_counts)))

