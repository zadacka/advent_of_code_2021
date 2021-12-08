import os.path

def load_data(filename):
    result = []
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath) as f:
        for line in f.readlines():
            before, after = line.split('|')
            result.append((before.split(), after.split()))
    return result


def count_uniques(data):
    segment_to_digit_map = {2: '1', 3: '7', 4: '4', 7: '8'}  # map of segments illuminated to number shown
    unique_count = 0
    for before, after in data:
        for group in after:
            if len(group) in segment_to_digit_map:
                unique_count += 1
    return unique_count


def get_where(input_list, length):
    return [item for item in input_list if len(item) == length]


def get_wire_to_segment_map(data):
    # unique digits where lengths identify them
    one = set(get_where(data, length=2).pop())
    four = set(get_where(data, length=4).pop())
    seven = set(get_where(data, length=3).pop())
    eight = set(get_where(data, length=7).pop())

    # segment to wire mapping where they are unambiguous
    a = seven - one

    #  then work the rest out...
    zero_six_nine = set(get_where(data, length=6))
    two_three_five = set(get_where(data, length=5))

    six = set([candidate for candidate in zero_six_nine if len(set(candidate) - one) == 5].pop())
    zero_nine = [c for c in zero_six_nine if set(c) != six]
    c = eight - six

    three = set([c for c in two_three_five if len(set(c) - one) == 3].pop())
    two_five = [c for c in two_three_five if set(c) != three]

    two = set([c for c in two_five if len(set(c) - six) == 1].pop())
    five = set([c for c in two_five if len(set(c) - six) == 0].pop())

    e = two - three
    zero = set([c for c in zero_nine if e.issubset(set(c))].pop())
    nine = set([c for c in zero_nine if set(c) != zero].pop())

    b = eight - two - one
    d = eight - zero
    f = eight - two - b
    g = eight - four - a - e

    segment_to_wire_map = {
        "a": list(a).pop(),
        "b": list(b).pop(),
        "c": list(c).pop(),
        "d": list(d).pop(),
        "e": list(e).pop(),
        "f": list(f).pop(),
        "g": list(g).pop(),
    }
    wire_to_segment_map = {value: key for key, value in segment_to_wire_map.items()}

    return wire_to_segment_map

segments_to_digit = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9
}

def translate_code_to_number(mapping, code):
    active_segments = ""
    for character in code:
        active_segments += mapping[character]
    active_segments = ''.join(sorted(active_segments))
    return segments_to_digit[active_segments]

def calculate_remaining_digits_value(mapping, codes):
    result = 0
    for code, multiplier in zip(codes, (1000, 100, 10, 1)):
        result += translate_code_to_number(mapping, code) * multiplier
    return result

def get_total(data):
    total = 0
    for before, after in data:
        mapping = get_wire_to_segment_map(before)
        total += calculate_remaining_digits_value(mapping, after)
    return total

if __name__ == "__main__":
    data = load_data("day08_real_data.txt")
    print("There are {} unique digits after the | delimiter in the data".format(count_uniques(data)))

    print("There total is {}".format(get_total(data)))
