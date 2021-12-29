import unittest

import numpy as np
from numpy.testing import assert_equal

import advent_tools
import day15


class MyTestCase(unittest.TestCase):
    def test_get_units(self):
        lines = [
            "#########",
            "#G..G..G#",
            "#.......#",
            "#.......#",
            "#G..E..G#",
            "#.......#",
            "#.......#",
            "#G..G..G#",
            "#########",
        ]
        grid = advent_tools.PlottingGrid.from_lines(lines, day15.CHAR_MAP)
        units = day15.get_units(grid)
        expected_result = [
            day15.Unit((1, 1), 200, day15.GOBLIN),
            day15.Unit((1, 4), 200, day15.GOBLIN),
            day15.Unit((1, 7), 200, day15.GOBLIN),
            day15.Unit((4, 1), 200, day15.GOBLIN),
            day15.Unit((4, 4), 200, day15.ELF),
            day15.Unit((4, 7), 200, day15.GOBLIN),
            day15.Unit((7, 1), 200, day15.GOBLIN),
            day15.Unit((7, 4), 200, day15.GOBLIN),
            day15.Unit((7, 7), 200, day15.GOBLIN),
        ]
        self.assertEqual(expected_result, units)

    def test_find_in_range(self):
        lines = [
            "#######",
            "#E..G.#",
            "#...#.#",
            "#.G.#G#",
            "#######",
        ]
        grid = advent_tools.PlottingGrid.from_lines(lines, day15.CHAR_MAP)
        in_range = day15.find_in_range(grid, day15.GOBLIN)
        expected_result = np.asarray([
            [False, False, False, False, False, False, False],
            [False, False, False, True, False, True, False],
            [False, False, True, False, False, True, False],
            [False, True, False, True, False, False, False],
            [False, False, False, False, False, False, False],
        ])
        assert_equal(expected_result, in_range.grid)

    def test_get_next_pos(self):
        lines = [
            "#######",
            "#E..G.#",
            "#...#.#",
            "#.G.#G#",
            "#######",
        ]
        grid = advent_tools.PlottingGrid.from_lines(lines, day15.CHAR_MAP)
        in_range = day15.find_in_range(grid, day15.GOBLIN)
        next_pos = day15.get_next_pos(grid.grid, in_range.grid, (1, 1))
        assert_equal((1, 2), next_pos)

    def test_get_next_pos_2(self):
        lines = [
            "#########",
            "#.G.G..G#",
            "#.......#",
            "#.......#",
            "#G..E..G#",
            "#.......#",
            "#.......#",
            "#G..G..G#",
            "#########",
        ]
        grid = advent_tools.PlottingGrid.from_lines(lines, day15.CHAR_MAP)
        in_range = day15.find_in_range(grid, day15.ELF)
        next_pos = day15.get_next_pos(grid.grid, in_range.grid, (1, 4))
        self.assertEqual((2, 4), next_pos)

    def test_get_next_pos_3(self):
        lines = [
            "#########",
            "#.G....G#",
            "#...G...#",
            "#.......#",
            "#G..E..G#",
            "#.......#",
            "#.......#",
            "#G..G..G#",
            "#########",
        ]
        grid = advent_tools.PlottingGrid.from_lines(lines, day15.CHAR_MAP)
        in_range = day15.find_in_range(grid, day15.ELF)
        next_pos = day15.get_next_pos(grid.grid, in_range.grid, (1, 7))
        self.assertEqual((1, 6), next_pos)

    def test_get_next_pos_4(self):
        lines = [
            "#########",
            "#.G...G.#",
            "#...G...#",
            "#.......#",
            "#G..E..G#",
            "#.......#",
            "#.......#",
            "#G..G..G#",
            "#########",
        ]
        grid = advent_tools.PlottingGrid.from_lines(lines, day15.CHAR_MAP)
        in_range = day15.find_in_range(grid, day15.ELF)
        next_pos = day15.get_next_pos(grid.grid, in_range.grid, (4, 2))
        self.assertEqual((4, 3), next_pos)

    def test_get_next_pos_5(self):
        lines = [
            "#########",
            "#.G...G.#",
            "#...G...#",
            "#.......#",
            "#G..E..G#",
            "#.......#",
            "#.......#",
            "#G..G..G#",
            "#########",
        ]
        grid = advent_tools.PlottingGrid.from_lines(lines, day15.CHAR_MAP)
        in_range = day15.find_in_range(grid, day15.ELF)
        next_pos = day15.get_next_pos(grid.grid, in_range.grid, (4, 4))
        self.assertEqual((3, 4), next_pos)

    def test_get_next_pos_6(self):
        lines = [
            "#########",
            "#.G...G.#",
            "#...G...#",
            "#...E...#",
            "#G.....G#",
            "#.......#",
            "#.......#",
            "#G..G..G#",
            "#########",
        ]
        grid = advent_tools.PlottingGrid.from_lines(lines, day15.CHAR_MAP)
        in_range = day15.find_in_range(grid, day15.ELF)
        next_pos = day15.get_next_pos(grid.grid, in_range.grid, (4, 7))
        self.assertEqual((3, 7), next_pos)

    def test_run_one_round(self):
        lines = [
            "#########",
            "#G..G..G#",
            "#.......#",
            "#.......#",
            "#G..E..G#",
            "#.......#",
            "#.......#",
            "#G..G..G#",
            "#########",
        ]
        grid = advent_tools.PlottingGrid.from_lines(lines, day15.CHAR_MAP)
        units = day15.get_units(grid)
        expec_lines = [
            "#########",
            "#.G...G.#",
            "#...G...#",
            "#...E..G#",
            "#.G.....#",
            "#.......#",
            "#G..G..G#",
            "#.......#",
            "#########",
        ]
        expec_grid = advent_tools.PlottingGrid.from_lines(expec_lines, day15.CHAR_MAP)
        result_map, units = day15.run_one_round(grid, units)
        assert_equal(expec_grid.grid, result_map.grid)

if __name__ == '__main__':
    unittest.main()
