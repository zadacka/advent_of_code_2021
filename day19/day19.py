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
            beacons = [tuple((int(e) for e in line.split(','))) for line in lines[1:]]
            result.append(beacons)
    return result


def x_rotation_90(vector):
    """Rotates 3-D vector around x-axis"""
    R = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    return tuple(np.dot(R, vector))


def y_rotation_90(vector):
    """Rotates 3-D vector around y-axis"""
    R = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
    return tuple(np.dot(R, vector))


def z_rotation_90(vector):
    """Rotates 3-D vector around z-axis"""
    R = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    return tuple(np.dot(R, vector))


def generate_permutations(beacons):
    result = [[] for _ in range(24)]
    # Look at the room in front of you.
    # the positive x-axis runs out to your right
    # the positive y-axis runs up through your head to the ceiling
    # the positive z-axis runs out in front of you to the wall

    # Thinking about this (not *quite* how I've done the below - but the end result is the same)
    # we can face along the positive or negative directions along each axis = 6 sides to our cube
    # for each direction we face, we can additionally rotate around our viewpoint in steps of 90 degrees
    # result = facing 6 directions * 4 rotations = 24 possible coordinate systems we could use to represent points

    for beacon in beacons:
        b = copy.deepcopy(beacon)
        # four rotations around x axis ... a back-flip in four stages!
        result[0].append(b)
        result[1].append(x_rotation_90(b))
        result[2].append(x_rotation_90(x_rotation_90(b)))
        result[3].append(x_rotation_90(x_rotation_90(x_rotation_90(b))))

        # 90 around y (turn to the right) ...
        b = y_rotation_90(b)
        result[4].append(b)
        result[5].append(x_rotation_90(b))
        result[6].append(x_rotation_90(x_rotation_90(b)))
        result[7].append(x_rotation_90(x_rotation_90(x_rotation_90(b))))

        # 180 around y (you've turned around to face the opposite direction from where you started)
        b = y_rotation_90(b)
        result[8].append(b)
        result[9].append(x_rotation_90(b))
        result[10].append(x_rotation_90(x_rotation_90(b)))
        result[11].append(x_rotation_90(x_rotation_90(x_rotation_90(b))))

        # 270 around y (still turning ... you're facing what was originally on your left)
        b = y_rotation_90(b)
        result[12].append(b)
        result[13].append(x_rotation_90(b))
        result[14].append(x_rotation_90(x_rotation_90(b)))
        result[15].append(x_rotation_90(x_rotation_90(x_rotation_90(b))))

        # 90 around z (back to the starting point, then tilt your head 90 degrees)
        b = z_rotation_90(beacon)
        result[16].append(b)
        result[17].append(x_rotation_90(b))
        result[18].append(x_rotation_90(x_rotation_90(b)))
        result[19].append(x_rotation_90(x_rotation_90(x_rotation_90(b))))

        # 270 around z (back to the start, then tilt your head left 90 degrees)
        b = z_rotation_90(z_rotation_90(b))
        result[20].append(b)
        result[21].append(x_rotation_90(b))
        result[22].append(x_rotation_90(x_rotation_90(b)))
        result[23].append(x_rotation_90(x_rotation_90(x_rotation_90(b))))
    return result


def find_translation(scanner0_beacons, new_beacons):
    translation = defaultdict(int)  # for a given translation, how many beacons would get mapped?
    for beacon in scanner0_beacons:
        for maybe_the_same_beacon in new_beacons:
            diff = np.array(beacon) - np.array(maybe_the_same_beacon)
            translation[tuple(diff)] += 1
            if translation[tuple(diff)] == 12:
                return tuple(diff)
    return None


def attempt_translate_beacons(registered_beacons, beacons):
    for frame_of_reference in generate_permutations(beacons):
        translation = find_translation(registered_beacons, frame_of_reference)
        if translation:
            return {tuple(np.array(beacon) + np.array(translation)) for beacon in frame_of_reference}, translation
    return None, None


def register_beacons(beacons_by_scanner):
    # scanner 0 is true by definition
    registered_beacons = {beacon for beacon in beacons_by_scanner[0]}
    translated_scanners = {0: (0, 0, 0)}

    while len(translated_scanners) < len(beacons_by_scanner):

        for scanner_number, beacons in enumerate(beacons_by_scanner):
            if scanner_number in translated_scanners:
                continue  # we've already done this scanner

            translated_beacons, translation = attempt_translate_beacons(registered_beacons, beacons)
            if translated_beacons is not None:
                print(f"Registration found for scanner {scanner_number}!")  # runs slow-ish, get an idea of progress
                registered_beacons.update(translated_beacons)
                translated_scanners[scanner_number] = translation

    return registered_beacons, translated_scanners


def calculate_manhattan_distance(point1, point2):
    return sum(abs(p2 - p1) for p1, p2 in zip(point1, point2))


def calculate_max_manhattan_distance(scanner_positions):
    result = {}
    for scanner1, position1 in scanner_positions.items():
        for scanner2, position2 in scanner_positions.items():
            if scanner1 == scanner2:
                pass
            result[f"{scanner1}->{scanner2}"] = calculate_manhattan_distance(position1, position2)
    return max(result.values())


if __name__ == '__main__':
    beacons_by_scanner = load_day19_data("day19_real_data.txt")
    beacons, scanner_positions = register_beacons(beacons_by_scanner)
    print(f"Once registered consistently, there are {len(beacons)} beacons present.")
    print(f"... and a max Manhattan distance between scanners of {calculate_max_manhattan_distance(scanner_positions)}")
