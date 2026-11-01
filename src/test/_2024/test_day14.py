from pathlib import Path
import unittest
from unittest.mock import patch

from src.main._2024.day14 import Day14 as Day

class TestDay14(unittest.TestCase):

    def setUp(self):
        self.my_dir: Path = Path(__file__).parent.resolve()

    def test_sample_input(self):
        solver = Day(11, 7)
        with open(f"{self.my_dir}/day14_01.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        self.assertEqual(solver.part_one(), 12)
        # Part 2 is letting it run for a long time on the full input

if __name__ == '__main__':
    unittest.main()
