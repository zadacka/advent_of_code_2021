import os
from cmath import inf
from collections import defaultdict
from copy import deepcopy
from operator import itemgetter

from memoized import memoized

anthropod2energy = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}

anthropod2room = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}

memo = dict()

allowed_corridor_locations = (0, 0), (1, 0), (3, 0), (5, 0), (7, 0), (9, 0), (10, 0)
corridor_end = allowed_corridor_locations[-1][0]


class Anthropod(object):

    def __init__(self, type, x, y):
        super(Anthropod, self).__init__()
        self.type = type
        self.x = x
        self.y = y

    def __ne__(self, o: object) -> bool:
        return self.type != getattr(o, 'type') or self.x != getattr(o, 'x') or self.y != getattr(o, 'y')

    def get_allowed_moves(self, anthropods):
        def routes_out():
            left_limit = max([a.x for a in anthropods if a.y == 0 and a.x < self.x], default=-1)
            right_limit = min([a.x for a in anthropods if a.y == 0 and a.x > self.x], default=corridor_end + 1)
            return [loc for loc in allowed_corridor_locations if left_limit < loc[0] < right_limit]

        def routes_home():
            home_room = anthropod2room[self.type]
            start = min(self.x, home_room)
            end = max(self.x, home_room)
            blockers_home = [a.x for a in anthropods if a.y == 0 and start < a.x < end]
            if blockers_home:
                return []  # no way home
            h4_correct = any(a for a in anthropods if a.y == 4 and a.x == home_room and a.type == self.type)
            h3_correct = any(a for a in anthropods if a.y == 3 and a.x == home_room and a.type == self.type)
            h2_correct = any(a for a in anthropods if a.y == 2 and a.x == home_room and a.type == self.type)
            if not any(a for a in anthropods if a.y == 1 and a.x == home_room):
                if not any(a for a in anthropods if a.y == 2 and a.x == home_room):
                    if not any(a for a in anthropods if a.y == 3 and a.x == home_room):
                        if not any(a for a in anthropods if a.y == 4 and a.x == home_room):
                            return [(home_room, 4), ]
                        elif h4_correct:
                            return [(home_room, 3), ]
                    elif h4_correct and h3_correct:
                        return [(home_room, 2), ]
                elif h4_correct and h3_correct and h2_correct:
                    return [(home_room, 1), ]
            return []

        if self.y == 4:
            if anthropod2room[self.type] == self.x:
                return []  # already in the right place!
            elif any(a.x == self.x and a.y in (3,2,1) for a in anthropods):
                return []  # no allowed moves - blocked in!
            else:
                return routes_out()

        if self.y == 3:
            if any(a.x == self.x and a.y in (1, 2) for a in anthropods):
                return []  # no allowed moves - blocked in!
            elif self.x == anthropod2room[self.type] and self.pos4full(anthropods):
                return []  # correct place!
            else:
                return routes_out()

        if self.y == 2:
            if any(a.x == self.x and a.y == 1 for a in anthropods):
                return []  # no allowed moves - blocked in!
            elif self.x == anthropod2room[self.type] and self.pos4full(anthropods) and self.pos3full(anthropods):
                return []  # correct place!
            else:
                return routes_out()

        if self.y == 1:
            if self.x == anthropod2room[self.type]:  # in home room
                if self.pos2full(anthropods) and self.pos3full(anthropods) and self.pos4full(anthropods):
                    return []  # home room is full!
            return routes_out()

        if self.y == 0:
            return routes_home()

        raise ValueError("Really should ever reach here.")

    def pos2full(self, anthropods):
        return any(a for a in anthropods if a.type == self.type and a.x == self.x and a.y == 2)

    def pos3full(self, anthropods):
        return any(a for a in anthropods if a.type == self.type and a.x == self.x and a.y == 3)

    def pos4full(self, anthropods):
        return any(a for a in anthropods if a.type == self.type and a.x == self.x and a.y == 4)

    @property
    def at_home(self):
        return self.y in (1, 2,3,4) and self.x == anthropod2room[self.type]



def load_day23_data(filename):
    """
     v---- ---end of hallway  ... x = 0
    #############
    #...........#  - hallway  ... y = 0
    ###B#C#B#D###  - room     ... y = 1
      #A#D#C#A#    - room         y = 2
      #########
    """
    filepath = os.path.join(os.path.dirname(__file__), filename)

    anthropods = []
    with open(filepath) as f:
        floormap = f.readlines()

    corridor = [0 for c in floormap[1] if c == '.']
    for y in range(1, 5):
        for index, c in enumerate(floormap[y + 1]):
            if c in anthropod2energy:
                anthropod = Anthropod(type=c, x=index - 1, y=y)
                anthropods.append(anthropod)
    return corridor, anthropods


def anthropods2tuple(anthropods):
    anthropod_list = [(a.x, a.y, a.type) for a in anthropods]
    return tuple(sorted(anthropod_list, key=itemgetter(0, 1, 2)))

def set2anthropods(anthropods):
    return [Anthropod(type, x, y) for (x, y, type) in anthropods]


@memoized
def play_game(anthropod_tuple):
    anthropods = set2anthropods(anthropod_tuple)

    # print_map(anthropods)
    if not any(a.get_allowed_moves(anthropods) for a in anthropods):
        if all(a.at_home for a in anthropods):
            return 0
        else:
            return inf

    costs = []
    for index, a in enumerate(anthropods):
        allowed_moves = a.get_allowed_moves(anthropods)
        for move in allowed_moves:
            target_x, target_y = move
            cost = (abs(a.x - target_x) + abs(a.y - target_y)) * anthropod2energy[a.type]
            anthropods2 = deepcopy(anthropods)
            anthropods2[index].x = target_x
            anthropods2[index].y = target_y
            cost2end = play_game(anthropods2tuple(anthropods2))
            costs.append(cost + cost2end)
    # key = anthropods2set(anthropods)
    # memo[key] = min(memo.get(key, min(costs) + 1), min(costs))
    return min(costs)

if __name__ == '__main__':
    coridoor, anthropods = load_day23_data("day23_real_data.txt")
    anthrpods_tuple = anthropods2tuple(anthropods)

    print("Moving all of the anthropods home takes {} energy".format(play_game(anthrpods_tuple)))