import contextlib
import collections
import copy
import functools
import itertools
import numpy as np
import pandas as pd
import re

from matplotlib import pyplot as plt

import advent_tools


def run_generations(init_state, num_gen):
    buffer = num_gen * 2
    state = '.' * buffer + init_state + '.' * buffer
    numbers = range(-buffer, len(init_state) + buffer)
    maps = advent_tools.dict_from_input_file()
    totals = []
    for _ in range(num_gen):
        new_state = '...'
        for i in range(3, len(state) - 3):
            local_state = state[i - 2:i + 3]
            new_state = new_state + maps[local_state]
        state = new_state + '...'
        total = sum(num if plant == '#' else 0 for num, plant in zip(numbers, state))
        totals.append(total)
    return totals


def run_part_1():
    init_state = "#.##.###.#.##...##..#..##....#.#.#.#.##....##..#..####..###.####.##.#..#...#..######.#.....#..##...#"
    totals = run_generations(init_state, 20)
    return totals[-1]


def run_part_2():
    num_gen = 200
    init_state = "#.##.###.#.##...##..#..##....#.#.#.#.##....##..#..####..###.####.##.#..#...#..######.#.....#..##...#"
    totals = run_generations(init_state, num_gen)
    m = totals[-1] - totals[-2]
    b = totals[-1] - m * (num_gen -1)
    y = [m * x + b for x in range(num_gen)]
    plt.plot(totals)
    plt.plot(y)
    plt.show()
    return m * (50000000000 - 1) + b


if __name__ == '__main__':
    print(run_part_1())
    print(run_part_2())