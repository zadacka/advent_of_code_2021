import os.path

ON = 1
OFF = -1


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


def load_day22_data(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath) as f:
        return lines2steps(f.readlines())


class Region(object):

    def __init__(self, state, x_range, y_range, z_range):
        super(Region, self).__init__()
        self.x_min, self.x_max = x_range
        self.y_min, self.y_max = y_range
        self.z_min, self.z_max = z_range
        self.state = 1 if state == ON else -1

    def __repr__(self):
        template = "Region({}, {}, {}, {})"
        return template.format(self.state, (self.x_min, self.x_max), (self.y_min, self.y_max), (self.z_min, self.z_max))

    @property
    def lights_on(self):
        return (self.x_max + 1 - self.x_min) * (self.y_max + 1 - self.y_min) * (self.z_max + 1 - self.z_min)


def outside_initialization_region(step):
    state, (x_min, x_max), (y_min, y_max), (z_min, z_max) = step
    return x_min > 50 or x_max < -50 or y_min > 50 or y_max < -50 or z_min > 50 or z_max < 50


def execute_steps(steps, initialize=True):
    """
    Thought process....
    if the new region is ON
    ... if the new region overlaps something
    ... ... if the region being overlapped is on - add an 'off' region
    ... ... if the region being overlapped is off - add an 'on' region
    finally - add the new region

    elif the new region is OFF
    ... if the new region overlaps something
    ... ... if the region being overlapped is off ... add an 'on' region
    ... ... if the region being overlapped is on ... add an 'off' region
    finally, do NOT add the new region
    """
    regions = []
    for step in steps:
        if initialize and outside_initialization_region(step):
            continue  # skip this step
        new_region = Region(*step)
        overlaps = []
        for existing_region in regions:
            overlap_region = calculate_overlap(new_region, existing_region)
            if overlap_region:
                overlaps.append(overlap_region)
        regions.extend(overlaps)
        if new_region.state == ON:
            regions.append(new_region)
    return sum(region.lights_on * region.state for region in regions)


def calculate_overlap(new, ext):
    state = OFF if ext.state == 1 else ON  # flip state
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
    steps = load_day22_data("day22_real_data.txt")
    total = execute_steps(steps)
    print(total)
