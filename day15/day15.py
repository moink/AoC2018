import collections
import copy
import dataclasses
from operator import attrgetter

import numpy as np

import advent_tools

START_HIT_POINTS = 200
DEFAULT_ATTACK = 3

EMPTY = 0
WALL = 1
ELF = 2
GOBLIN = 3

CHAR_MAP = {'.': EMPTY, '#': WALL, "E": ELF, "G": GOBLIN}

ENEMIES = {ELF: GOBLIN, GOBLIN: ELF}

ADJACENCIES = [(-1, 0), (0, -1), (0, 1), (1, 0)]


@dataclasses.dataclass
class Unit:
    current_position: tuple
    hit_points: int
    attack: int
    race: int
    alive: bool


def main():
    start_map = advent_tools.PlottingGrid.from_file(CHAR_MAP)
    print('Part 1:', run_part_1(copy.deepcopy(start_map)))
    print('Part 2:', run_part_2(start_map))


def run_part_1(start_map):
    units = get_units(start_map)
    num_elves, outcome = run_fight(start_map, units)
    return outcome


def run_part_2(start_map):
    lower_bound = DEFAULT_ATTACK
    upper_bound = 100
    outcome_upper = None
    while upper_bound - lower_bound > 1:
        elf_attack = (lower_bound + upper_bound) // 2
        this_map = copy.deepcopy(start_map)
        units = get_units(this_map, elf_attack)
        start_elves = sum(1 for unit in units if unit.race == ELF)
        num_elves, outcome = run_fight(this_map, units)
        if num_elves == start_elves:
            upper_bound = elf_attack
            outcome_upper = outcome
        else:
            lower_bound = elf_attack
    return outcome_upper


def run_fight(start_map, units):
    num_goblins = sum(1 for unit in units if unit.race == GOBLIN)
    num_elves = sum(1 for unit in units if unit.race == ELF)
    count = 0
    while num_goblins and num_elves:
        start_map, units = run_one_round(start_map, units)
        num_goblins = sum(1 for unit in units if unit.race == GOBLIN)
        num_elves = sum(1 for unit in units if unit.race == ELF)
        if num_goblins and num_elves:
            count = count + 1
    sum_hp = sum(unit.hit_points for unit in units)
    return num_elves, sum_hp * count


def get_units(data, elf_attack=3):
    units = []
    rows, cols = data.grid.shape
    for j in range(rows):
        for i in range(cols):
            val = data.grid[(j, i)]
            if val == GOBLIN:
                units.append(Unit((j, i), START_HIT_POINTS, DEFAULT_ATTACK, val, True))
            elif val == ELF:
                units.append(Unit((j, i), START_HIT_POINTS, elf_attack, val, True))
    return units


def find_in_range(grid, enemy):
    next_to_enemy = (
        (np.roll(grid.grid, 1, 0) == enemy) |
        (np.roll(grid.grid, -1, 0) == enemy) |
        (np.roll(grid.grid, 1, 1) == enemy) |
        (np.roll(grid.grid, -1, 1) == enemy)
    )
    in_range = next_to_enemy & (grid.grid == EMPTY)
    result = advent_tools.PlottingGrid(in_range.shape)
    result.grid = in_range
    return result


def get_next_pos(start_map, in_range, start_pos):
    queue = collections.deque([start_pos])
    discovered = {start_pos: 0}
    destinations = {}
    parents = collections.defaultdict(set)
    while queue:
        current = queue.popleft()
        if in_range[current]:
            destinations[current] = discovered[current]
        else:
            i, j = current
            for delta_i, delta_j, in ADJACENCIES:
                ii = i + delta_i
                jj = j + delta_j
                new_node = (ii, jj)
                if start_map[new_node] == EMPTY:
                    if new_node not in discovered:
                        discovered[new_node] = discovered[current] + 1
                        queue.append(new_node)
                        parents[new_node].add(current)
                    else:
                        discovered[new_node] = min(
                            discovered[new_node], discovered[current] + 1)
                        if not parents[new_node]:
                            parents[new_node].add(current)
                        else:
                            min_parent = min(discovered[parent] for parent in parents[new_node])
                            if discovered[current] == min_parent:
                                parents[new_node].add(current)
    if not destinations:
        return start_pos
    goal_pos = min(dest for dest, dist in destinations.items()
                   if dist == min(destinations.values()))
    path = [goal_pos]
    while start_pos not in parents[path[-1]]:
        parent_dists = {parent: discovered[parent] for parent in (parents[path[-1]])}
        path.append(min(parent for parent, dist in parent_dists.items()
                        if dist == min(parent_dists.values())))
    return path[-1]


def attack(unit, units, start_map):
    targets = find_targets(unit, units)
    if targets:
        min_hit_points = min(target.hit_points for target in targets)
        lowest_hp_targets = [
            target for target in targets if target.hit_points == min_hit_points
        ]
        target = min(lowest_hp_targets, key=attrgetter("current_position"))
        target.hit_points -= unit.attack
        if target.hit_points <= 0:
            target.alive = False
            start_map.grid[target.current_position] = EMPTY


def find_targets(unit, units):
    i, j = unit.current_position
    targets = []
    for delta_i, delta_j, in ADJACENCIES:
        ii = i + delta_i
        jj = j + delta_j
        for enemy_unit in units:
            if (
                enemy_unit.current_position == (ii, jj)
                and enemy_unit.race == ENEMIES[unit.race]
                and enemy_unit.alive
            ):
                targets.append(enemy_unit)
                break
    return targets


def run_one_round(start_map, units):
    for unit in sorted(units, key=attrgetter("current_position")):
        if unit.alive:
            in_range = find_in_range(start_map, ENEMIES[unit.race])
            targets = find_targets(unit, units)
            if not targets:
                next_step = get_next_pos(
                    start_map.grid, in_range.grid, unit.current_position
                )
                start_map.grid[unit.current_position] = EMPTY
                start_map.grid[next_step] = unit.race
                unit.current_position = next_step
                targets = find_targets(unit, units)
            if targets:
                attack(unit, units, start_map)
    units = [unit for unit in units if unit.alive]
    return start_map, units


if __name__ == '__main__':
    main()
