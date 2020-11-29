import contextlib
import collections
import copy
import functools
import itertools
import time

import numpy as np
import pandas as pd
import re

import advent_tools


def run_game(num_players, max_marble_num):
    num_marbles = max_marble_num
    scores = collections.defaultdict(int)
    elf = 0
    circle = advent_tools.CircularLinkedList()
    for cur_marble in range(1, num_marbles):
        elf = (elf + 1) % num_players
        if (cur_marble % 23) == 0 and cur_marble != 0:
            scores[elf] = scores[elf] + cur_marble
            circle.move_counterclockwise(8)
            scores[elf] = scores[elf] + circle.current.data
            circle.remove_current_node()
        else:
            circle.add_node_after_current(cur_marble)
        circle.move_clockwise(1)
    return max(scores.values())


def run_part_1():
    return run_game(416, 71975)


def run_part_2():
    return run_game(416, 7197500)


if __name__ == '__main__':
    print(run_part_1())
    print(run_part_2())
