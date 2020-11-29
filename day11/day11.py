import contextlib
import collections
import copy
import functools
import itertools
import numpy as np
import pandas as pd
import re

import advent_tools

def power_level(x, y, serial):
    power = (((x + 10) * y + serial) * (x + 10) // 100) % 10 - 5
    return power


def total_power(x, y, serial):
    return sum(power_level(x + del_x, y + del_y, serial)
               for del_x in range(3) for del_y in range(3))


def max_power(serial):
    result = (0, 0, -15)
    for x in range(1, 298):
        for y in range(1, 298):
            power = total_power(x, y, serial)
            if power > result[2]:
                result = (x, y, power)
    return result


def total_power2(x, y, size, serial):
    return sum(power_level(x + del_x, y + del_y, serial)
               for del_x in range(size) for del_y in range(size))

def max_power2(serial):
    result = (0, 0, 1, -15)
    for x in range(1, 298):
        for y in range(1, 298):
            max_size = min((300 - x + 1, 300 - y + 1))
            for size in range(1, max_size + 1):
                power = total_power2(x, y, size, serial)
                if power > result[3]:
                    result = (x, y, size, power)
    return result

def run_part_1():
    return max_power(9810)

def run_part_2():
    # return total_power2(90, 269, 16, 18)
    grid = advent_tools.PlottingGrid((301, 301))
    for x in range(1, 301):
        for y in range(1, 301):
            grid.grid[y, x] = power_level(x, y, 9810)
    maximum = -10
    old_val = ()
    for size in range(1, 300):
        windows = sum(grid.grid[y:y-size+1 or None, x:x-size+1 or None] for x in range(size) for y in range(size))
        old_max = maximum
        maximum = int(windows.max())
        location = np.where(windows == maximum)
        print(location[1][0], location[0][0], size, maximum)
        # if maximum < old_max:
        #     return old_val
        # else:
        #     old_val = val

if __name__ == '__main__':
    print(run_part_1())
    print(run_part_2())