from testfixtures import compare

from day12.day12 import build_map, calculate_routes, can_visit

test_data_small = """\
start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

test_data_medium = """\
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

test_data_complex = """\
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""


def test_build_map():
    test_map = {
        'A': {'end', 'c', 'start', 'b'},
        'b': {'end', 'A', 'start', 'd'},
        'c': {'A'},
        'd': {'b'},
        'end': {'A', 'b'},
        'start': {'A', 'b'},
    }
    compare(build_map(test_data_small), expected=test_map)


def test__calculate_routes__simple():
    expected = """\
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,end
start,A,c,A,end
start,A,end
start,b,A,c,A,end
start,b,A,end
start,b,end"""
    expected = [line.split(',') for line in expected.split('\n')]
    map = build_map(test_data_small)
    actual = calculate_routes(map)
    compare(actual, expected=sorted(expected))

def test__calculate_routes__medium():
    connections = build_map(test_data_medium)
    expected = """\
start,HN,dc,HN,end
start,HN,dc,HN,kj,HN,end
start,HN,dc,end
start,HN,dc,kj,HN,end
start,HN,end
start,HN,kj,HN,dc,HN,end
start,HN,kj,HN,dc,end
start,HN,kj,HN,end
start,HN,kj,dc,HN,end
start,HN,kj,dc,end
start,dc,HN,end
start,dc,HN,kj,HN,end
start,dc,end
start,dc,kj,HN,end
start,kj,HN,dc,HN,end
start,kj,HN,dc,end
start,kj,HN,end
start,kj,dc,HN,end
start,kj,dc,end"""
    expected = [line.split(',') for line in expected.split('\n')]
    actual = calculate_routes(connections)
    compare(actual, expected=sorted(expected))

def test__calculate_routes__complex():
    connections = build_map(test_data_complex)
    actual = calculate_routes(connections)
    compare(len(actual), expected=226)

def test__calculate_routes_revisiting_small_caves__simple():
    expected = """\
start,A,b,A,b,A,c,A,end
start,A,b,A,b,A,end
start,A,b,A,b,end
start,A,b,A,c,A,b,A,end
start,A,b,A,c,A,b,end
start,A,b,A,c,A,c,A,end
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,d,b,A,c,A,end
start,A,b,d,b,A,end
start,A,b,d,b,end
start,A,b,end
start,A,c,A,b,A,b,A,end
start,A,c,A,b,A,b,end
start,A,c,A,b,A,c,A,end
start,A,c,A,b,A,end
start,A,c,A,b,d,b,A,end
start,A,c,A,b,d,b,end
start,A,c,A,b,end
start,A,c,A,c,A,b,A,end
start,A,c,A,c,A,b,end
start,A,c,A,c,A,end
start,A,c,A,end
start,A,end
start,b,A,b,A,c,A,end
start,b,A,b,A,end
start,b,A,b,end
start,b,A,c,A,b,A,end
start,b,A,c,A,b,end
start,b,A,c,A,c,A,end
start,b,A,c,A,end
start,b,A,end
start,b,d,b,A,c,A,end
start,b,d,b,A,end
start,b,d,b,end
start,b,end"""
    expected = [line.split(',') for line in expected.split('\n')]
    map = build_map(test_data_small)
    actual = calculate_routes(map, small_cave_visits_allowed=2)
    compare(actual, expected=sorted(expected))

def test__calculate_routes_revisiting_small_caves__medium():
    connections = build_map(test_data_medium)
    actual = calculate_routes(connections, small_cave_visits_allowed=2)
    compare(len(actual), expected=103)

def test__calculate_routes_revisiting_small_caves__complex():
    connections = build_map(test_data_complex)
    actual = calculate_routes(connections, small_cave_visits_allowed=2)
    compare(len(actual), expected=3509)

def test_can_visit():
    compare(expected=True, actual=can_visit('a', ['start', 'b'], small_cave_visits_allowed=1))
    compare(expected=False, actual=can_visit('a', ['start', 'b', 'a'], small_cave_visits_allowed=1))
    compare(expected=True, actual=can_visit('a', ['start', 'b', 'a'], small_cave_visits_allowed=2))
    compare(expected=False, actual=can_visit('a', ['start', 'b', 'a', 'b'], small_cave_visits_allowed=2))

    compare(expected=True, actual=can_visit('b', ['start', 'A', 'b', 'A'], small_cave_visits_allowed=2))
