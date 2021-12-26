import unittest

import day13


class TestCollisions(unittest.TestCase):

    def test_get_underlying_map_vertical(self):
        start_pos = ["|", "v", "|", "|", "|", "^", "|"]
        expec_map = ["|", "|", "|", "|", "|", "|", "|"]
        expec_carts = {(0, 1): ("v", 0), (0, 5): ("^", 0)}
        calc_map, carts = day13.get_underlying_map(start_pos)
        self.assertEqual(expec_map, calc_map)
        self.assertEqual(expec_carts, carts)

    def test_get_underlying_map_horizontal(self):
        start_pos = ["->---<-"]
        expec_map = ["-------"]
        expec_carts = {(1, 0): (">", 0), (5, 0): ("<", 0)}
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
        expec_carts = {(0, 2): ("v", 0), (0, 4): ("^", 0)}
        underlying_map, carts = day13.get_underlying_map(start_pos)
        crash, carts = day13.take_one_step(underlying_map, carts)
        self.assertEqual(None, crash)
        self.assertEqual(expec_carts, carts)

    def test_vert_track_crash(self):
        start_pos = ["|", "|", "v", "|", "^", "|", "|"]
        underlying_map, carts = day13.get_underlying_map(start_pos)
        end_pos = day13.take_one_step(underlying_map, carts)
        self.assertEqual(((0, 3), None), end_pos)

    def test_horiz_track_step1(self):
        start_pos = ["->---<-"]
        expec_carts = {(2, 0): (">", 0), (4, 0): ("<", 0)}
        underlying_map, carts = day13.get_underlying_map(start_pos)
        crash, carts = day13.take_one_step(underlying_map, carts)
        self.assertEqual(None, crash)
        self.assertEqual(expec_carts, carts)

    def test_horiz_track_crash(self):
        start_pos = ["-->-<--"]
        underlying_map, carts = day13.get_underlying_map(start_pos)
        end_pos = day13.take_one_step(underlying_map, carts)
        self.assertEqual(((3, 0), None), end_pos)

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
        _, carts = day13.get_underlying_map(prev_pos)
        expec_carts = {(4, 0): ('v', 0), (10, 4): ('>', 0)}
        crash, carts = day13.take_one_step(underlying_map, carts)
        self.assertEqual(None, crash)
        self.assertEqual(expec_carts, carts)


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
