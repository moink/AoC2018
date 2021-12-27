import contextlib
import collections
import copy

import advent_tools


def main():
    input_data = advent_tools.read_input_lines()
    dependencies = process_input(input_data)
    print('Part 1:', run_part_1(copy.deepcopy(dependencies)))
    print('Part 2:', run_part_2(dependencies, num_workers=5))


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
    available = set()
    completion_times[0] = set()
    tick = 0
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
