import itertools
import os


def get_readings(filename):
    test_data = os.path.join(os.path.dirname(__file__), filename)
    with open(test_data) as f:
        diagnostic_report = f.read().splitlines()  # this rather than readlines() to strip the terminal '\n' characters
    return diagnostic_report


def get_most_common(report_strings, tie_break=None):
    result = ""
    for bits in zip(*report_strings):
        number_of_ones = sum(b == "1" for b in bits)
        halfway_point = len(bits) / 2.0
        if number_of_ones > halfway_point:
            result += "1"
        elif number_of_ones < halfway_point:
            result += "0"
        else:
            if tie_break is None:
                raise ValueError("Equal numbers of 0s and 1s, and tie_break not set!!")
            result += tie_break
    return result


def invert(str):
    return "".join(["0" if char == "1" else "1" for char in str])


def bin_to_dec(str):
    return int(str, 2)


def get_gamma(report_strings):
    most_common = get_most_common(report_strings)
    return bin_to_dec(most_common)


def get_epsilon(report_strings):
    most_common = get_most_common(report_strings)
    return bin_to_dec(invert(most_common))


def get_oxygen_generator(report_strings):
    candidates = [r for r in report_strings]  # copy
    for index in range(len(report_strings[0])):
        most_common = get_most_common(candidates, tie_break="1")
        # filter out candidate values which don't match filter criterion
        candidates = [c for c in candidates if c[index] == most_common[index]]
        if len(candidates) == 1:
            return bin_to_dec(candidates[0])
    raise ValueError("No viable candidate found for oxygen_generator value")


def get_co2_scrubber(report_strings):
    candidates = [r for r in report_strings]  # copy
    for index in range(len(report_strings[0])):
        least_common = invert(get_most_common(candidates, tie_break="1"))
        # filter out candidate values which don't match filter criterion
        candidates = [c for c in candidates if c[index] == least_common[index]]
        if len(candidates) == 1:
            return bin_to_dec(candidates[0])
    raise ValueError("No viable candidate found for oxygen_generator value")


if __name__ == "__main__":
    readings = get_readings("day03_real_data.txt")
    gamma = get_gamma(readings)
    epsilon = get_epsilon(readings)
    print("The data has a gamma of {} and an epsilon of {} for a product of {}".format(gamma, epsilon, gamma * epsilon))
    oxygen = get_oxygen_generator(readings)
    co2 = get_co2_scrubber(readings)
    print("... and an O2 reading of {}, CO2 reading of {} for a product of {}".format(oxygen, co2, oxygen * co2))
