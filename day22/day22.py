import os.path

ON = 1
OFF = -1


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
    cube = set()
    for step in steps:
        state, x_range, y_range, z_range = step
        x_range = make_range(x_range)
        y_range = make_range(y_range)
        z_range = make_range(z_range)
        if x_range and y_range and z_range:
            for x in range(*x_range):
                for y in range(*y_range):
                    for z in range(*z_range):
                        if state == ON:
                            cube.add((x, y, z))
                        else:
                            if (x, y, z) in cube:
                                cube.remove((x, y, z))
        print("Executed {} length now {}".format(step, len(cube)))
    return cube

# --------------

class Region(object):

    def __init__(self, state, x_range, y_range, z_range):
        super(Region, self).__init__()
        self.x_min, self.x_max = x_range
        self.y_min, self.y_max = y_range
        self.z_min, self.z_max = z_range
        self.state = 1 if state == ON else -1

    def __repr__(self):
        return "Region({}, {}, {}, {})".format(self.state, (self.x_min, self.x_max), (self.y_min, self.y_max), (self.z_min, self.z_max))

    @property
    def lights_on(self):
        return (self.x_max + 1 - self.x_min) * (self.y_max + 1 - self.y_min) * (self.z_max + 1 - self.z_min)


def lines2steps(lines):
    result = []
    for line in lines:
        state, locations = line.split()
        x, y, z = locations.split(',')
        result.append([
            ON if state == 'on' else OFF,
            tuple(int(i) for i in x[2:].split('..')),
            tuple(int(i) for i in y[2:].split('..')),
            tuple(int(i) for i in z[2:].split('..')),
        ])
    return result


def calculate_overlap(new, ext):
    state = OFF if ext.state == 1 else ON
    x_min = max(new.x_min, ext.x_min)
    x_max = min(new.x_max, ext.x_max)
    y_min = max(new.y_min, ext.y_min)
    y_max = min(new.y_max, ext.y_max)
    z_min = max(new.z_min, ext.z_min)
    z_max = min(new.z_max, ext.z_max)
    if (x_min <= x_max) and (y_min <= y_max) and (z_min <= z_max):
        return Region(state, (x_min, x_max), (y_min, y_max), (z_min, z_max))
    return None


if __name__ == '__main__':
    # steps = load_day22_data("day22_test_data.txt")
    # reactor = execute_steps(steps)
    # print("After initialization there are {len(reactor)} cubes on")


    steps = load_day22_data("day22_real_data.txt")
#     # reactor = execute_steps(steps)
#     # print("After initialization there are {} cubes on".format(len(reactor)))
#     regions = []
#
# #     test_lines = """\
# # on x=10..12,y=10..12,z=10..12
# # on x=11..13,y=11..13,z=11..13
# # off x=9..11,y=9..11,z=9..11
# # on x=10..10,y=10..10,z=10..10"""
#     test_lines = """\
# on x=-20..26,y=-36..17,z=-47..7
# on x=-20..33,y=-21..23,z=-26..28
# on x=-22..28,y=-29..23,z=-38..16
# on x=-46..7,y=-6..46,z=-50..-1
# on x=-49..1,y=-3..46,z=-24..28
# on x=2..47,y=-22..22,z=-23..27
# on x=-27..23,y=-28..26,z=-21..29
# on x=-39..5,y=-6..47,z=-3..44
# on x=-30..21,y=-8..43,z=-13..34
# on x=-22..26,y=-27..20,z=-29..19
# off x=-48..-32,y=26..41,z=-47..-37
# on x=-12..35,y=6..50,z=-50..-2
# off x=-48..-32,y=-32..-16,z=-15..-5
# on x=-18..26,y=-33..15,z=-7..46
# off x=-40..-22,y=-38..-28,z=23..41
# on x=-16..35,y=-41..10,z=-47..6
# off x=-32..-23,y=11..30,z=-14..3
# on x=-49..-5,y=-3..45,z=-29..18
# off x=18..30,y=-20..-8,z=-3..13
# on x=-41..9,y=-7..43,z=-33..15"""
#     steps = lines2steps(test_lines.split("\n"))
    # steps = (
    #     (ON, (0, 9), (0, 9), (0, 9)),
    #     (ON, (0, 4), (0, 4), (0, 4)),
    #     (OFF, (0, 4), (0, 4), (0, 4)),
    #     (ON, (0, 4), (0, 4), (0, 4)),
    #     (ON, (-10, -1), (-10, -1), (-10, -1)),

        # (ON, (-20, 33), (-21, 23), (-26, 28)),
        # (ON, (-22, 28), (-29, 23), (-38, 16)),
        # (ON, (-46, 7), (-6, 46), (-50, -1)),
        # (ON, (-49, 1), (-3, 46), (-24, 28)),
        # (ON, (2, 47), (-22, 22), (-23, 27)),
        # (ON, (-27, 23), (-28, 26), (-21, 29)),
        # (ON, (-39, 5), (-6, 47), (-3, 44)),
        # (ON, (-30, 21), (-8, 43), (-13, 34)),
        # (ON, (-22, 26), (-27, 20), (-29, 19)),
        # (OFF, (-48, -32), (26, 41), (-47, -37)),
        # (ON, (-12, 35), (6, 50), (-50, -2)),
        # (OFF, (-48, -32), (-32, -16), (-15, -5)),
        # (ON, (-18, 26), (-33, 15), (-7, 46)),
        # (OFF, (-40, -22), (-38, -28), (23, 41)),
        # (ON, (-16, 35), (-41, 10), (-47, 6)),
        # (OFF, (-32, -23), (11, 30), (-14, 3)),
        # (ON, (-49, -5), (-3, 45), (-29, 18)),
        # (OFF, (18, 30), (-20, -8), (-3, 13)),
        # (ON, (-41, 9), (-7, 43), (-33, 15)),
        # (ON, (-54112, -39298), (-85059, -49293), (-27449, 7877)),
        # (ON, (967, 23432), (45373, 81175), (27513, 53682)),
    # )
    regions = []
    for step in steps:
        state, x_range, y_range, z_range = step
        new_region = Region(*step)
        overlaps = []
        for existing_region in regions:
            overlap_region = calculate_overlap(new_region, existing_region)
            if overlap_region:
                overlaps.append(overlap_region)
        regions.extend(overlaps)
        if new_region.state == ON:
            regions.append(new_region)

        total = sum(region.lights_on * region.state for region in regions)
        print("Executed {} lights on {}".format(step, total))


        # if the new region is ON
        # ... if the new region overlaps something
        # ... ... if the region being overlapped is on - add an 'off' region
        # ... ... if the region being overlapped is off - add an 'on' region
        # finally - add the new region

        # if the new region is OFF
        # ... if the new region overlaps something
        # ... ... if the region being overlapped is off ... add an 'on' region
        # ... ... if the region being overlapped is on ... add an 'off' region
        # finally, do NOT add the new region

    print("And finally....")
    total = sum(region.lights_on * region.state for region in regions)
    print(total)
