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
    data = advent_tools.read_all_integers()[0]
    return process_node(data, 0)


def process_node(data, i):
    num_children = data[i]
    num_meta = data[i + 1]
    total = 0
    new_i = i + 2
    for child in range(num_children):
        delta, new_i = process_node(data, new_i)
        total = total + delta
    total = total + sum(data[new_i:new_i+num_meta])
    return total, new_i + num_meta


def run_part_2():
    data = advent_tools.read_all_integers()[0]
    return process_node_part_two(data, 0)


def process_node_part_two(data, i):
    num_children = data[i]
    num_meta = data[i + 1]
    total = 0
    new_i = i + 2
    children = collections.defaultdict(int)
    for child in range(num_children):
        delta, new_i = process_node_part_two(data, new_i)
        children[child] = delta
    if num_children == 0:
        total = sum(data[new_i:new_i+num_meta])
    else:
        for index in data[new_i:new_i+num_meta]:
            total = total + children[index-1]
    return total, new_i + num_meta

if __name__ == '__main__':
    print(run_part_1())
    print(run_part_2())