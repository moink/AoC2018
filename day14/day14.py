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


def main():
    advent_tools.TESTING = True
    # data = advent_tools.read_all_integers()
    # data = advent_tools.read_whole_input()
    # data = advent_tools.read_input_lines()
    # data = advent_tools.read_input_no_strip()
    # data = advent_tools.read_dict_from_input_file(sep=' => ', key='left')
    # data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    # data = advent_tools.read_one_int_per_line()
    # data = advent_tools.PlottingGrid.from_file({'.' : 0, '#' : 1})
    # data = advent_tools.read_input_line_groups()
    # data = advent_tools.read_nparray_from_digits()
    print('Part 1:', run_part_1(880751))
    print('Part 2:', run_part_2(880751))


def process_input(data):
    print(data)
    return data


def print_result(result, first_elf_pos, second_elf_pos):
    to_print = []
    for i, val in enumerate(result):
        if i == first_elf_pos:
            to_print.append(f"({val})")
        elif i == second_elf_pos:
            to_print.append(f"[{val}]")
        else:
            to_print.append(f" {val} ")
    print(" ".join(to_print))


def run_part_1(count):
    result = [3, 7]
    first_elf_pos = 0
    second_elf_pos = 1
    steps = count + 10
    while len(result) < steps:
        new_recipe = result[first_elf_pos] + result[second_elf_pos]
        if new_recipe >= 10:
            result.append(new_recipe // 10)
            if len(result) >= steps:
                break
        result.append(new_recipe % 10)
        first_elf_pos = (first_elf_pos + 1 + result[first_elf_pos]) % len(result)
        second_elf_pos = (second_elf_pos + 1 + result[second_elf_pos]) % len(result)
    return "".join(str(num) for num in result[-10:])


def run_part_2(seq):
    seq = [int(char) for char in str(seq)]
    result = [3, 7]
    first_elf_pos = 0
    second_elf_pos = 1
    while result[-len(seq):] != seq:
        new_recipe = result[first_elf_pos] + result[second_elf_pos]
        if new_recipe >= 10:
            result.append(new_recipe // 10)
            if result[-len(seq):] == seq:
                break
        result.append(new_recipe % 10)
        first_elf_pos = (first_elf_pos + 1 + result[first_elf_pos]) % len(result)
        second_elf_pos = (second_elf_pos + 1 + result[second_elf_pos]) % len(result)
    return len(result) - len(seq)



if __name__ == '__main__':
    main()
