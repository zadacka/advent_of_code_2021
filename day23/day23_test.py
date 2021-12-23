from testfixtures import compare

from day23.day23 import load_day23_data, Anthropod


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