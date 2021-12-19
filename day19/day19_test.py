from testfixtures import compare

from day19.day19 import load_day19_data, generate_permutations, find_translation, register_beacons, \
    calculate_manhattan_distance, calculate_max_manhattan_distance


def test__load_day19_data():
    actual = load_day19_data("day19_test_data.txt")
    compare(actual[0][0], expected=(404, -588, -901))
    compare(actual[0][-1], expected=(459, -707, 401))
    compare(actual[-1][-1], expected=(30, -46, -14))


def test__generate_permutations():
    beacons = [
        (1, 1, 1),
        (2, 2, 2),
    ]
    actual = generate_permutations(beacons)
    expected = [
        [(1, 1, 1), (2, 2, 2)],
        [(1, -1, 1), (2, -2, 2)],
        [(1, -1, -1), (2, -2, -2)],
        [(1, 1, -1), (2, 2, -2)],
        [(1, 1, -1), (2, 2, -2)],
        [(1, 1, 1), (2, 2, 2)],
        [(1, -1, 1), (2, -2, 2)],
        [(1, -1, -1), (2, -2, -2)],
        [(-1, 1, -1), (-2, 2, -2)],
        [(-1, 1, 1), (-2, 2, 2)],
        [(-1, -1, 1), (-2, -2, 2)],
        [(-1, -1, -1), (-2, -2, -2)],
        [(-1, 1, 1), (-2, 2, 2)],
        [(-1, -1, 1), (-2, -2, 2)],
        [(-1, -1, -1), (-2, -2, -2)],
        [(-1, 1, -1), (-2, 2, -2)],
        [(-1, 1, 1), (-2, 2, 2)],
        [(-1, -1, 1), (-2, -2, 2)],
        [(-1, -1, -1), (-2, -2, -2)],
        [(-1, 1, -1), (-2, 2, -2)],
        [(1, -1, 1), (2, -2, 2)],
        [(1, -1, -1), (2, -2, -2)],
        [(1, 1, -1), (2, 2, -2)],
        [(1, 1, 1), (2, 2, 2)],
    ]
    compare(actual, expected=expected)


def test_find_translation():
    beacons_seen_by_scanner_0 = [
        (-618, -824, -621),
        (-537, -823, -458),
        (-447, -329, 318),
        (404, -588, -901),
        (544, -627, -890),
        (528, -643, 409),
        (-661, -816, -575),
        (390, -675, -793),
        (423, -701, 434),
        (-345, -311, 381),
        (459, -707, 401),
        (-485, -357, 347),
    ]
    beacons_seen_by_scanner_1 = [
        (686, 422, 578),
        (605, 423, 415),
        (515, 917, -361),
        (-336, 658, 858),
        (-476, 619, 847),
        (-460, 603, -452),
        (729, 430, 532),
        (-322, 571, 750),
        (-355, 545, -477),
        (413, 935, -424),
        (-391, 539, -444),
        (553, 889, -390),
    ]
    found_translation = None
    permutations = generate_permutations(beacons_seen_by_scanner_1)
    for beacons_in_this_frame_of_reference in permutations:
        translation = find_translation(beacons_seen_by_scanner_0, beacons_in_this_frame_of_reference)
        if translation:
            found_translation = translation

    compare(found_translation, expected=(68, -1246, -43))


def test__register_beacons():
    beacons_by_scanner = load_day19_data("day19_test_data.txt")
    registered_beacons, _ = register_beacons(beacons_by_scanner)
    compare(len(registered_beacons), expected=79)


def test__register_beacons_scanner_positions():
    beacons_by_scanner = load_day19_data("day19_test_data.txt")
    _, scanner_positions = register_beacons(beacons_by_scanner)
    compare(scanner_positions[0], expected=(0, 0, 0))
    compare(scanner_positions[2], expected=(1105, -1205, 1229))
    compare(scanner_positions[3], expected=(-92, -2380, -20))


def test_manhattan_distances():
    compare(calculate_manhattan_distance((1105, -1205, 1229), (-92, -2380, -20)), expected=3621)


def test_calculate_max_manhattan_distance():
    scanners_positions = {0: (0, 0, 0), 1: (68, -1246, -43), 3: (-92, -2380, -20), 4: (-20, -1133, 1061),
                          2: (1105, -1205, 1229)}
    compare(calculate_max_manhattan_distance(scanners_positions), expected=3621)
