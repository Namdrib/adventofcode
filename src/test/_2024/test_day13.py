from pathlib import Path
import unittest
from unittest.mock import patch

from src.main._2024.day13 import Day13 as Day

class TestDay13(unittest.TestCase):

    def setUp(self):
        self.my_dir: Path = Path(__file__).parent.resolve()

    def test_sample_input(self):
        solver = Day()
        with open(f"{self.my_dir}/day13_01.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        self.assertEqual(solver.part_one(), 480)
        # Part 2 is just super large - there is no example answer for this input

if __name__ == '__main__':
    unittest.main()
