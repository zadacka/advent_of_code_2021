from testfixtures import compare

from day22 import load_day22_data, ON, OFF, execute_steps


def test__load_day22_data():
    actual = load_day22_data("day22_test_data.txt")
    expected = (        (ON, (-20, 26), (-36, 17), (-47, 7)),
        (ON, (-20, 33), (-21, 23), (-26, 28)),
        (ON, (-22, 28), (-29, 23), (-38, 16)),
        (ON, (-46, 7), (-6, 46), (-50, -1)),
        (ON, (-49, 1), (-3, 46), (-24, 28)),
        (ON, (2, 47), (-22, 22), (-23, 27)),
        (ON, (-27, 23), (-28, 26), (-21, 29)),
        (ON, (-39, 5), (-6, 47), (-3, 44)),
        (ON, (-30, 21), (-8, 43), (-13, 34)),
        (ON, (-22, 26), (-27, 20), (-29, 19)),
        (OFF, (-48, -32), (26, 41), (-47, -37)),
        (ON, (-12, 35), (6, 50), (-50, -2)),
        (OFF, (-48, -32), (-32, -16), (-15, -5)),
        (ON, (-18, 26), (-33, 15), (-7, 46)),
        (OFF, (-40, -22), (-38, -28), (23, 41)),
        (ON, (-16, 35), (-41, 10), (-47, 6)),
        (OFF, (-32, -23), (11, 30), (-14, 3)),
        (ON, (-49, -5), (-3, 45), (-29, 18)),
        (OFF, (18, 30), (-20, -8), (-3, 13)),
        (ON, (-41, 9), (-7, 43), (-33, 15)),
        (ON, (-54112, -39298), (-85059, -49293), (-27449, 7877)),
        (ON, (967, 23432), (45373, 81175), (27513, 53682)),
    )
    compare(actual, expected=expected)


def test_execute_steps():
    test_reactor = execute_steps(
        (
            (ON, (10, 12), (10, 12), (10, 12)),
        )
    )
    actual = sorted(list(test_reactor))
    expected = [
        (10,10,10),
        (10,10,11),
        (10,10,12),
        (10,11,10),
        (10,11,11),
        (10,11,12),
        (10,12,10),
        (10,12,11),
        (10,12,12),
        (11,10,10),
        (11,10,11),
        (11,10,12),
        (11,11,10),
        (11,11,11),
        (11,11,12),
        (11,12,10),
        (11,12,11),
        (11,12,12),
        (12,10,10),
        (12,10,11),
        (12,10,12),
        (12,11,10),
        (12,11,11),
        (12,11,12),
        (12,12,10),
        (12,12,11),
        (12,12,12),
    ]
    compare(actual, expected=expected)

def test_report_on():
    test_reactor = execute_steps(
        (
            (ON, (10, 12), (10, 12), (10, 12)),
        )
    )
    compare(len(test_reactor), expected=27)


def test_execute_steps__ignores_outside_of_initialization_area():
    test_reactor = execute_steps(
        (
            (ON, (-55, -51), (-55, -51), (-55, -51)),
        )
    )
    compare(len(test_reactor), expected=0)

def test_integration():
    steps = load_day22_data("day22_test_data.txt")
    reactor = execute_steps(steps)
    compare(len(reactor), expected=590784)

    # reactor = execute_steps(steps, include_bounding)
    # compare(len(reactor), expected=590784)