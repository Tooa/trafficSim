#!/usr/bin/env python3.4
import sys
import random
from os import listdir
from os.path import isfile, join

import numpy as np

from animation import Animation
from walker import Walker
from grid import Grid
from config import Cell
from ioutil import parse_map, parse_simulation_params


class Simulation(object):
    """Enables to load different simulations from file to show the actual animation"""
    def __init__(self, simulation_name, additional_sim_params):
        self.grid = None
        self.walkers = []
        self.simulation_params = parse_simulation_params(simulation_name, additional_sim_params)
        self.load_simulation()

        self.animation = Animation(self.grid, self.animation_step, self.simulation_params["step_interval"],
                                   self.simulation_params["show_potential"])

    def load_simulation(self):
        num_walkers = self.simulation_params["num_rnd_walkers"]
        #Load targets
        self.grid = Grid(*parse_map(self.simulation_params["mapfile"]), targets=self.simulation_params["targets"])

        #Load predefined walkers
        for w in self.simulation_params["walkers"]:
            pos = w["pos"]
            direction = w.get("direction", 9)
            time = w.get("orientation_time", 0)
            pot_name = w.get("target_name", None)
            self.add_walker(pos, pot_name, direction, time)

        #Generate random walkers
        if num_walkers > 0:
            self.generate_random_walkers()

    def run(self):
        self.animation.start_animation()

    def animation_step(self):
        cnt = 0
        while True:
            cnt += 1
            for walker in self.walkers:
                walker.walk()

                if walker.has_target_reached:
                    self.walkers.remove(walker)

            #All workers removed from list
            if not self.walkers:
                print("Simulation ended after %d steps." % cnt)
                exit(0)
            yield

    def add_walker(self, pos, target=None, direction=9, time=0):
        target_names = [t["name"] for t in self.simulation_params["targets"]]
        target = random.choice(target_names) if target is None else target

        direction = np.random.randint(1, 10) if direction == 0 else direction

        min_time = self.simulation_params["rnd_walkers_orientation_time_min"]
        max_time = self.simulation_params["rnd_walkers_orientation_time_max"]
        time = np.random.randint(min_time, max_time + 1) if time == -1 else time
        psway = self.simulation_params["psway"]

        self.walkers.append(Walker(self.grid, pos, psway, target, direction, time))

    def generate_random_walkers(self):
        number_of_workers = self.simulation_params["num_rnd_walkers"]

        x_pairs, y_pairs = np.where(self.grid.mat == Cell.EMPTY)
        free_cells = [(x, y) for x, y in zip(x_pairs, y_pairs)]

        length = len(free_cells)
        #Get some indices for where we could place the walkers
        indices = list(range(length))
        np.random.shuffle(indices)

        target = self.simulation_params.get("rnd_walkers_target", None)
        direction = self.simulation_params.get("rnd_walkers_direction", 0)

        for i in indices[:number_of_workers]:
            pos = free_cells[i]
            self.add_walker(pos, target, direction, -1)


if __name__ == "__main__":
    #No params were given, just print possible sim files
    if len(sys.argv) == 1:
        simulation_files = [f for f in listdir("simulations") if isfile(join("simulations", f)) and f.endswith(".sim")]
        print(simulation_files)
    elif len(sys.argv) >= 2:
        m = Simulation(sys.argv[1], sys.argv[2:])
        m.run()
