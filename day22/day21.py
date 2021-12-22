import os.path
from itertools import chain

ON = 1
OFF = 0


def load_day22_data(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    result = []
    with open(filepath) as f:
        for line in f.readlines():
            state, locations = line.split()
            x, y, z = locations.split(',')
            result.append([
                ON if state == 'on' else OFF,
                tuple(int(i) for i in x[2:].split('..')),
                tuple(int(i) for i in y[2:].split('..')),
                tuple(int(i) for i in z[2:].split('..')),
            ]
            )
    return result

cube_size = 50

def execute_steps(steps):
    starting_cube = [[ [OFF for _ in range(-cube_size, cube_size)] for _ in range(-cube_size, cube_size)] for _ in range(-cube_size, cube_size)]
    for step in steps:
        state, (x_start, x_end), (y_start, y_end), (z_start, z_end) = step

        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                for z in range(z_start, z_end + 1):
                    starting_cube[x][y][z] = state
    return starting_cube

def report_on(reactor):
    on_cubes = []
    for x in range(-cube_size, cube_size):
        for y in range(-cube_size, cube_size):
            for z in range(-cube_size, cube_size):
                if reactor[x][y][z] == ON:
                    on_cubes.append((x, y, z))
    return on_cubes

def calc_on_cubes(reactor):
    total = 0
    for row in reactor:
        for column in row:
                total += sum(column)
    return total


# if __name__ == '__main__':
