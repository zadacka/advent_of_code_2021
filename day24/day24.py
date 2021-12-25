import os.path
from collections import deque, defaultdict
from copy import deepcopy


class Alu(object):

    def __init__(self, model2check, steps, w=0, x=0, y=0, z=0) -> None:
        super().__init__()
        self.input_buffer = model2check
        self.steps = steps
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def input(self, target):
        self.__setattr__(target, self.input_buffer.popleft())

    def add(self, a, b):
        if not isinstance(b, int):
            b = self.__getattribute__(b)
        self.__setattr__(a, self.__getattribute__(a) + b)

    def mul(self, a, b):
        if not isinstance(b, int):
            b = self.__getattribute__(b)
        self.__setattr__(a, self.__getattribute__(a) * b)

    def div(self, a, b):
        if not isinstance(b, int):
            b = self.__getattribute__(b)
        self.__setattr__(a, self.__getattribute__(a) // b)

    def mod(self, a, b):
        if not isinstance(b, int):
            b = self.__getattribute__(b)
        self.__setattr__(a, self.__getattribute__(a) % b)

    def eql(self, a, b):
        if not isinstance(b, int):
            b = self.__getattribute__(b)
        self.__setattr__(a, 1 if self.__getattribute__(a) == b else 0)

    def do_steps(self, block):
        current_block = -1
        for (instruction, a, b) in self.steps:
            if instruction == 'inp':
                # self.input(a)
                current_block += 1
            elif instruction == 'add' and current_block == block:
                self.add(a,b)
            elif instruction == 'mul' and current_block == block:
                self.mul(a, b)
            elif instruction == 'div' and current_block == block:
                self.div(a, b)
            elif instruction == 'mod' and current_block == block:
                self.mod(a, b)
            elif instruction == 'eql' and current_block == block:
                self.eql(a, b)
            # else:
            #     raise ValueError(f'Unexpected instruction {instruction}')


def text2steps(text):
    result = []
    for line in text.split('\n'):
        thisline = line.split(' ')
        if len(thisline) == 3 and thisline[2] not in ('x', 'y', 'z', 'w'):
            thisline[2] = int(thisline[2])
        if len(thisline) ==2:
            thisline.append(None)
        result.append(thisline)
    return result


def load_day_24_data(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath) as f:
        text = f.read()
    return text2steps(text)

if __name__ == '__main__':
    steps = load_day_24_data("day24_real_data.txt")

    xyz_sets = dict()

    # block 0
    for starting_w in range(1, 10):
        alu = Alu(None, steps, w=starting_w)
        alu.do_steps(block=0)
        xyz_sets[tuple([alu.x, alu.y, alu.z])] = [starting_w,]
        # print(f"w input {starting_w} -> {alu.x}, {alu.y}, {alu.z}")

    # block 1
    for block in range(1, 15):
        xyz_sets2 = dict()
        for starting_w in range(1, 10):
            for (x, y, z), path in xyz_sets.items():
                alu = Alu(None, steps, w=starting_w, x=x, y=y, z=z)
                alu.do_steps(block=block)
                key = tuple([alu.x, alu.y, alu.z])
                path_here = deepcopy(path)
                path_here.append(starting_w)
                xyz_sets2[key] = path_here
                # print(f"w input {starting_w} -> {alu.x}, {alu.y}, {alu.z}")
        xyz_sets = xyz_sets2
        print(f"{block} has {len(xyz_sets)}")

    print(xyz_sets)
    print(len(xyz_sets))
