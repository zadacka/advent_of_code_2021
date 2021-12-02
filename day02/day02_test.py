import os.path

import pytest
import testfixtures

from day02.day02 import Submarine


@pytest.fixture()
def submarine():
    yield Submarine(aim_enabled=False)


@pytest.fixture()
def aiming_submarine():
    yield Submarine(aim_enabled=True)


class TestSubmarine:
    def test_submarine_initial_position(self, submarine):
        testfixtures.compare(submarine.depth, 0)
        testfixtures.compare(submarine.horizontal_position, 0)

    def test_submarine_movement_works(self, submarine):
        testfixtures.compare(submarine.report_position(), (0, 0))
        submarine.forward(1)
        testfixtures.compare(submarine.report_position(), (0, 1))
        submarine.down(1)
        testfixtures.compare(submarine.report_position(), (1, 1))
        submarine.up(1)
        testfixtures.compare(submarine.report_position(), (0, 1))

    def test_do_movement(self, submarine):
        testfixtures.compare(submarine.report_position(), (0, 0))
        submarine.do_movement("forward 1")
        testfixtures.compare(submarine.report_position(), (0, 1))
        submarine.do_movement("down 1")
        testfixtures.compare(submarine.report_position(), (1, 1))
        submarine.do_movement("up 1")
        testfixtures.compare(submarine.report_position(), (0, 1))

    def test_do_movement_with_aim(self, aiming_submarine):
        testfixtures.compare(aiming_submarine.report_position(), (0, 0, 0))
        aiming_submarine.do_movement("forward 5")
        testfixtures.compare(aiming_submarine.report_position(), (0, 5, 0))
        aiming_submarine.do_movement("down 5")
        testfixtures.compare(aiming_submarine.report_position(), (0, 5, 5))
        aiming_submarine.do_movement("forward 8")
        testfixtures.compare(aiming_submarine.report_position(), (40, 13, 5))
        aiming_submarine.do_movement("up 3")
        testfixtures.compare(aiming_submarine.report_position(), (40, 13, 2))
        aiming_submarine.do_movement("down 8")
        testfixtures.compare(aiming_submarine.report_position(), (40, 13, 10))
        aiming_submarine.do_movement("forward 2")
        testfixtures.compare(aiming_submarine.report_position(), (60, 15, 10))


def test_movement():
    test_data = os.path.join(os.path.dirname(__file__), "day02_test_data.txt")
    with open(test_data) as f:
        movements = f.readlines()

    submarine = Submarine(aim_enabled=False)
    for movement in movements:
        submarine.do_movement(movement)
    testfixtures.compare(150, submarine.depth * submarine.horizontal_position)

    submarine = Submarine(aim_enabled=True)
    for movement in movements:
        submarine.do_movement(movement)
    testfixtures.compare(900, submarine.depth * submarine.horizontal_position)
