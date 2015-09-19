import random
import numpy as np

from grid import Grid
from util import is_even, rotate
from config import Direction, Cell, DIAG_COST, NONDIAG_COST


class Walker(object):
    """
    This class represents a walker in the grid.
    """
    def __init__(self, grid, pos, psway, potential_name, direction, orientation_time):
        self.grid = grid
        self.pos = np.array(pos)
        self.direction = direction
        self.psway = psway
        self.potential_name = potential_name
        self.orientation_time = orientation_time

        #The target position
        self.target = None
        #Number of fields remaining to the target position
        self.remaining = 0
        self.has_target_reached = False

        #Occupy position in grid
        assert self.grid[self.pos] == Cell.EMPTY
        self.grid[self.pos] = Cell.WALKER

    def find_empty_cell(self, direction, rot):
        """ checks if self.pos + (direction +- rot) is an empty cell.
        If only one is empty, return the direction and position for it
        If both are empty, decide randomly which one to use.
        If none is empty, return None

        @return
        A (direction, position) tuple for the resulting cell found or (Direction.NONE, None),
        if all concerned cells are occupied.
        """

        # if direction == Direction.NONE:
        #     # if we don't have
        #     return Direction.NONE, None

        pdir = rotate(direction, +rot)
        mdir = rotate(direction, -rot)

        ppos = Grid.neighbour_pos_in_direction(self.pos, pdir)
        mpos = Grid.neighbour_pos_in_direction(self.pos, mdir)

        pempty = self.grid.is_empty(ppos)
        mempty = self.grid.is_empty(mpos)

        pres = (pdir, ppos)
        mres = (mdir, mpos)

        if pempty and mempty:
            # both are free, decide randomly
            return random.choice([pres, mres])
        elif pempty:
            return pres
        elif mempty:
            return mres
        else:
            # none is empty
            return Direction.NONE, None

    def try_cell(self, direction):
        target_dir = direction
        target_pos = Grid.neighbour_pos_in_direction(self.pos, direction)
        #Cell is empty move to it in direction
        if self.grid.is_empty(target_pos):
            return target_dir, target_pos

        if target_dir == Direction.NONE:
            return target_dir, None

        #Otherwise try surrounding fields
        for t in (45, 90):
            target_dir, target_pos = self.find_empty_cell(direction, t)

            # if we can move in the checked directions
            if target_pos is not None:
                return target_dir, target_pos

        #No valid position found
        return Direction.NONE, None

    def find_target(self):
        """
        This method calculates the next move.
        Call it, if the walker is currently not moving
        """

        # Follows the potential if not in orientation phase.
        # Otherwise it tries to follow it's given initial direction.
        if self.orientation_time:
            target_dir = self.direction
        else:
            pot = self.grid.potentials[self.potential_name][tuple(self.pos)]
            target_dir = pot["d"]

        target_dir, target_pos = self.try_cell(target_dir)

        # here we have the following situation:
        # target_dir is either a direction or Direction.NONE
        # target_pos is either a valid position or None
        # both is okay, because moving to None simply means not moving.

        # after the loop, (target_dir, target_pos) either contains a valid direction-position-pair
        # or (Direction.NONE, None) which is both okay
        self.target = target_pos

        # if we have a target
        if target_pos is not None:
            assert self.grid.is_empty(target_pos)
            self.remaining = NONDIAG_COST if is_even(target_dir) else DIAG_COST

            if self.grid[self.target] == Cell.EMPTY:
                # only reserve, if the target cell is empty, otherwise
                # (in case of target cell) do nothing
                self.grid[self.target] = Cell.RESERVED

    def set_pos(self, pos):
        """
        sets the player to a new position and also resets his target (next cell) to
        find a new one.
        """
        assert self.grid[pos] in (Cell.RESERVED, Cell.TARGET, Cell.EMPTY)

        #If we are standing on the target, DO NOT override it
        if self.grid[self.pos] != Cell.TARGET:
            #Free current cell
            self.grid[self.pos] = Cell.EMPTY
        self.pos = pos

        #Set Walker on the new position but do not override target (empty psway)
        if self.grid[self.pos] in (Cell.EMPTY, Cell.RESERVED):
            # ... <=> if cell is not target
            self.grid[self.pos] = Cell.WALKER

        #Reset the target
        self.target = None

    def do_extra_step(self):
        #With a chance of PSWAY, this walker is "pushed" to another cell
        chance = np.random.randint(1, 101)
        if chance <= self.psway:
            #Now choose a random cell
            direction = np.random.randint(1, 9)
            neighbour = Grid.neighbour_pos_in_direction(self.pos, direction)
            if self.grid.is_empty(neighbour):
                self.set_pos(neighbour)

    def walk(self):
        """
        walks one time step
        """

        if self.orientation_time:
            self.orientation_time -= 1

        #Currently no target, so choose one
        if self.target is None:
            self.find_target()

        self.remaining -= 1
        #Got target and waiting time is over, just move
        if self.remaining == 0:
            self.set_pos(self.target)
            self.do_extra_step()

        #Time to die?
        if self.grid[self.pos] == Cell.TARGET:
            self.has_target_reached = True

