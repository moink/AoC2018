import contextlib
import collections
import copy
import functools
import itertools
import numpy as np
import pandas as pd
import re

import advent_tools

def take_steps(data, num_steps):
    result = []
    for row in data:
        x = row[0] + num_steps * row[2]
        y = row[1] + num_steps * row[3]
        result.append([x, y])
    return result


def get_range(data):
    x_min = min(row[0] for row in data)
    x_max = max(row[0] for row in data)
    y_min = min(row[1] for row in data)
    y_max = max(row[1] for row in data)
    return x_min, x_max, y_min, y_max


def show_grid(data, steps):
    new_data = take_steps(data, steps)
    x_min, x_max, y_min, y_max = get_range(new_data)
    grid = advent_tools.PlottingGrid((y_max - y_min + 1, x_max - x_min + 1))
    for row in new_data:
        grid.grid[row[1] - y_min, row[0] - x_min] = 1
    grid.show()

def run_part_1():
    data = advent_tools.read_all_integers()
    # first_steps = 9800
    # last_steps = 10200
    first_steps = 10020
    last_steps = 10030
    for steps in range(first_steps, last_steps):
        show_grid(data, steps)


def run_part_2():
    pass


if __name__ == '__main__':
    print(run_part_1())
    print(run_part_2())