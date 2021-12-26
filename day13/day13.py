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

MINE_MARKERS = {
    "v": "|",
    "^": "|",
    ">": "-",
    "<": "-"
}

CART_STEP_MAP = {
    ("v", "|"): "v",
    ("v", "/"): "<",
    ("v", "\\"): ">",
    ("^", "|"): "^",
    ("^", "/"): ">",
    ("^", "\\"): "<",
    (">", "-"): ">",
    (">", "\\"): "v",
    (">", "/"): "^",
    ("<", "-"): "<",
    ("<", "/"): "v",
    ("<", "\\"): "^",
}

INTERSECTION_MAP = {
    ("v", 0): ">",
    ("v", 1): "v",
    ("v", 2): "<",
    (">", 0): "^",
    (">", 1): ">",
    (">", 2): "v",
    ("^", 0): "<",
    ("^", 1): "^",
    ("^", 2): ">",
    ("<", 0): "v",
    ("<", 1): "<",
    ("<", 2): "^",
}



def main():
    # advent_tools.TESTING = True
    # data = advent_tools.read_all_integers()
    # data = advent_tools.read_whole_input()
    # data = advent_tools.read_input_lines()
    data = advent_tools.read_input_no_strip()
    # data = advent_tools.read_dict_from_input_file(sep=' => ', key='left')
    # data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    # data = advent_tools.read_one_int_per_line()
    # data = advent_tools.PlottingGrid.from_file({'.' : 0, '#' : 1})
    # data = advent_tools.read_input_line_groups()
    data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    return data


def run_part_1(curr_map):
    underlying_map, carts = get_underlying_map(curr_map)
    crash = None
    while crash is None:
        curr_map, crash, carts = take_one_step(curr_map, underlying_map, carts)
    return crash


def get_underlying_map(start_pos):
    char_map = {char: char for char in r"/\|- +"}
    char_map.update(MINE_MARKERS)
    map = []
    carts = {}
    for j, line in enumerate(start_pos):
        row = []
        for i, char in enumerate(line):
            row.append(char_map[char])
            if char in MINE_MARKERS:
                carts[(i, j)] = 0
        map.append("".join(row))
    return map, carts


def take_one_step(start_pos, underlying_map, old_carts):
    n_cols = len(start_pos[0])
    result = [[char for char in line] for line in start_pos]
    carts = {}
    for i in range(n_cols):
        for j, line in enumerate(start_pos):
            char = line[i]
            if char == "v":
                result[j][i] = underlying_map[j][i]
                next_char = result[j + 1][i]
                if next_char in MINE_MARKERS:
                    result[j + 1][i] = "X"
                    return ["".join(line) for line in result], (i, j + 1), None
                if next_char == "+":
                    fill_char = INTERSECTION_MAP[(char, old_carts[(i, j)])]
                    carts[(i, j + 1)] = (old_carts[(i, j)] + 1) % 3
                else:
                    fill_char = CART_STEP_MAP[(char, next_char)]
                    carts[(i, j + 1)] = old_carts[(i, j)]
                result[j + 1][i] = fill_char
            if char == "^":
                result[j][i] = underlying_map[j][i]
                next_char = result[j - 1][i]
                if next_char in MINE_MARKERS:
                    result[j - 1][i] = "X"
                    return ["".join(line) for line in result], (i, j - 1), None
                if next_char == "+":
                    fill_char = INTERSECTION_MAP[(char, old_carts[(i, j)])]
                    carts[(i, j - 1)] = (old_carts[(i, j)] + 1) % 3
                else:
                    fill_char = CART_STEP_MAP[(char, next_char)]
                    carts[(i, j - 1)] = old_carts[(i, j)]
                result[j - 1][i] = fill_char
            if char == ">":
                result[j][i] = underlying_map[j][i]
                next_char = result[j][i + 1]
                if next_char in MINE_MARKERS:
                    result[j][i + 1] = "X"
                    return ["".join(line) for line in result], (i + 1, j), None
                if next_char == "+":
                    fill_char = INTERSECTION_MAP[(char, old_carts[(i, j)])]
                    carts[(i + 1, j)] = (old_carts[(i, j)] + 1) % 3
                else:
                    fill_char = CART_STEP_MAP[(char, next_char)]
                    carts[(i + 1, j)] = old_carts[(i, j)]
                result[j][i + 1] = fill_char
            if char == "<":
                result[j][i] = underlying_map[j][i]
                next_char = result[j][i - 1]
                if next_char in MINE_MARKERS:
                    result[j][i - 1] = "X"
                    return ["".join(line) for line in result], (i - 1, j), None
                if next_char == "+":
                    fill_char = INTERSECTION_MAP[(char, old_carts[(i, j)])]
                    carts[(i - 1, j)] = (old_carts[(i, j)] + 1) % 3
                else:
                    fill_char = CART_STEP_MAP[(char, next_char)]
                    carts[(i - 1, j)] = old_carts[(i, j)]
                result[j][i - 1] = fill_char
    return ["".join(line) for line in result], None, carts



def run_part_2(data):
    pass


if __name__ == '__main__':
    main()