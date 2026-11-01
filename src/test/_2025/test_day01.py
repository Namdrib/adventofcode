from pathlib import Path
import unittest
from unittest.mock import patch

from src.main._2025.day01 import Day01

class TestDay01(unittest.TestCase):

    def setUp(self):
        self.my_dir: Path = Path(__file__).parent.resolve()

    def test_day_01_01_in(self):
        solver = Day01()
        with open(f"{self.my_dir}/day01_01.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        self.assertEqual(solver.part_one(), 3)
        self.assertEqual(solver.part_two(), 6)

if __name__ == '__main__':
    unittest.main()
