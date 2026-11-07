from pathlib import Path
import unittest
from unittest.mock import patch

from src.main._2023.day10 import Day10 as Day

class TestDay10(unittest.TestCase):

    def setUp(self):
        self.my_dir: Path = Path(__file__).parent.resolve()

    def test_sample_input(self):
        solver = Day()
        with open(f"{self.my_dir}/day10_01.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        self.assertEqual(solver.part_one(), 4)

    def test_sample_input_2(self):
        solver = Day()
        with open(f"{self.my_dir}/day10_02.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        self.assertEqual(solver.part_one(), 4)

    def test_sample_input_3(self):
        solver = Day()
        with open(f"{self.my_dir}/day10_03.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        self.assertEqual(solver.part_one(), 8)

    def test_sample_input_4(self):
        solver = Day()
        with open(f"{self.my_dir}/day10_04.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        self.assertEqual(solver.part_one(), 8)

if __name__ == '__main__':
    unittest.main()
