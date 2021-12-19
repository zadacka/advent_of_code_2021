from itertools import zip_longest

from testfixtures import compare
import numpy as np

from day19.day19 import load_day19_data, generate_permutations, find_translation, register_beacons


def test__load_day19_data():
    actual = load_day19_data("day19_test_data.txt")
    compare(np.array_equal(actual[0][0], np.array([404, -588, -901])), expected=True)
    compare(np.array_equal(actual[0][-1], np.array([459, -707, 401])), expected=True)
    compare(np.array_equal(actual[-1][-1], np.array([30, -46, -14])), expected=True)


def test__generate_permutations():
    beacons = [
        np.array([1, 1, 1]),
        np.array([2, 2, 2]),
    ]
    actual = generate_permutations(beacons)
    expected = {
        0: [np.array([1, 1, 1]), np.array([2, 2, 2])],
        1: [np.array([1, -1, 1]), np.array([2, -2, 2])],
        2: [np.array([1, -1, -1]), np.array([2, -2, -2])],
        3: [np.array([1, 1, -1]), np.array([2, 2, -2])],
        4: [np.array([1, 1, -1]), np.array([2, 2, -2])],
        5: [np.array([1, 1, 1]), np.array([2, 2, 2])],  # TODO: potential bug? Need to think a bit more about the rotations...
        6: [np.array([1, -1, 1]), np.array([2, -2, 2])],
        7: [np.array([1, -1, -1]), np.array([2, -2, -2])],
        8: [np.array([-1, 1, -1]), np.array([-2, 2, -2])],
        9: [np.array([-1, 1, 1]), np.array([-2, 2, 2])],
        10: [np.array([-1, -1, 1]), np.array([-2, -2, 2])],
        11: [np.array([-1, -1, -1]), np.array([-2, -2, -2])],
        12: [np.array([-1, 1, 1]), np.array([-2, 2, 2])],
        13: [np.array([-1, -1, 1]), np.array([-2, -2, 2])],
        14: [np.array([-1, -1, -1]), np.array([-2, -2, -2])],
        15: [np.array([-1, 1, -1]), np.array([-2, 2, -2])],
        16: [np.array([-1, 1, 1]), np.array([-2, 2, 2])],
        17: [np.array([-1, -1, 1]), np.array([-2, -2, 2])],
        18: [np.array([-1, -1, -1]), np.array([-2, -2, -2])],
        19: [np.array([-1, 1, -1]), np.array([-2, 2, -2])],
        20: [np.array([-1, -1, 1]), np.array([-2, -2, 2])],
        21: [np.array([-1, -1, -1]), np.array([-2, -2, -2])],
        22: [np.array([-1, 1, -1]), np.array([-2, 2, -2])],
        23: [np.array([-1, 1, 1]), np.array([-2, 2, 2])],
    }
    compare(set(actual.keys()), expected=set(expected.keys()))
    for key in actual.keys():
        for e, a in zip_longest(expected[key], actual[key]):
            compare(np.array_equal(e, a), expected=True)


def test_find_translation():
    beacons_seen_by_scanner_0 = [
        np.array([-618, -824, -621]),
        np.array([-537, -823, -458]),
        np.array([-447, -329, 318]),
        np.array([404, -588, -901]),
        np.array([544, -627, -890]),
        np.array([528, -643, 409]),
        np.array([-661, -816, -575]),
        np.array([390, -675, -793]),
        np.array([423, -701, 434]),
        np.array([-345, -311, 381]),
        np.array([459, -707, 401]),
        np.array([-485, -357, 347]),
    ]
    beacons_seen_by_scanner_1 = [
        np.array([686, 422, 578]),
        np.array([605, 423, 415]),
        np.array([515, 917, -361]),
        np.array([-336, 658, 858]),
        np.array([-476, 619, 847]),
        np.array([-460, 603, -452]),
        np.array([729, 430, 532]),
        np.array([-322, 571, 750]),
        np.array([-355, 545, -477]),
        np.array([413, 935, -424]),
        np.array([-391, 539, -444]),
        np.array([553, 889, -390]),
    ]
    found_translation = None
    permutations = generate_permutations(beacons_seen_by_scanner_1)
    for k, beacons_in_this_frame_of_reference in permutations.items():
        translation = find_translation(beacons_seen_by_scanner_0, beacons_in_this_frame_of_reference)
        if translation:
            found_translation = translation

    compare(found_translation, expected=(68, -1246, -43))


def test_register_beacons():
    beacons_by_scanner = load_day19_data("day19_test_data.txt")
    registered = register_beacons(beacons_by_scanner)
    compare(len(registered), expected=79)
