from pathlib import Path
import unittest
from unittest.mock import patch

from src.main._2024.day12 import Day12 as Day

class TestDay12(unittest.TestCase):

    def setUp(self):
        self.my_dir: Path = Path(__file__).parent.resolve()

    def test_sample_input(self):
        solver = Day()
        with open(f"{self.my_dir}/day12_01.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        self.assertEqual(solver.part_one(), 140)
        self.assertEqual(solver.part_two(), 80)

    def test_sample_input_2(self):
        solver = Day()
        with open(f"{self.my_dir}/day12_02.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        self.assertEqual(solver.part_one(), 772)
        self.assertEqual(solver.part_two(), 436)

    def test_sample_input_3(self):
        solver = Day()
        with open(f"{self.my_dir}/day12_03.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        self.assertEqual(solver.part_one(), 1930)

if __name__ == '__main__':
    unittest.main()
