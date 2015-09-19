from itertools import product

import numpy as np

from util import encode_rot
from config import DIAG_COST, NONDIAG_COST


def make_graph(grid):
    """Consumes a Grid and creates a list of GridNodes and the graph
       for the path finding. The Graph is represented as a adjacency
       list encoded as dictionary.
    """
    obstacles = grid.find_obstacles()

    nodes = [[GridNode(x, y) for y in range(grid.width)] for x in range(grid.height)]
    graph = {}
    for x, y in product(range(grid.height), range(grid.width)):
        if (x, y) in obstacles: continue

        node = nodes[x][y]
        graph[node] = []
        #Check surrounding nodes
        for i, j in product([-1, 0, 1], [-1, 0, 1]):
            if not (0 <= x + i < grid.height): continue
            if not (0 <= y + j < grid.width): continue
            if (x + i, y + j) in obstacles: continue
            #Don't add the current node to the adjacency list
            if i == 0 and j == 0: continue
            graph[nodes[x][y]].append(nodes[x + i][y + j])
    return graph, nodes


class GridNode(object):
    """Represents a node on the grid.
       x -- x-position of this node on the grid
       y -- y-position of this node on the grid
    """
    def __init__(self, x, y):
        self.g = 99999999999
        self.x = x
        self.y = y
        self.parent = None

    def reset(self):
        self.g = 99999999999
        self.parent = None

    def move_cost(self, other):
        diagonal = abs(self.x - other.x) == 1 and abs(self.y - other.y) == 1
        return DIAG_COST if diagonal else NONDIAG_COST

    def __repr__(self):
        return "(X: {0}, Y: {1}, Cost: {2})".format(self.x, self.y, self.g)


class Dijkstra(object):
    """Implements the dijkstra algorithm to find all shortest paths
       to the sink.
       graph      -- adjacency dictionary representing the graph
       nodes      -- referenced GridNodes by the graph
    """
    def __init__(self, graph, nodes):
        self.graph = graph
        self.nodes = nodes

        self.height = len(nodes)
        self.width = len(nodes[0])

    def calc_potential(self, x, y):
        source = self.nodes[x][y]
        #Calculate all shortest paths to source
        p = self.dijkstra(source)
        #Reset costs and parents
        self.reset_nodes()
        return p

    def reset_nodes(self):
        for x, y in product(range(self.height), range(self.width)):
            self.nodes[x][y].reset()

    def dijkstra(self, source):
        potential = np.zeros(shape=(self.height, self.width), dtype=np.dtype([('x', 'i4'), ('y', 'i4'), ('d', 'i4')]))

        openset = set()
        closedset = set()
        current = source
        current.g = 0
        openset.add(current)
        while openset:
            current = min(openset, key=lambda o: o.g)
            openset.remove(current)
            closedset.add(current)
            for node in self.graph[current]:
                if node in closedset:
                    continue

                openset.add(node)
                new_g = current.g + current.move_cost(node)

                if node.g > new_g:
                    node.g = new_g
                    node.parent = current
                    self._calculate_potential_entry(current, node, potential)
        return potential

    def _calculate_potential_entry(self, current, node, potential):
        direction_x, direction_y = current.x - node.x, current.y - node.y
        potential[node.x, node.y]['x'], potential[node.x, node.y]['y'] = direction_x, direction_y
        potential[node.x, node.y]["d"] = encode_rot(direction_x, direction_y)