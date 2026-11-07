from pathlib import Path
import unittest
from unittest.mock import patch

from src.main._2023.day07 import Day07 as Day

class TestDay07(unittest.TestCase):

    def setUp(self):
        self.my_dir: Path = Path(__file__).parent.resolve()

    def test_sample_input(self):
        solver = Day()
        with open(f"{self.my_dir}/day07_01.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        self.assertEqual(solver.part_one(), 6440)
        self.assertEqual(solver.part_two(), 5905)

if __name__ == '__main__':
    unittest.main()
