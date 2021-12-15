import os.path
from collections import defaultdict, deque
from operator import itemgetter


def load_risks(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath) as f:
        risks = [[int(element) for element in line.strip()] for line in f.readlines()]
    return risks


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
    end_node = (len(risks)-1, len(risks[0])-1)

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

def score_path(path, risks):
    total = 0
    for node in path[1:]:
        r, c = node
        total += risks[r][c]
    return total

if __name__ == '__main__':
    risks = load_risks("day15_real_data.txt")
    path = get_path(risks)
    score = score_path(path, risks)
    print("The shortest path from start to finish has a risk of {}".format(score))
