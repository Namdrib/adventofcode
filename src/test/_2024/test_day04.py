from pathlib import Path
import unittest
from unittest.mock import patch

from src.main._2024.day04 import Day04 as Day

class TestDay04(unittest.TestCase):

    def setUp(self):
        self.my_dir: Path = Path(__file__).parent.resolve()

    def test_sample_input(self):
        solver = Day()
        with open(f"{self.my_dir}/day04_01.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        self.assertEqual(solver.part_one(), 18)
        self.assertEqual(solver.part_two(), 9)

if __name__ == '__main__':
    unittest.main()
