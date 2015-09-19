from itertools import product

import numpy as np

from util import decode_rot
from config import Cell
from dijkstra import make_graph, Dijkstra


class Grid(object):
    """Represents the field for the walkers

       data    -- contains the map representation according to config.Cell.
                 Use ioutil.parse_map to generate the input.
       width   -- the width of the given map data
       height  -- the height of the given map data
       targets -- list of targets for which a potential should be generateted
    """
    def __init__(self, data, width, height, targets):
        self.mat = np.array(data, dtype="int32").reshape(height, width)
        self.potentials = {}

        graph, nodes = make_graph(self)
        self.pathfinding = Dijkstra(graph, nodes)
        self.generate_potential_for_targets(targets)

    def generate_potential_for_targets(self, targets):
        #Generate potential fields
        for target in targets:
            x, y = target["pos"]
            if not self.is_empty(target["pos"]):
                raise RuntimeError("Tried to place a target on an occupied cell")

            p = self.pathfinding.calc_potential(x, y)
            self.potentials[target["name"]] = p
            #Place Target on map
            self.mat[x, y] = Cell.TARGET

    def is_empty(self, pos):
        x, y = pos[0], pos[1]
        return self.mat[x, y] in (Cell.EMPTY, Cell.TARGET)

    @staticmethod
    def neighbour_pos_in_direction(pos, direction):
        return pos + decode_rot(direction)

    @property
    def width(self):
        return self.mat.shape[1]

    @property
    def height(self):
        return self.mat.shape[0]

    def find_obstacles(self):
        """Returns a list of tuple containing the obstacles of the map (including the outer borders)"""
        return [(x, y) for x, y in product(range(self.height), range(self.width)) if self.mat[x, y] == Cell.WALL]

    def __getitem__(self, pos):
        return self.mat[tuple(pos)]

    def __setitem__(self, pos, val):
        self.mat[tuple(pos)] = val

