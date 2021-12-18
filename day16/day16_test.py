from testfixtures import compare

from day17.day17 import calculate_metrics, Probe

test_target_area = (20, 30, -10, -5)


def test_print_trajectory():
    expected = """\
.............#....#............
.......#..............#........
...............................
S........................#.....
...............................
...............................
...........................#...
...............................
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTT#TT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
"""
    probe = Probe(x_velocity=7, y_velocity=2, target=test_target_area)
    actual = probe.print_trajectory()
    compare(actual, expected=expected)


def test_integration():
    max_height, total_hits = calculate_metrics(test_target_area, max_x_velocity=50, max_y_velocity=100)
    compare(max_height, expected=45)
    compare(total_hits, expected=112)
