import itertools

import advent_tools


def run_part_1():
    stuff = [num[0] for num in advent_tools.read_all_integers()]
    return sum(stuff)


def run_part_2():
    stuff = [num[0] for num in advent_tools.read_all_integers()]
    recorded = {0}
    summed = 0
    for num in itertools.cycle(stuff):
        summed += num
        if summed in recorded:
            return summed
        recorded.add(summed)


if __name__ == '__main__':
    print(run_part_1()) # 2:14
    print(run_part_2()) # 6:56