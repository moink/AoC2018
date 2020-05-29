import contextlib
import collections
import copy
import functools
import itertools
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt

import advent_tools


def run_part_1():
    lines = advent_tools.read_all_integers()
    grid = np.zeros((1000, 1000))
    for elf_num, x, y, width, height in lines:
        grid[x:x+width, y:y+height] = grid[x:x+width, y:y+height] + 1
    plt.imshow(grid)
    plt.show()
    return (grid > 1).sum().sum()


def run_part_2():
    lines = advent_tools.read_all_integers()
    grid = np.zeros((1000, 1000))
    for elf_num, x, y, width, height in lines:
        grid[x:x + width, y:y + height] = grid[x:x + width, y:y + height] + 1
    for elf_num, x, y, width, height in lines:
        max_num = grid[x:x + width, y:y + height].max().max()
        if max_num == 1:
            return elf_num


if __name__ == '__main__':
    # print(run_part_1()) # 10:20
    print(run_part_2()) # 11:34