import contextlib
import collections
import copy
import functools
import itertools
import numpy as np
import pandas as pd
import re

import advent_tools


def run_part_1():
    lines = advent_tools.read_input_lines()
    two_count = 0
    three_count = 0
    for line in lines:
        counter = collections.Counter(line)
        has_two = 0
        has_three = 0
        for _, num in counter.items():
            if num == 2:
                has_two = 1
            if num == 3:
                has_three = 1
        two_count += has_two
        three_count += has_three
    return two_count * three_count


def run_part_2():
    lines = advent_tools.read_input_lines()
    min_diff = 99
    best_found = None
    for first, second in itertools.combinations(lines, 2):
        difference = 0
        for char1, char2 in zip(first, second):
            if char1 != char2:
                difference += 1
        if difference < min_diff:
            min_diff = difference
            best_found = (first, second)
    first, second = best_found
    result = []
    for char1, char2 in zip(first, second):
        if char1 == char2:
            result.append(char1)
    return ''.join(result)





if __name__ == '__main__':
    print(run_part_1())  # 3:28
    print(run_part_2())  # 9:31