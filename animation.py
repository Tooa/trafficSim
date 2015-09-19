from config import Cell, Direction

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
from matplotlib.figure import figaspect


class Animation(object):
    """Wraps the matplotlib matrix to visualize the grid as animated matrix"""
    def __init__(self, grid, animation_step, step_interval, arrow_for_potential):
        self.grid = grid
        self.animation_step = animation_step
        self.arrow_potential = arrow_for_potential

        #Setup subplots
        aspect = figaspect(1)
        self.figure, self.axis = plt.subplots(figsize=1.5 * aspect)
        self.arrows = self.place_arrows()

        self.animated_matrix = self.axis.matshow(self.grid.mat, vmin=Cell.RESERVED, vmax=Direction.RIGHT,
                                                 cmap=cm.Paired)

        self.animation = animation.FuncAnimation(self.figure, self.update_view, self.animation_step,
                                                 init_func=self.update_view,
                                                 interval=step_interval,
                                                 save_count=0, blit=True)

    def start_animation(self):
        plt.show()

    def place_arrows(self):
        # arrows
        shape = self.grid.mat.shape
        u, v = np.zeros(shape), np.zeros(shape)

        # arrow positions
        x, y = np.mgrid[0:self.grid.height, 0:self.grid.width]

        for (i, j), val in np.ndenumerate(self.grid.potentials[self.arrow_potential]):
            u[i, j] = val["y"]
            v[i, j] = -val["x"]

        return self.axis.quiver(y, x, u, v, alpha=0.5)

    def update_view(self, anim_data=None):
        self.animated_matrix.set_data(self.grid.mat)
        return self.animated_matrix, self.arrows
