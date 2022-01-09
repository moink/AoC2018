import copy
import sys

import numpy as np
from scipy import signal

import advent_tools

EMPTY = 0
TREES = 1
LUMBERYARD = 2


def main():
    data = LumberGame.from_file({'.': EMPTY, '#': LUMBERYARD, "|": TREES})
    np.set_printoptions(threshold=sys.maxsize)
    print('Part 1:', run_part_1(data))
    data = LumberGame.from_file({'.': EMPTY, '#': LUMBERYARD, "|": TREES})
    print('Part 2:', run_part_2(data))


class LumberGame(advent_tools.GameOfLife):

    def count_neighbours(self):
        lumber_count = signal.convolve(self.grid == LUMBERYARD, self.convolve_matrix,
                                       mode="same").round(0).astype(int)
        tree_count = signal.convolve(self.grid == TREES, self.convolve_matrix,
                                     mode="same").round(0).astype(int)
        return lumber_count, tree_count

    def evaluate_where_on(self, counts):
        lumber_count, tree_count = counts
        # An open acre will become filled with trees if three or more adjacent acres
        # contained trees. Otherwise, nothing happens.
        old_grid = copy.copy(self.grid)
        self.grid[(old_grid == EMPTY) & (tree_count >= 3)] = TREES
        # An acre filled with trees will become a lumberyard if three or more adjacent
        # acres were lumberyards. Otherwise, nothing happens.
        self.grid[(old_grid == TREES) & (lumber_count >= 3)] = LUMBERYARD
        # An acre containing a lumberyard will remain a lumberyard if it was adjacent
        # to at least one other lumberyard and at least one acre containing trees.
        # Otherwise, it becomes open.
        self.grid[
            (old_grid == LUMBERYARD) & ((lumber_count < 1) | (tree_count < 1))] = EMPTY

    def resource_value(self):
        return (self.grid == TREES).sum() * (self.grid == LUMBERYARD).sum()

    def __str__(self):
        return str(self.grid)


def run_part_1(game):
    game.simulate_n_steps(10)
    return game.resource_value()


def run_part_2(game):
    first_seen = {str(game): 0}
    resource_values = {0: game.resource_value()}
    for count in range(1000):
        count += 1
        game.one_step()
        resource_values[count] = game.resource_value()
        if str(game) in first_seen:
            return resource_values[
                ((1000000000 - first_seen[str(game)])
                 % (count - first_seen[str(game)]) + first_seen[str(game)])
            ]
        first_seen[str(game)] = count


if __name__ == '__main__':
    main()
