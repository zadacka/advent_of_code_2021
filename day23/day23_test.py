from cmath import inf
from copy import deepcopy

from testfixtures import compare

from day23.day23 import load_day23_data, Anthropod, anthropod2energy, play_game, anthropods2tuple

printable_template = [
    [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ],
    [" ", "#", ".", "#", ".", "#", ".", "#", ".", "#", " ", ],
    [" ", "#", ".", "#", ".", "#", ".", "#", ".", "#", " ", ],
]


def test_load_day23_data():
    """
         v---- ---end of hallway  ... x = 0
        #############
        #...........#  - hallway  ... y = 0
        ###B#C#B#D###  - room     ... y = 1
          #A#D#C#A#    - room         y = 2
          #########
    """
    corridor, anthropods = load_day23_data("day23_test_data.txt")
    compare(corridor, expected=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    compare(anthropods, expected=[
        Anthropod('B', 2, 1),
        Anthropod('C', 4, 1),
        Anthropod('B', 6, 1),
        Anthropod('D', 8, 1),
        Anthropod('A', 2, 2),
        Anthropod('D', 4, 2),
        Anthropod('C', 6, 2),
        Anthropod('A', 8, 2),
    ])


def test_get_allowed_moves_out():
    """
         v---- ---end of hallway  ... x = 0
        #############
        #...........#  - hallway  ... y = 0
        ###B#C#B#D###  - room     ... y = 1
          #A#D#C#A#    - room         y = 2
          #########
    """
    bob = Anthropod('B', x=2, y=2)
    everywhere_in_corridor = [(0, 0), (1, 0), (3, 0), (5, 0), (7, 0), (9, 0), (10, 0)]
    compare(bob.get_allowed_moves(anthropods=[], ), expected=everywhere_in_corridor)

    blocked_in_by_someone = []
    compare(bob.get_allowed_moves(anthropods=[Anthropod('C', x=2, y=1)], ), expected=blocked_in_by_someone)

    blocked_on_the_right = [(0, 0), (1, 0), ]
    compare(bob.get_allowed_moves(anthropods=[Anthropod('C', x=3, y=0)], ), expected=blocked_on_the_right)

    blocked_on_the_right = [(3, 0), (5, 0), (7, 0), (9, 0), (10, 0), ]
    compare(bob.get_allowed_moves(anthropods=[Anthropod('C', x=1, y=0)], ), expected=blocked_on_the_right)

    # already in the right place
    bob = Anthropod('B', x=4, y=1)
    compare(bob.get_allowed_moves(anthropods=[Anthropod('B', x=4, y=0)], ), expected=[])

def test_get_allowed_moves_back():
    """
         v---- ---end of hallway  ... x = 0
        #############
        #...........#  - hallway  ... y = 0
        ###B#C#B#D###  - room     ... y = 1
          #A#D#C#A#    - room         y = 2
          #########
    """
    bob = Anthropod('B', x=0, y=0)
    bottom_of_home_room = [(4, 2), ]
    compare(bob.get_allowed_moves(anthropods=[], ), expected=bottom_of_home_room)

    top_of_home_room = [(4, 1), ]
    compare(bob.get_allowed_moves(anthropods=[Anthropod('B', x=4, y=2)], ), expected=top_of_home_room)

    nowhere = []
    # another anthropod of a different type in the home room - can't go in the empty y=1 space
    compare(bob.get_allowed_moves(anthropods=[Anthropod('C', x=4, y=2)], ), expected=nowhere)

    # something in the way in the corridor
    compare(bob.get_allowed_moves(anthropods=[Anthropod('B', x=1, y=0)], ), expected=nowhere)


def print_map(anthropods):
    template = deepcopy(printable_template)
    for anthropod in anthropods:
        template[anthropod.y][anthropod.x] = anthropod.type
    print()
    for row in template:
        print("".join(row))


def string2anthropods(string):
    floormap = string.split("\n")
    anthropods = []
    for y in range(0, 5):
        for index, c in enumerate(floormap[y + 1]):
            if c in anthropod2energy:
                anthropod = Anthropod(type=c, x=index - 1, y=y)
                anthropods.append(anthropod)
    return anthropods2tuple(anthropods)

def test_play_example_game():
    # corridor, anthropods = load_day23_data("day23_test_data.txt")
    # results = play_game(anthropods2tuple(anthropods))
    # compare(results, expected=44169)
    floormap = """\
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########
"""
    anthropods = string2anthropods(floormap)
    compare(play_game(anthropods), expected=0)
#
#     penultimate_floormap = """\
# #############
# #.....D.D.A.#
# ###.#B#C#.###
#   #A#B#C#.#
#   #########
# """
#
#     anthropods = string2anthropods(penultimate_floormap)
#     compare(play_game(anthropods), expected=7008)
#
#
#     penultimate_floormap = """\
# #############
# #.....D.....#
# ###.#B#C#D###
#   #A#B#C#A#
#   #########
# """
#     anthropods = string2anthropods(penultimate_floormap)
#     compare(play_game(anthropods), expected=9011)
#
#     penultimate_floormap = """\
# #############
# #.....D.....#
# ###B#.#C#D###
#   #A#B#C#A#
#   #########
# """
#     anthropods = string2anthropods(penultimate_floormap)
#     compare(play_game(anthropods), expected=9051)
#
#
#     penultimate_floormap = """\
# #############
# #...B.......#
# ###B#.#C#D###
#   #A#D#C#A#
#   #########
# """
#     anthropods = string2anthropods(penultimate_floormap)
#     compare(play_game(anthropods), expected=12081)
#
#
#     penultimate_floormap = """\
# #############
# #...B.......#
# ###B#C#.#D###
#   #A#D#C#A#
#   #########
# # """
#     anthropods = string2anthropods(penultimate_floormap)
#     compare(play_game(anthropods), expected=12481)
#
#
#
#     penultimate_floormap = """\
# #############
# #...........#
# ###B#C#B#D###
#   #A#D#C#A#
#   #########
# """
#     anthropods = string2anthropods(penultimate_floormap)
#     compare(play_game(anthropods), expected=12521)
#
