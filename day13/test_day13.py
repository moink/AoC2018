import unittest

import day13


class TestCollisions(unittest.TestCase):

    def test_get_underlying_map_vertical(self):
        start_pos = ["|", "v", "|", "|", "|", "^", "|"]
        expec_map = ["|", "|", "|", "|", "|", "|", "|"]
        expec_carts = {(0, 1): 0, (0, 5): 0}
        calc_map, carts = day13.get_underlying_map(start_pos)
        self.assertEqual(expec_map, calc_map)
        self.assertEqual(expec_carts, carts)

    def test_get_underlying_map_horizontal(self):
        start_pos = ["->---<-"]
        expec_map = ["-------"]
        expec_carts = {(1, 0): 0, (5, 0): 0}
        calc_map, carts = day13.get_underlying_map(start_pos)
        self.assertEqual(expec_map, calc_map)
        self.assertEqual(expec_carts, carts)

    def test_get_underlying_map_complex(self):
        start_pos = [
            r"/-----\ ",
            r"|     | ",
            r"|  /--+--\ ",
            r"|  |  |  | ",
            r"\--+--/  | ",
            r"   |     | ",
            r"   \-----/ ",
        ]
        expec_map = [
            r"/-----\ ",
            r"|     | ",
            r"|  /--+--\ ",
            r"|  |  |  | ",
            r"\--+--/  | ",
            r"   |     | ",
            r"   \-----/ ",
        ]
        expec_carts = {}
        calc_map, carts = day13.get_underlying_map(start_pos)
        self.assertEqual(expec_map, calc_map)
        self.assertEqual(expec_carts, carts)

    def test_vert_track_step1(self):
        start_pos = ["|", "v", "|", "|", "|", "^", "|"]
        expec_end = ["|", "|", "v", "|", "^", "|", "|"]
        expec_carts = {(0, 2): 0, (0, 4): 0}
        underlying_map, carts = day13.get_underlying_map(start_pos)
        end_pos, crash, carts = day13.take_one_step(start_pos, underlying_map, carts)
        self.assertEqual(expec_end, end_pos)
        self.assertEqual(None, crash)
        self.assertEqual(expec_carts, carts)

    def test_vert_track_crash(self):
        start_pos = ["|", "|", "v", "|", "^", "|", "|"]
        expec_end = ["|", "|", "|", "X", "|", "|", "|"]
        underlying_map, carts = day13.get_underlying_map(start_pos)
        end_pos = day13.take_one_step(start_pos, underlying_map, carts)
        self.assertEqual((expec_end, (0, 3), None), end_pos)

    def test_horiz_track_step1(self):
        start_pos = ["->---<-"]
        expec_end = ["-->-<--"]
        expec_carts = {(2, 0): 0, (4, 0): 0}
        underlying_map, carts = day13.get_underlying_map(start_pos)
        end_pos, crash, carts = day13.take_one_step(start_pos, underlying_map, carts)
        self.assertEqual(expec_end, end_pos)
        self.assertEqual(None, crash)
        self.assertEqual(expec_carts, carts)

    def test_horiz_track_crash(self):
        start_pos = ["-->-<--"]
        expec_end = ["---X---"]
        underlying_map, carts = day13.get_underlying_map(start_pos)
        end_pos = day13.take_one_step(start_pos, underlying_map, carts)
        self.assertEqual((expec_end, (3, 0), None), end_pos)

class TestLongerExample(unittest.TestCase):

    def test_complex_map_step(self):
        start_pos = [
            r"/->-\         ",
            r"|   |  /----\ ",
            r"| /-+--+-\  | ",
            r"| | |  | v  | ",
            r"\-+-/  \-+--/ ",
            r"  \------/    ",
        ]
        prev_pos = [
            r"/-->\         ",
            r"|   |  /----\ ",
            r"| /-+--+-\  | ",
            r"| | |  | |  | ",
            r"\-+-/  \->--/ ",
            r"  \------/    ",
        ]
        expec_end = [
            r"/---v         ",
            r"|   |  /----\ ",
            r"| /-+--+-\  | ",
            r"| | |  | |  | ",
            r"\-+-/  \-+>-/ ",
            r"  \------/    ",
        ]
        underlying_map, _ = day13.get_underlying_map(start_pos)
        carts = {(3, 0): 0, (9, 4): 0}
        expec_carts = {(4, 0): 0, (10, 4): 0}
        end_pos, crash, carts = day13.take_one_step(
            prev_pos, underlying_map, carts
        )
        self.assertEqual(expec_end, end_pos)
        self.assertEqual(None, crash)
        self.assertEqual(expec_carts, carts)

    def test_intermediate_steps(self):
        steps = [
            [
                r"/->-\         ",
                r"|   |  /----\ ",
                r"| /-+--+-\  | ",
                r"| | |  | v  | ",
                r"\-+-/  \-+--/ ",
                r"  \------/    ",
            ],
            [
                r"/-->\         ",
                r"|   |  /----\ ",
                r"| /-+--+-\  | ",
                r"| | |  | |  | ",
                r"\-+-/  \->--/ ",
                r"  \------/    ",
            ],
            [
                r"/---v         ",
                r"|   |  /----\ ",
                r"| /-+--+-\  | ",
                r"| | |  | |  | ",
                r"\-+-/  \-+>-/ ",
                r"  \------/    ",
            ],
            [
                r"/---\         ",
                r"|   v  /----\ ",
                r"| /-+--+-\  | ",
                r"| | |  | |  | ",
                r"\-+-/  \-+->/ ",
                r"  \------/    ",
            ],
            [
                r"/---\         ",
                r"|   |  /----\ ",
                r"| /->--+-\  | ",
                r"| | |  | |  | ",
                r"\-+-/  \-+--^ ",
                r"  \------/    ",
            ],
            [
                r"/---\         ",
                r"|   |  /----\ ",
                r"| /-+>-+-\  | ",
                r"| | |  | |  ^ ",
                r"\-+-/  \-+--/ ",
                r"  \------/    ",
            ],
            [
                r"/---\         ",
                r"|   |  /----\ ",
                r"| /-+->+-\  ^ ",
                r"| | |  | |  | ",
                r"\-+-/  \-+--/ ",
                r"  \------/    ",
            ],
            [
                r"/---\         ",
                r"|   |  /----< ",
                r"| /-+-->-\  | ",
                r"| | |  | |  | ",
                r"\-+-/  \-+--/ ",
                r"  \------/    ",
            ],
            [
                r"/---\         ",
                r"|   |  /---<\ ",
                r"| /-+--+>\  | ",
                r"| | |  | |  | ",
                r"\-+-/  \-+--/ ",
                r"  \------/    ",
            ],
            [
                r"/---\         ",
                r"|   |  /--<-\ ",
                r"| /-+--+-v  | ",
                r"| | |  | |  | ",
                r"\-+-/  \-+--/ ",
                r"  \------/    ",
            ],
            [
                r"/---\         ",
                r"|   |  /-<--\ ",
                r"| /-+--+-\  | ",
                r"| | |  | v  | ",
                r"\-+-/  \-+--/ ",
                r"  \------/    ",
            ],
            [
                r"/---\         ",
                r"|   |  /<---\ ",
                r"| /-+--+-\  | ",
                r"| | |  | |  | ",
                r"\-+-/  \-<--/ ",
                r"  \------/    ",
            ],
            [
                r"/---\         ",
                r"|   |  v----\ ",
                r"| /-+--+-\  | ",
                r"| | |  | |  | ",
                r"\-+-/  \<+--/ ",
                r"  \------/    ",
            ],
            [
                r"/---\         ",
                r"|   |  /----\ ",
                r"| /-+--v-\  | ",
                r"| | |  | |  | ",
                r"\-+-/  ^-+--/ ",
                r"  \------/    ",
            ],
            [
                r"/---\         ",
                r"|   |  /----\ ",
                r"| /-+--+-\  | ",
                r"| | |  X |  | ",
                r"\-+-/  \-+--/ ",
                r"  \------/    ",
            ],
        ]
        underlying_map, carts = day13.get_underlying_map(steps[0])
        for prev_pos, expec_end in zip(steps[0:-2], steps[1:-1]):
            end_pos, crash, carts = day13.take_one_step(
                prev_pos, underlying_map, carts
            )
            self.assertEqual(expec_end, end_pos)
            self.assertEqual(None, crash)
        prev_pos = steps[-2]
        expec_end = steps[-1]
        end_pos, crash, carts = day13.take_one_step(
            prev_pos, underlying_map, carts
        )
        self.assertEqual(expec_end, end_pos)
        self.assertEqual((7, 3), crash)

    def test_part_1_example(self):
        start_pos = [
            r"/->-\         ",
            r"|   |  /----\ ",
            r"| /-+--+-\  | ",
            r"| | |  | v  | ",
            r"\-+-/  \-+--/ ",
            r"  \------/    ",
        ]
        result = day13.run_part_1(start_pos)
        self.assertEqual((7, 3), result)


if __name__ == '__main__':
    unittest.main()
