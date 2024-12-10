import unittest

from src.main.util import helpers

class TestHelpers(unittest.TestCase):

    def test_point(self):
        p: helpers.Point = helpers.Point(1, 2)

        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)

    def test_rotate_clockwise(self):
        test_cases: list = [
            (helpers.Point(1, 0),  helpers.Point(0, 1),  'East to South'),
            (helpers.Point(0, 1),  helpers.Point(-1, 0), 'South to West'),
            (helpers.Point(-1, 0), helpers.Point(0, -1), 'West to North'),
            (helpers.Point(0, -1), helpers.Point(1, 0),  'North to East'),
        ]

        for start, end, msg in test_cases:
            with self.subTest(start=start, msg=msg):
                self.assertEqual(helpers.rotate_clockwise(start), end)

    def test_rotate_anticlockwise(self):
        test_cases: list = [
            (helpers.Point(0, -1), helpers.Point(-1, 0), 'North to West'),
            (helpers.Point(-1, 0), helpers.Point(0, 1),  'West to South'),
            (helpers.Point(0, 1),  helpers.Point(1, 0),  'South to East'),
            (helpers.Point(1, 0),  helpers.Point(0, -1), 'East to North'),
        ]

        for start, end, msg in test_cases:
            with self.subTest(start=start, msg=msg):
                self.assertEqual(helpers.rotate_anticlockwise(start), end)

    def test_in_range(self):
        test_list: list = [1, 1, 1, 1]

        for x in range(len(test_list)-1):
            self.assertTrue(helpers.in_range(test_list, x))

        self.assertFalse(helpers.in_range(test_list, -1))
        self.assertFalse(helpers.in_range(test_list, len(test_list)))
