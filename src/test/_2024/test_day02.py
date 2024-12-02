import unittest

from src.main._2024 import day02

class TestDay02(unittest.TestCase):

    def test_is_safe_ascending(self):
        items = (
            [1, 2, 3, 4], # By 1
            [1, 3, 5, 7], # By 2
            [1, 4, 7, 10], # By 3
            [1, 3, 4, 5], # Mixed
            [-4, -3, -2, -1], # From negative
            [1, 2, 4, 7], # Mixed
            [1, 3, 6, 7, 9], # Mixed
        )

        for item in items:
            with self.subTest(item=item):
                self.assertTrue(day02.is_safe(item))

    def test_is_safe_descending(self):
        items = (
            [4, 3, 2, 1], # By -1
            [4, 2, 0, -2], # By -2
            [10, 7, 4, 1], # By -3
            [10, 7, 5, 4], # Mixed
            [7, 6, 4, 2, 1], # Mixed
        )

        for item in items:
            with self.subTest(item=item):
                self.assertTrue(day02.is_safe(item))

    def test_is_safe_unsafe(self):
        items = (
            [1, 2, 7, 8, 9], # Big jump
            [9, 7, 6, 2, 1], # Big jump
            [1, 3, 2, 4, 5], # Wrong way
            [8, 6, 4, 4, 1], # Zero-length change
        )

        for item in items:
            with self.subTest(item=item):
                self.assertFalse(day02.is_safe(item))

if __name__ == '__main__':
    unittest.main()
