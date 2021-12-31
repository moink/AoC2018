import contextlib
import collections
import copy
import functools
import itertools
import math
import re
import statistics

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import advent_tools

DRY_SAND = 0
CLAY = 1
WET_SAND = 2
WATER = 3


def main():
    # advent_tools.TESTING = True
    # data = advent_tools.read_all_integers()
    # data = advent_tools.read_whole_input()
    # data = advent_tools.read_input_no_strip()
    # data = advent_tools.read_dict_from_input_file(sep=' => ', key='left')
    # data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    # data = advent_tools.read_one_int_per_line()
    # data = advent_tools.PlottingGrid.from_file({'.' : 0, '#' : 1})
    # data = advent_tools.read_input_line_groups()
    # data = advent_tools.read_nparray_from_digits()
    scan, spring_loc = process_input(advent_tools.read_input_lines())
    part1, part2 = run_both_parts(scan, spring_loc)
    print('Part 1:', part1)
    print('Part 2:', part2)


def process_input(data):
    interim = []
    x_min = np.inf
    x_max = -np.inf
    y_min = np.inf
    y_max = - np.inf
    for line in data:
        first, second = line.split(",")
        first_var, num = first.split("=")
        range_start, range_end = second.split("=")[1].split("..")
        interim.append((first_var, int(num), int(range_start), int(range_end)))
        if first_var == "x":
            if int(num) < x_min:
                x_min = int(num)
            if int(num) > x_max:
                x_max = int(num)
            if int(range_start) < y_min:
                y_min = int(range_start)
            if int(range_end) > y_max:
                y_max = int(range_end)
        else:
            if int(num) < y_min:
                y_min = int(num)
            if int(num) > y_max:
                y_max = int(num)
            if int(range_start) < x_min:
                x_min = int(range_start)
            if int(range_end) > x_max:
                x_max = int(range_end)
    x_min = x_min - 2
    x_max = x_max + 2
    result = advent_tools.PlottingGrid((y_max - y_min + 1, x_max - x_min + 1))
    for first_var, num, range_start, range_end in interim:
        if first_var == "x":
            result.grid[range_start - y_min:range_end - y_min + 1, num - x_min] = CLAY
        else:
            result.grid[num - y_min, range_start - x_min:range_end - x_min + 1] = CLAY
    spring_loc = 500 - x_min
    return result, spring_loc


def run_both_parts(scan, spring_loc):
    scan.grid[0, spring_loc] = WET_SAND
    old_scan = advent_tools.PlottingGrid(scan.grid.shape)
    count = 0
    while (old_scan.grid != scan.grid).any():
        count = count + 1
        if count % 10 == 0:
            print(".", end="")
        if count % 800 == 0:
            print(f"\n{count}")
        old_scan.grid = scan.grid.copy()
        drip_phase(scan)
        spread_phase(scan)
        settle_phase(scan)
    scan.show()
    part_1 = ((scan.grid == WET_SAND) | (scan.grid == WATER)).sum()
    return part_1, (scan.grid == WATER).sum()


def settle_phase(scan):
    r = re.compile(f"{CLAY}[{WET_SAND}]+{CLAY}")
    for j, line in enumerate(scan.grid):
        line_string = re.sub(r'\n|\s', '', np.array_str(line))[1:-1]
        for match in r.finditer(line_string):
            scan.grid[j, match.start() + 1:match.end() - 1] = WATER


def spread_phase(scan):
    cont = True
    while cont:
        cannot_drip = (
                (scan.grid == WET_SAND)
                & (
                        (np.pad(scan.grid[1:] == WATER, ((0, 1), (0, 0)), constant_values=False))
                        | (np.pad(scan.grid[1:] == CLAY, ((0, 1), (0, 0)), constant_values=False)))
        )
        spread_to = ((np.roll(cannot_drip, -1, axis=1)
                      | np.roll(cannot_drip, 1, axis=1))
                     & (scan.grid == DRY_SAND))
        where_spread_to = np.where(spread_to)
        cont = where_spread_to[0].any()
        if cont:
            lowest_wet = where_spread_to[0].max()
            scan.grid[lowest_wet, spread_to[lowest_wet]] = WET_SAND


def drip_phase(scan):
    old_scan = advent_tools.PlottingGrid(scan.grid.shape)
    while (scan.grid != old_scan.grid).any():
        old_scan.grid = copy.copy(scan.grid)
        drip_location = (
                np.pad(scan.grid[:-1] == WET_SAND, ((1, 0), (0, 0)), constant_values=False)
                & (scan.grid == DRY_SAND)
        )
        if drip_location.any():
            scan.grid[drip_location] = WET_SAND


def run_part_2(scan, spring_loc):
    pass


if __name__ == '__main__':
    main()
