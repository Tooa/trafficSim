from enum import IntEnum

#Different costs for a move on the grid
DIAG_COST = 3
NONDIAG_COST = 2

#Path where the sim files are stored
SIMULATIONS_PATH = "simulations"


class Cell(IntEnum):
    """ Intern representation for the matrix
    RESERVED -- indicates that the cell
                is reserved for a walker
    TARGET   -- the actual target for the walkers
    WALL     -- field which is not accessible for a walker
    EMPTY    -- indicates free fields on the grid
    WALKER   -- represents a walker on the cell
    """
    RESERVED = -3
    TARGET = -2
    WALL = -1
    EMPTY = 0
    WALKER = 1


class Direction(IntEnum):
    """ Encodes the walk direction for the walkers
    """
    NONE = 9
    RIGHT = 1
    BOTTOM_RIGHT = 2
    BOTTOM = 3
    BOTTOM_LEFT = 4
    LEFT = 5
    TOP_LEFT = 6
    TOP = 7
    TOP_RIGHT = 8


#Maps the walk directions to direction vectors
DIR_VEC_MAPPING = {(0, 0): Direction.NONE,
                   (0, 1): Direction.RIGHT,
                   (1, 1): Direction.BOTTOM_RIGHT,
                   (1, 0): Direction.BOTTOM,
                   (1, -1): Direction.BOTTOM_LEFT,
                   (0, -1): Direction.LEFT,
                   (-1, -1): Direction.TOP_LEFT,
                   (-1, 0): Direction.TOP,
                   (-1, 1): Direction.TOP_RIGHT}

#Representation for the map format
CONVERSIONS = {"W": Cell.WALL, " ": Cell.EMPTY}
