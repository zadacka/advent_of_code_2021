import os.path
from collections import deque
from operator import itemgetter


def load_risks(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath) as f:
        risks = [[int(element) for element in line.strip()] for line in f.readlines()]
    return risks


def embiggen_risks(risks, n=5):
    rows = len(risks) * n
    original_rows = len(risks)
    original_cols = len(risks[0])
    columns = len(risks[0]) * n
    mega_risks = [[0] * columns for _ in range(rows)]
    for row in range(rows):
        for column in range(columns):
            r_adjustment, r_idx = divmod(row, original_rows)
            c_adjustment, c_idx = divmod(column, original_cols)
            original = risks[r_idx][c_idx]
            adjusted = original + r_adjustment + c_adjustment
            mega_risks[row][column] = adjusted - 9 if adjusted > 9 else adjusted
    return mega_risks


def get_unverified_neighbours(node, unverified_nodes):
    r, c = node
    potential_neighbours = {
        # (r - 1, c - 1), (r, c - 1), (r + 1, c),
        # (r, c - 1), (r + 1, c),
        # (r - 1, c + 1), (r, c + 1), (r + 1, c + 1),
        (r, c - 1),
        (r, c - 1), (r + 1, c),
        (r, c + 1),
    }
    return unverified_nodes.intersection(potential_neighbours)


def get_path(risks):
    start_node = (0, 0)
    end_node = (len(risks) - 1, len(risks[0]) - 1)

    previous = dict()
    accumulated_risk = dict()
    risk_lookup = dict()

    unverified_nodes = set()
    for row_index, row in enumerate(risks):
        for column_index, element in enumerate(row):
            node = (row_index, column_index)
            unverified_nodes.add(node)
            risk_lookup[node] = element
            accumulated_risk[node] = float("inf")
            previous[node] = None

    accumulated_risk[start_node] = 0

    while unverified_nodes:
        node = get_vertex_in_unverified_nodes_with_min_risk(accumulated_risk, unverified_nodes)

        if node == end_node:
            path = deque()
            path.append(end_node)
            previous_node = previous[node]
            while previous_node != start_node:
                path.appendleft(previous_node)
                previous_node = previous[previous_node]
            path.appendleft(start_node)
            return list(path)

        unverified_nodes.remove(node)
        for neighbour in get_unverified_neighbours(node, unverified_nodes):
            this_risk = accumulated_risk[node] + risk_lookup[neighbour]
            if this_risk < accumulated_risk[neighbour]:
                accumulated_risk[neighbour] = this_risk
                previous[neighbour] = node


def get_vertex_in_unverified_nodes_with_min_risk(accumulated_risk, unverified_nodes):
    sorted_node_risks = sorted(accumulated_risk.items(), key=itemgetter(1), reverse=True)
    return [k for k, v in sorted_node_risks if k in unverified_nodes].pop()


def heuristic(neighbour, end_node):
    x1, y1 = neighbour
    x2, y2 = end_node
    return abs(x1 - x2) + abs(y1 - y2)


def get_path_astar(risks):
    start_node = (0, 0)
    end_node = (len(risks) - 1, len(risks[0]) - 1)

    previous = dict()
    accumulated_risk = dict()
    risk_lookup = dict()

    unverified_nodes = set()
    for row_index, row in enumerate(risks):
        for column_index, element in enumerate(row):
            node = (row_index, column_index)
            unverified_nodes.add(node)
            risk_lookup[node] = element
            accumulated_risk[node] = float("inf")
            previous[node] = None

    accumulated_risk[start_node] = 0

    while unverified_nodes:
        node = get_vertex_in_unverified_nodes_with_min_risk(accumulated_risk, unverified_nodes)

        if node == end_node:
            path = deque()
            path.append(end_node)
            previous_node = previous[node]
            while previous_node != start_node:
                path.appendleft(previous_node)
                previous_node = previous[previous_node]
            path.appendleft(start_node)
            return list(path)

        unverified_nodes.remove(node)
        for neighbour in get_unverified_neighbours(node, unverified_nodes):
            this_risk = accumulated_risk[node] + risk_lookup[neighbour]
            if this_risk < accumulated_risk[neighbour]:
                accumulated_risk[neighbour] = this_risk + heuristic(neighbour, end_node)
                previous[neighbour] = node


def score_path(path, risks):
    total = 0
    for node in path[1:]:
        r, c = node
        total += risks[r][c]
    return total


# weight
#
# def get_path_a_star(risks):
#     import heapq
#     dis = dict()
#     risk_lookup = dict()
#
#     queue = []
#
#     for row_index, row in enumerate(risks):
#         for column_index, element in enumerate(row):
#             node = (row_index, column_index)
#             risk_lookup[node] = element
#             dis[node] = float("inf")
#
#     start = (0, 0)
#     dis[start] = 0
#
#     heapq.heappush(queue, )
#     for
# 1. Assign dis[v] for all nodes = INT_MAX (distance from root node + heuristics of every node).
# 2. Assign dis[root] = 0 + heuristic(root, goal) (distance from root node to itself + heuristics).
# 2. Add root node to priority queue.
# 3. Loop on the queue as long as it's not empty.
# 1. In every loop, choose the node with the minimum distance from the root node in the queue + heuristic (root node will be selected first).
# 2. Remove the current chosen node from the queue (vis[current] = true).
# 3. If the current node is the goal node, then return it.
# 4. For every child of the current node, do the following:
# 1. Assign temp = distance(root, current) + distance(current, child) + heuristic(child, goal).
# 2. If temp < dis[child], then, assign dist[child] = temp. This denotes a shorter path to child node has been found.
# 3. And, add child node to the queue if not already in the queue (thus, it's now marked as not visited again).
# 4. If queue is empty, then goal node was not found!


if __name__ == '__main__':
    # PART 1
    # risks = load_risks("day15_real_data.txt")
    # path = get_path(risks)
    # score = score_path(path, risks)
    # print("The shortest path from start to finish has a risk of {}".format(score))

    # PART 2 (too slow)
    risks = load_risks("day15_real_data.txt")
    embiggened_risks = embiggen_risks(risks)
    path = get_path_astar(embiggened_risks)
    score = score_path(path, embiggened_risks)
    print("The shortest path from start to finish for the BIG cave has a risk of {}".format(score))

    #  PART 2 Proof of Concept (different solver = managealbe solution)
    # from pathfinding.finder.a_star import AStarFinder
    # from pathfinding.core.grid import Grid
    # risks = load_risks("day15_real_data.txt")
    # embiggened_risks = embiggen_risks(risks)
    # grid = Grid(matrix=embiggened_risks)
    # start = grid.node(0, 0)
    # end = grid.node(len(embiggened_risks)-1, len(embiggened_risks)-1)
    # finder = AStarFinder()
    # path, runs = finder.find_path(start, end, grid)
    # flipped_path = [(r, c) for c, r in path]
    # print("Cheating ... the megapath has a risk of {}".format(score_path(flipped_path, embiggened_risks)))
