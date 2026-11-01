from pathlib import Path
import unittest
from unittest.mock import patch

from src.main._2024.day22 import Day22 as Day

class TestDay22(unittest.TestCase):

    def setUp(self):
        self.my_dir: Path = Path(__file__).parent.resolve()

    def test_sample_input(self):
        solver = Day()
        with open(f"{self.my_dir}/day22_01.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        self.assertEqual(solver.part_one(), 37327623)

    def test_sample_input_three(self):
        solver = Day()
        with open(f"{self.my_dir}/day22_03.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        self.assertEqual(solver.part_two(), 23)

if __name__ == '__main__':
    unittest.main()
