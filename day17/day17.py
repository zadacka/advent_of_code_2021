target_area = 288, 330, -96, -50  # x range, y range


def replace(string, position, character):
    return string[:position] + character + string[position + 1:]


class Target:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max


class Probe:

    def __init__(self, x_velocity, y_velocity, target):
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.x_position = 0
        self.y_position = 0
        self.target = Target(*target)
        self.trajectory = []
        self._calculate_trajectory()

    def _calculate_trajectory(self):
        while self._in_bounds:
            self.trajectory.append((self.x_position, self.y_position))
            self.x_position += self.x_velocity
            self.y_position += self.y_velocity
            self.x_velocity = max(self.x_velocity - 1, 0)
            self.y_velocity -= 1
        self.trajectory.append((self.x_position, self.y_position))  # past the target - useful for aim

    @property
    def lands_inside_target(self):
        def within_target(x, y):
            return self.target.x_min <= x <= self.target.x_max and self.target.y_min <= y <= self.target.y_max

        return any(within_target(x, y) for x, y in self.trajectory)

    @property
    def _in_bounds(self):
        return self.x_position < self.target.x_max and self.y_position > self.target.y_min

    def print_trajectory(self):
        max_x = self.target.x_max + 1
        max_y = max(y for x, y in self.trajectory)
        min_x = 0
        min_y = self.target.y_min - 1

        offset = max_y
        array = ["." * max_x for _ in range(offset - min_y)]

        for y in range(offset - self.target.y_max, 1 + offset - self.target.y_min):
            for x in range(self.target.x_min, 1 + self.target.x_max):
                array[y] = replace(array[y], x, "T")

        for x, y in self.trajectory[:-1]:
            array[offset - y] = replace(array[offset - y], x, '#')

        array[offset] = replace(array[offset], 0, "S")

        result = ""
        for line in array:
            result += line
            result += "\n"
        return result


def calculate_metrics(target_zone, max_x_velocity=350, max_y_velocity=500):
    # ugly brute force approach
    hits = dict()
    for x_velocity in range(0, max_x_velocity):
        for y_velocity in range(-max_y_velocity, max_y_velocity):
            probe = Probe(x_velocity, y_velocity, target_zone)
            if probe.lands_inside_target:
                hits[(x_velocity, y_velocity)] = max(y for x, y in probe.trajectory)
    return max(v for v in hits.values()), len(hits)


if __name__ == '__main__':
    max_height, total_hits = calculate_metrics(target_area)
    print(f"Max height reached: {max_height}")
    print(f"There are {total_hits} different initial velocities which would hit the target.")
