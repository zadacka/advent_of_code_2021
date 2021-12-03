import pytest
from testfixtures import compare

from day03.day03 import get_most_common, get_readings, invert, bin_to_dec, get_gamma, get_epsilon, get_oxygen_generator, \
    get_co2_scrubber

TEST_DATA_FILE = "day03_test_data.txt"


def test_get_readings():
    diagnostic_report = get_readings(TEST_DATA_FILE)
    expected = ["00100", "11110", "10110", "10111", "10101", "01111", "00111", "11100", "10000", "11001", "00010",
                "01010"]
    compare(expected, actual=diagnostic_report)


def test_get_most_common():
    diagnostic_report = get_readings("day03_test_data.txt")
    actual = get_most_common(diagnostic_report)
    expected = "10110"
    compare(expected, actual=actual)


def test_invert():
    compare("0011001", actual=invert("1100110"))


def test_bin_to_dec():
    compare(1, actual=bin_to_dec("1"))
    compare(2, actual=bin_to_dec("10"))
    compare(5, actual=bin_to_dec("101"))


@pytest.fixture
def readings():
    yield get_readings(TEST_DATA_FILE)


def test_get_gamma(readings):
    expected = 22
    compare(expected, actual=get_gamma(readings))


def test_get_epsilon(readings):
    expected = 9
    readings = get_readings(TEST_DATA_FILE)
    compare(expected, actual=get_epsilon(readings))


def test_get_oxygen_generator(readings):
    expected = 23
    compare(expected, actual=get_oxygen_generator(readings))


def test_get_co2_scrubber(readings):
    expected = 10
    compare(expected, actual=get_co2_scrubber(readings))
