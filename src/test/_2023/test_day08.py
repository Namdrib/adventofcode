from pathlib import Path
import unittest
from unittest.mock import patch

from src.main._2023.day08 import Day08 as Day

class TestDay08(unittest.TestCase):

    def setUp(self):
        self.my_dir: Path = Path(__file__).parent.resolve()

    def test_sample_input(self):
        solver = Day()
        with open(f"{self.my_dir}/day08_01.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        self.assertEqual(solver.part_one(), 2)

    def test_sample_input_2(self):
        solver = Day()
        with open(f"{self.my_dir}/day08_02.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        self.assertEqual(solver.part_one(), 6)

    def test_sample_input_3(self):
        solver = Day()
        with open(f"{self.my_dir}/day08_03.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        self.assertEqual(solver.part_two(), 6)

if __name__ == '__main__':
    unittest.main()
