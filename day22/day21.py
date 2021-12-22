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


def make_range(dim_range):
    range_min, range_max = dim_range
    range_min = max(-cube_size, range_min)
    range_max = min(cube_size, range_max)
    if range_max >= range_min:
        return range_min, range_max + 1
    else:
        return None


def execute_steps(steps):
    starting_cube = [[[OFF for _ in range(-cube_size, cube_size)] for _ in range(-cube_size, cube_size)] for _ in
                     range(-cube_size, cube_size)]
    for step in steps:
        state, x_range, y_range, z_range = step
        x_range = make_range(x_range)
        y_range = make_range(y_range)
        z_range = make_range(z_range)
        if x_range and y_range and z_range:
            for x in range(*x_range):
                for y in range(*y_range):
                    for z in range(*z_range):
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

if __name__ == '__main__':
    steps = load_day22_data("day22_real_data.txt")
    reactor=  execute_steps(steps)
    print(f"After initialization there are {calc_on_cubes(reactor)} cubes on")
