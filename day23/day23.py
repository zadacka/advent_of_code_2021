import os

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
            if not any(a for a in anthropods if a.y == 1 and a.x == home_room):
                if not any(a for a in anthropods if a.y == 2 and a.x == home_room):
                    return [(home_room, 2), ]
                if any(a for a in anthropods if a.y == 2 and a.x == home_room and a.type == self.type):
                    return [(home_room, 1), ]
            return []

        if self.y == 2:
            if anthropod2room[self.type] == self.x:
                return []  # already in the right place!
            elif any(a.x == self.x and a.y == 1 for a in anthropods):
                return []  # no allowed moves - blocked in!
            else:
                return routes_out()

        if self.y == 1:
            return routes_out()

        if self.y == 0:
            return routes_home()

        raise ValueError("Really should ever reach here.")

        # if self.y == 2 and any(a.x == self.x and a.y == 1 for a in anthropods):
        #     return []  # no allowed moves - blocked in!
        # elif self.y == 0:
        #     pass  # todo
        # else:
        #     coridoor_left =


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
    for y in range(1, 3):
        for index, c in enumerate(floormap[y + 1]):
            if c in anthropod2energy:
                anthropod = Anthropod(type=c, x=index - 1, y=y)
                anthropods.append(anthropod)
    return corridor, anthropods
