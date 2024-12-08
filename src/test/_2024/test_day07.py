import unittest

from src.main._2024 import day07

class TestDay07(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.test_day = day07.Day07()

    def test_can_be_made_part_one(self):
        test_cases: list = [
            (29, [10, 19], "10 + 19"),
            (190, [10, 19], "10 * 19"),
            (24, [1, 2, 3, 4], "1 * 2 * 3 * 4"),
            (24, [4, 3, 2, 1], "4 * 3 * 2 * 1"),
            (10, [1, 2, 3, 4], "1 + 2 + 3 + 4"),
            (13, [1, 2, 3, 4], "1 + 2 * 3 + 4"),
        ]

        for target, operands, msg in test_cases:
            with self.subTest(target=target, operands=operands, msg=msg):
                self.assertTrue(self.test_day.can_be_made(target, operands, False))

    def test_can_be_made_part_one_sad(self):
        test_cases: list = [
            (1019, [10, 19], "Not concatenating"),
            (20, [10, 19], "Not adding 1 for the first element"),
            (19, [10, 19], "Not multiplying by 1 for the first element"),
            (1019, [10, 19], "Not concatenating"),
            (0, [1, 2, 3, 4], "Not multiplying everything by a starting 0"),
            (6, [1, 2, 3, 4], "Not skipping the last number"),
            (234, [1, 2, 3, 4], "Not concatenating"),
        ]

        for target, operands, msg in test_cases:
            with self.subTest(target=target, operands=operands, msg=msg):
                self.assertFalse(self.test_day.can_be_made(target, operands, False))

    def test_can_be_made_part_two(self):
        test_cases: list = [
            (1019, [10, 19], "10 || 19"),
            (64, [1, 2, 3, 4], "1 * 2 * 3 || 4"),
            (432, [4, 3, 2, 1], "4 || 3 || 2 * 1"),
            (154, [1, 2, 3, 4], "1 || 2 + 3 || 4"),
            (13, [1, 2, 3, 4], "1 + 2 * 3 + 4"),
            (1234, [1, 2, 3, 4], "1 || 2 || 3 || 4"),
            (234, [1, 2, 3, 4], "1 * 2 || 3 || 4"),
        ]

        for target, operands, msg in test_cases:
            with self.subTest(target=target, operands=operands, msg=msg):
                self.assertTrue(self.test_day.can_be_made(target, operands, True))

    def test_can_be_made_part_two_sad(self):
        test_cases: list = [
            (1910, [10, 19], "Not concatenating in reverse"),
            (46, [1, 2, 3, 4], "(1 || 2) + (3 || 4)"),
        ]

        for target, operands, msg in test_cases:
            with self.subTest(target=target, operands=operands, msg=msg):
                self.assertFalse(self.test_day.can_be_made(target, operands, True))
