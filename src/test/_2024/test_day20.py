from pathlib import Path
import unittest
from unittest.mock import patch

from src.main._2024.day20 import Day20 as Day

class TestDay20(unittest.TestCase):

    def setUp(self):
        self.my_dir: Path = Path(__file__).parent.resolve()

    def test_sample_input(self):
        solver = Day(savings_threshold_ps=100)
        with open(f"{self.my_dir}/day20_01.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        part_one_results: dict = solver.calculate_cheat_benefits(2)
        # The key is how many picoseconds are saved
        # The value is how many cheats there are that save this number of picoseconds
        num_cheats_saving_time: dict = {
            2: 14,
            4: 14,
            6: 2,
            8: 4,
            10: 2,
            12: 3,
            20: 1,
            36: 1,
            38: 1,
            40: 1,
            64: 1,
        }

        for savings_ps, count in num_cheats_saving_time.items():
            with self.subTest(f"part 1 cheat_savings={savings_ps} picoseconds"):
                num_cheats: int = sum(1 for x in part_one_results.values() if x == savings_ps)
                self.assertEqual(num_cheats, count)

        part_two_results: dict = solver.calculate_cheat_benefits(20)
        # The key is how many picoseconds are saved
        # The value is how many cheats there are that save this number of picoseconds
        num_cheats_saving_time: dict = {
            50: 32,
            52: 31,
            54: 29,
            56: 39,
            58: 25,
            60: 23,
            62: 20,
            64: 19,
            66: 12,
            68: 14,
            70: 12,
            72: 22,
            74: 4,
            76: 3,
        }

        for savings_ps, count in num_cheats_saving_time.items():
            with self.subTest(f"part 2 cheat_savings={savings_ps} picoseconds"):
                num_cheats: int = sum(1 for x in part_two_results.values() if x == savings_ps)
                self.assertEqual(num_cheats, count)

if __name__ == '__main__':
    unittest.main()
