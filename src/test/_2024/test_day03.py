from pathlib import Path
import unittest
from unittest.mock import patch

from src.main._2024 import day03
from src.main._2024.day03 import Day03 as Day

class TestDay03(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.test_day = day03.Day03()

    def setUp(self):
        self.my_dir: Path = Path(__file__).parent.resolve()

    def test_sample_input(self):
        solver = Day()
        with open(f"{self.my_dir}/day03_01.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        self.assertEqual(solver.part_one(), 161)

    def test_sample_input_part_2(self):
        solver = Day()
        with open(f"{self.my_dir}/day03_02.in") as f:
            with patch('sys.stdin', f):
                solver.read_input()

        self.assertEqual(solver.part_two(), 48)

    def test_mul_pattern(self):
        item: str = 'mul(1,2)andmul[2,3]mul(1),sum(3,4)mul(mul(4,5),mul(6,7))mul(!,2)'
        output = self.test_day.mul_pattern.findall(item)
        self.assertListEqual(output, ['mul(1,2)', 'mul(4,5)', 'mul(6,7)'])

    def test_mul_with_able_pattern(self):
        item: str = "mul(1,2)anddo()_n't())mul[2,3]mul(1)don't()sum(3,4)mul(4,5)mul(X,Y)"
        output = self.test_day.mul_with_able_pattern.findall(item)
        self.assertListEqual(output, ['mul(1,2)', 'do()', "don't()", 'mul(4,5)'])

    def test_run_multiply(self):
        items = {
            'mul(44,46)': 2024,
            'mul(123,4)': 492,
        }

        for input_, output in items.items():
            with self.subTest(in_=input_):
                self.assertEqual(self.test_day.run_multiply(input_), output)
