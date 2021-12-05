from testfixtures import compare

from day05.day05 import parse_vent_input_file, Vent


def test_parse_vent_input_file():
    lines = parse_vent_input_file("day05_test_data.txt")
    expected = [
        ((0, 9), (5, 9))
        ((8, 0), (0, 8))
        ((9, 4), (3, 4))
        ((2, 2), (2, 1))
        ((7, 0), (7, 4))
        ((6, 4), (2, 0))
        ((0, 9), (2, 9))
        ((3, 4), (1, 4))
        ((0, 0), (8, 8))
        ((5, 5), (8, 2))
        # Vent(0, 9, 5, 9),
        # Vent(8, 0, 0, 8),
        # Vent(9, 4, 3, 4),
        # Vent(2, 2, 2, 1),
        # Vent(7, 0, 7, 4),
        # Vent(6, 4, 2, 0),
        # Vent(0, 9, 2, 9),
        # Vent(3, 4, 1, 4),
        # Vent(0, 0, 8, 8),
        # Vent(5, 5, 8, 2),
    ]
    compare(expected, actual=lines)


def test_generate_map():
    pass
