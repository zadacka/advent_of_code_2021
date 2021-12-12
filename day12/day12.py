from collections import defaultdict
from copy import deepcopy
from itertools import groupby


def build_map(connections):
    map = defaultdict(set)
    for line in connections.split("\n"):
        start, end = line.split("-")
        map[start].add(end)
        map[end].add(start)
    return map


def can_visit(cave, route_so_far, small_cave_visits_allowed=1):
    if cave.isupper():
        return True  # can visit big caves any  number of times
    elif cave == "start":
        return False # cannot visit start more than once
    elif cave == "end":
        return True  # you can always visit end but you will terminate there
    elif cave not in route_so_far:
        return True
    else:
        small_caves = [c for c in route_so_far if c.islower()]
        max_times_a_small_cave_was_visited = max(len(list(g)) for k, g in groupby(sorted(small_caves)))
        return max_times_a_small_cave_was_visited < small_cave_visits_allowed


def calculate_routes(map, small_cave_visits_allowed=1):
    all_routes = []

    def calculate_route(route_so_far):
        """
        This is a closure which makes use of map, all_routes, and small_cave_visits_allowed
        :param route_so_far:
        :return:
        """
        here = route_so_far[-1]
        if here == "end":
            all_routes.append(route_so_far)
            return
        next_options = map[here]
        next_valid = [o for o in next_options if can_visit(o, route_so_far, small_cave_visits_allowed)]
        for next_cave in next_valid:
            route = deepcopy(route_so_far)  # need to copy so we don't mutate list in callee
            route.append(next_cave)
            calculate_route(route)

    route_so_far = ["start"]
    calculate_route(route_so_far)

    return sorted(all_routes)

if __name__ == "__main__":
    cave_connections = """\
we-NX
ys-px
ys-we
px-end
yq-NX
px-NX
yq-px
qk-yq
pr-NX
wq-EY
pr-oe
wq-pr
ys-end
start-we
ys-start
oe-DW
EY-oe
end-oe
pr-yq
pr-we
wq-start
oe-NX
yq-EY
ys-wq
ys-pr"""
    cave_map = build_map(cave_connections)
    routes = calculate_routes(cave_map)
    print("The cave system has {} routes which meet the route conditions.".format(len(routes)))

    # WARNING! This is SLOOOOOOOW!
    more_routes = calculate_routes(cave_map, small_cave_visits_allowed=2)
    print("The cave system has {} routes which meet the route conditions.".format(len(more_routes)))