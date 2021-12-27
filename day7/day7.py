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
    # advent_tools.TESTING = True
    # data = advent_tools.read_all_integers()
    # data = advent_tools.read_whole_input()
    data = advent_tools.read_input_lines()
    # data = advent_tools.read_input_no_strip()
    # data = advent_tools.read_dict_from_input_file(sep=' => ', key='left')
    # data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    # data = advent_tools.read_one_int_per_line()
    # data = advent_tools.PlottingGrid.from_file({'.' : 0, '#' : 1})
    # data = advent_tools.read_input_line_groups()
    # data = advent_tools.read_nparray_from_digits()
    data = process_input(data)
    print('Part 1:', run_part_1(copy.deepcopy(data)))
    print('Part 2:', run_part_2(data, num_workers=5))


def process_input(data):
    result = collections.defaultdict(set)
    for line in data:
        words = line.split()
        result[words[-3]].add(words[1])
    return result


def run_part_1(dependencies):
    not_done = {val for dep in dependencies.values()
                for val in dep}.union(dependencies.keys())
    completed = []
    while not_done:
        for step in sorted(not_done):
            if not dependencies[step]:
                completed.append(step)
                not_done.remove(step)
                for dep in dependencies.values():
                    with contextlib.suppress(KeyError):
                        dep.remove(step)
                break
    return "".join(completed)


def run_part_2(dependencies, num_workers=2):
    not_started = {val for dep in dependencies.values()
                for val in dep}.union(dependencies.keys())
    completion_times = collections.defaultdict(set)
    available = {step for step in sorted(not_started) if not dependencies[step]}
    tick = 0
    for worker in range(num_workers):
        if available:
            to_do = sorted(available)[0]
            not_started.remove(to_do)
            available.remove(to_do)
            completion_times[ord(to_do) - 4 + tick].add(to_do)
    while completion_times:
        tick = sorted(completion_times)[0]
        not_started = not_started.difference(completion_times[tick])
        for step, dep in dependencies.items():
            with contextlib.suppress(KeyError):
                dependencies[step] = dep.difference(completion_times[tick])
        available = available.union(
            {step for step in sorted(not_started) if not dependencies[step]}).difference(
            completion_times[tick]
        )
        del completion_times[tick]
        for worker in range(num_workers - len(completion_times)):
            if available:
                to_do = sorted(available)[0]
                available.remove(to_do)
                not_started.remove(to_do)
                completion_times[ord(to_do) - 4 + tick].add(to_do)
    return tick




if __name__ == '__main__':
    main()
