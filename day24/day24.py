import os.path
from collections import deque


class Alu(object):

    def __init__(self, input_string, steps) -> None:
        super().__init__()
        self.input_buffer = deque([int(x) for x in input_string])
        self.steps = steps
        self.x = 0
        self.y = 0
        self.z = 0
        self.w = 0

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

    def do_steps(self):
        for (instruction, a, b) in self.steps:
            if instruction == 'inp':
                self.input(a)
            elif instruction == 'add':
                self.add(a,b)
            elif instruction == 'mul':
                self.mul(a, b)
            elif instruction == 'div':
                self.div(a, b)
            elif instruction == 'mod':
                self.mod(a, b)
            elif instruction == 'eql':
                self.eql(a, b)
            else:
                raise ValueError(f'Unexpected instruction {instruction}')


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
    for potential_model_number in range(99999999999999, 0, -1):
        str_model_no = str(potential_model_number)
        if '0' in str_model_no:
            continue
        else:
            # print(f'trying {str_model_no}')
            alu = Alu(str_model_no, steps)
            alu.do_steps()
            if alu.z == 0:
                print(f"The submarine model is {str_model_no}")
                break
