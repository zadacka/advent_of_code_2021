from testfixtures import compare

from day25.day25 import load_day25_data, state_to_string, do_iterate, string_to_state, find_stable_state

test_state = [
    [".", ".", ".", ">", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ">"],
    ["v", ".", ".", ".", ".", ".", ">"],
    [".", ".", ".", ".", ".", ".", ">"],
    [".", ".", ".", ".", ".", ".", "."],
    [".", ".", "v", "v", "v", ".", "."],
]


def test_load_day25_data():
    compare(load_day25_data("day25_test_data.txt"), expected=test_state)

def test_to_string():
    expected= """\
...>...
.......
......>
v.....>
......>
.......
..vvv..
"""
    compare(state_to_string(test_state), expected=expected)

def test_iterate():
    expected1 = """\
..vv>..
.......
>......
v.....>
>......
.......
....v..
"""
    result = do_iterate(test_state)
    compare(state_to_string(result), expected=expected1)

    expected2="""\
....v>.
..vv...
.>.....
......>
v>.....
.......
.......
"""
    result = do_iterate(result)
    compare(state_to_string(result), expected=expected2)
    expected3="""\
......>
..v.v..
..>v...
>......
..>....
v......
.......
"""
    result = do_iterate(result)
    compare(state_to_string(result), expected=expected3)
    expected4="""\
>......
..v....
..>.v..
.>.v...
...>...
.......
v......
"""
    result = do_iterate(result)
    compare(state_to_string(result), expected=expected4)

def test_many_iterations():
    expected = """\
..>>v>vv.v
..v.>>vv..
v.>>v>>v..
..>>>>>vv.
vvv....>vv
..v....>>>
v>.......>
.vv>....v>
.>v.vv.v..
"""
    result = test_state
    for _ in range(50):
        result = do_iterate(result)
    compare(state_to_string(result), expected=expected)

def test_find_static_state():
    initial_state = """\
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""
    state=string_to_state(initial_state)
    compare(find_stable_state(state), expected=58)