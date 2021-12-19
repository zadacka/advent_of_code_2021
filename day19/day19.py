import copy
import os
from collections import defaultdict

import numpy as np


def load_day19_data(filename):
    result = []
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath) as f:
        scanners = f.read().split("\n\n")  # scanners separated by newline
        for scanner in scanners:
            lines = scanner.split('\n')
            assert lines[0].startswith("--- scanner")
            beacons = [[int(e) for e in line.split(',')] for line in lines[1:]]
            beacon_arrays = [np.array(b) for b in beacons]
            result.append(beacon_arrays)
    return result


def x_rotation_90(vector):
    """Rotates 3-D vector around x-axis"""
    R = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    return np.dot(R, vector)


def y_rotation_90(vector):
    """Rotates 3-D vector around y-axis"""
    R = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
    return np.dot(R, vector)


def z_rotation_90(vector):
    """Rotates 3-D vector around z-axis"""
    R = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    return np.dot(R, vector)


def generate_permutations(beacons):
    result = defaultdict(list)

    for beacon in beacons:
        b = copy.deepcopy(beacon)
        # four rotations around x axis
        result[0].append(b)
        result[1].append(x_rotation_90(b))
        result[2].append(x_rotation_90(x_rotation_90(b)))
        result[3].append(x_rotation_90(x_rotation_90(x_rotation_90(b))))

        # 90 around y
        b = y_rotation_90(b)
        result[4].append(b)
        result[5].append(x_rotation_90(b))
        result[6].append(x_rotation_90(x_rotation_90(b)))
        result[7].append(x_rotation_90(x_rotation_90(x_rotation_90(b))))

        # 180 around y
        b = y_rotation_90(b)
        result[8].append(b)
        result[9].append(x_rotation_90(b))
        result[10].append(x_rotation_90(x_rotation_90(b)))
        result[11].append(x_rotation_90(x_rotation_90(x_rotation_90(b))))

        # 270 around y
        b = y_rotation_90(b)
        result[12].append(b)
        result[13].append(x_rotation_90(b))
        result[14].append(x_rotation_90(x_rotation_90(b)))
        result[15].append(x_rotation_90(x_rotation_90(x_rotation_90(b))))

        # 90 around z
        b = z_rotation_90(beacon)
        result[16].append(b)
        result[17].append(x_rotation_90(b))
        result[18].append(x_rotation_90(x_rotation_90(b)))
        result[19].append(x_rotation_90(x_rotation_90(x_rotation_90(b))))

        # 270 around z
        b = z_rotation_90(b)
        result[20].append(b)
        result[21].append(x_rotation_90(b))
        result[22].append(x_rotation_90(x_rotation_90(b)))
        result[23].append(x_rotation_90(x_rotation_90(x_rotation_90(b))))
    return result


def find_translation(scanner0_beacons, new_beacons):
    translation = defaultdict(int)  # for a given translation, how many beacons would get mapped?
    for beacon in scanner0_beacons:
        for maybe_the_same_beacon in new_beacons:
            diff = beacon - maybe_the_same_beacon
            translation[(diff[0], diff[1], diff[2])] += 1
    for translation, count in translation.items():
        if count >= 12:  # 12 is the minimum beacons which must register to constitute a match
            return translation
    return None


def register_beacons(beacons_by_scanner):
    # scanner 0 is true by definition
    beacons = [beacon for beacon in beacons_by_scanner[0]]
    for scanner in beacons_by_scanner[1:]:
        all_orientations = generate_permutations(scanner)
        for beacons_in_this_frame_of_reference in all_orientations.values():
            translation = find_translation(beacons, beacons_in_this_frame_of_reference)
            if translation:
                for beacon in beacons_in_this_frame_of_reference:
                    beacons.append(beacon + np.array(translation))
                break

    return beacons
# scanner #1 is the 'origin' - we will use it as a reference

# for scanner in scanners[1:]

# this scanner can report its set of beacons with 24 different coordinates
# depending on how it is rotated.
# Generate a set of all of them so that we have ONE that matches the orientation of scanner 'origin'

# for each rotation....
# for each beacon in the 'origin' set, generate the relative position to each scanner in the 'candidate' set
# if we have 12 (or more) maps that are the same ... then we're a go! That rotation is a correct match

# for each beacon in the new known set (of the correct orientation) ... shift it by the mapping
# ... then continue with the next scanner
