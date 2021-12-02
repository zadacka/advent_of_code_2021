import os.path

import pytest
import testfixtures

from day02.day02 import Submarine


@pytest.fixture()
def submarine_aim_disabled():
    yield Submarine(aim_enabled=False)


@pytest.fixture()
def submarine_aim_enabled():
    yield Submarine(aim_enabled=True)


class TestSubmarine:
    def test_submarine_initial_position(self, submarine_aim_disabled):
        testfixtures.compare(submarine_aim_disabled.depth, 0)
        testfixtures.compare(submarine_aim_disabled.horizontal_position, 0)

    def test_submarine_movement_works(self, submarine_aim_disabled):
        testfixtures.compare(submarine_aim_disabled.report_position(), (0, 0))
        submarine_aim_disabled.forward(1)
        testfixtures.compare(submarine_aim_disabled.report_position(), (0, 1))
        submarine_aim_disabled.down(1)
        testfixtures.compare(submarine_aim_disabled.report_position(), (1, 1))
        submarine_aim_disabled.up(1)
        testfixtures.compare(submarine_aim_disabled.report_position(), (0, 1))

    def test_do_movement(self, submarine_aim_disabled):
        testfixtures.compare(submarine_aim_disabled.report_position(), (0, 0))
        submarine_aim_disabled.do_movement("forward 1")
        testfixtures.compare(submarine_aim_disabled.report_position(), (0, 1))
        submarine_aim_disabled.do_movement("down 1")
        testfixtures.compare(submarine_aim_disabled.report_position(), (1, 1))
        submarine_aim_disabled.do_movement("up 1")
        testfixtures.compare(submarine_aim_disabled.report_position(), (0, 1))

    def test_do_movement_with_aim(self, submarine_aim_enabled):
        testfixtures.compare(submarine_aim_enabled.report_position(), (0, 0, 0))
        submarine_aim_enabled.do_movement("forward 5")
        testfixtures.compare(submarine_aim_enabled.report_position(), (0, 5, 0))
        submarine_aim_enabled.do_movement("down 5")
        testfixtures.compare(submarine_aim_enabled.report_position(), (0, 5, 5))
        submarine_aim_enabled.do_movement("forward 8")
        testfixtures.compare(submarine_aim_enabled.report_position(), (40, 13, 5))
        submarine_aim_enabled.do_movement("up 3")
        testfixtures.compare(submarine_aim_enabled.report_position(), (40, 13, 2))
        submarine_aim_enabled.do_movement("down 8")
        testfixtures.compare(submarine_aim_enabled.report_position(), (40, 13, 10))
        submarine_aim_enabled.do_movement("forward 2")
        testfixtures.compare(submarine_aim_enabled.report_position(), (60, 15, 10))


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
