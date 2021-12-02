import os.path


class Submarine(object):

    def __init__(self, aim_enabled) -> None:
        super().__init__()
        self.depth = 0
        self.horizontal_position = 0
        self.aim = 0
        self.aim_enabled = aim_enabled

    def forward(self, distance):
        if self.aim_enabled:
            self.depth += self.aim * distance
        self.horizontal_position += distance

    def down(self, distance):
        if self.aim_enabled:
            self.aim += distance
        else:
            self.depth += distance

    def up(self, distance):
        if self.aim_enabled:
            self.aim -= distance
        else:
            self.depth -= distance

    def do_movement(self, movement_string):
        movement, distance = movement_string.split()
        self.__getattribute__(movement)(int(distance))

    def report_position(self):
        if self.aim_enabled:
            return self.depth, self.horizontal_position, self.aim
        return self.depth, self.horizontal_position


def process_movement_file(movement_file):
    data = os.path.join(os.path.dirname(__file__), movement_file)
    with open(data) as f:
        movements = f.readlines()

    submarine = Submarine(aim_enabled=False)
    for movement in movements:
        submarine.do_movement(movement)
    msg = "Final position (of aimless submarine) is depth {} and horizontal_position {} for a product of {}"
    print(msg.format(submarine.depth, submarine.horizontal_position, submarine.depth * submarine.horizontal_position))

    submarine = Submarine(aim_enabled=True)
    for movement in movements:
        submarine.do_movement(movement)
    msg = "Final position (of aimed submarine) is depth {} and horizontal_position {} for a product of {}"
    print(msg.format(submarine.depth, submarine.horizontal_position, submarine.depth * submarine.horizontal_position))


if __name__ == "__main__":
    process_movement_file("day02_real_data.txt")
