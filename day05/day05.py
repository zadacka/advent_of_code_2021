import os.path


class Vent:

    # def determine_type(self):
    #     if self.start_x == self.end_x and self.start_y == self.end_y:
    #         return "point"
    #     if self.start_x == self.end_x:
    #         return "horixontal"
    #     elif self.start_y == self.end_y:
    #         return "vertical"
    #     elif (self.end_x - self.start_x) == (self.end_y - self.start_y):
    #         return "diagonal"
    #     else:
    #         raise ValueError(
    #             "Unknown line type {},{} -> {}{}".format(self.start_x, self.start_y, self.end_x, self.end_y))
    #
    # def __init__(self, start_x, start_y, end_x, end_y) -> None:
    #     super().__init__()
    #     # ensure start < end so future line processing can assume that order
    #     self.start_x = min(int(start_x), int(end_x))
    #     self.start_y = min(int(start_y), int(end_y))
    #     self.end_x = max(int(start_x), int(end_x))
    #     self.end_y = max(int(start_y), int(end_y))
    #
    #     self.type = self.determine_type()


def parse_vent_input_file(filename):
    file_path = os.path.join(os.path.dirname(__file__), filename)
    result = []
    with open(file_path) as f:
        for line in f.readlines():
            start, arrow, end = line.split()
            vent = Vent(*start.split(','), *end.split(','))
            result.append(vent)
    return result
