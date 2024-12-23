import unittest

from src.main.util import helpers

class TestHelpers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.grid = [
            ['a', 'b', 'c'],
            ['d', 'e', 'f'],
            ['g', 'h', 'i'],
            ['j', 'k', 'l'],
        ]

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

    def test_get_directions_default(self):
        dirs: list = list(helpers.get_directions())
        self.assertEqual(len(dirs), 4)

    def test_get_directions_specified(self):
        dirs_in: list = ['N']
        dirs: list = list(helpers.get_directions(dirs_in))
        self.assertEqual(len(dirs), len(dirs_in))

    def test_get_neighbours_cardinal_no_oob_corner(self):
        neighbours: list = list(helpers.get_neighbours(0, 0, self.grid))

        points_in: list = [
            [0, 1], # Down
            [1, 0], # Right
        ]

        self.assertEqual(len(neighbours), 2)

        # No need to test the sad case, because we've exhausted all 2
        # possibilities here
        for point in points_in:
            with self.subTest(point=point):
                self.assertIn(helpers.Point(point[0], point[1]), neighbours)

    def test_get_neighbours_cardinal_no_oob_mid(self):
        neighbours: list = list(helpers.get_neighbours(1, 1, self.grid))

        points_in: list = [
            [1, 0], # Up
            [2, 1], # Right
            [1, 2], # Down
            [0, 1], # Left
        ]

        # No need to test the sad case, because we've exhausted all 4
        # possibilities here
        self.assertEqual(len(neighbours), 4)
        for point in points_in:
            with self.subTest(point=point):
                self.assertIn(helpers.Point(point[0], point[1]), neighbours)

    def test_get_neighbours_cardinal_with_oob(self):
        neighbours: list = list(helpers.get_neighbours(0, 0, self.grid, include_oob=True))

        points_in: list = [
            [0, -1], # North
            [1, 0], # East
            [0, 1], # South
            [-1, 0], # West
        ]

        self.assertEqual(len(neighbours), 4)

        for point in points_in:
            with self.subTest(point=point):
                self.assertIn(helpers.Point(point[0], point[1]), neighbours)

    def test_get_neighbours_ordinal_no_oob(self):
        neighbours: list = list(helpers.get_neighbours(0, 0, self.grid, directions=helpers.ordinal_directions))

        points_in: list = [
            [0, 1], # South
            [1, 0], # East
            [1, 1], # South-East
        ]

        self.assertEqual(len(neighbours), 3)

        for point in points_in:
            with self.subTest(point=point):
                self.assertIn(helpers.Point(point[0], point[1]), neighbours)

    def test_get_neighbours_ordinal_with_oob(self):
        neighbours: list = list(helpers.get_neighbours(0, 0, self.grid, directions=helpers.ordinal_directions, include_oob=True))

        points_in: list = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x and y:
                    points_in.append([x, y])

        self.assertEqual(len(neighbours), 8)

        for point in points_in:
            with self.subTest(point=point):
                self.assertIn(helpers.Point(point[0], point[1]), neighbours)

    def test_get_grid_diamond(self):

        # Points, from top to bottom, left to right
        perimeter_of_1: set = {
            ( 0, -1),
            (-1,  0),
            ( 1,  0),
            ( 0,  1),
        }

        perimeter_of_2: set = {
            ( 0, -2),
            (-1, -1),
            ( 1, -1),
            (-2,  0),
            ( 2,  0),
            (-1,  1),
            ( 1,  1),
            ( 0,  2),
        }

        with self.subTest(size=0):
            diamond = helpers.get_grid_diamond(0, 0, 0)
            self.assertSetEqual(set(), diamond)

        with self.subTest(size=1):
            diamond = helpers.get_grid_diamond(0, 0, 1)
            self.assertEqual(len(perimeter_of_1), len(diamond))
            for point in perimeter_of_1:
                self.assertIn(point, diamond)

        with self.subTest(size=2):
            diamond = helpers.get_grid_diamond(0, 0, 2)
            self.assertEqual(len(perimeter_of_1) + len(perimeter_of_2), len(diamond))

            for point in perimeter_of_1.union(perimeter_of_2):
                self.assertIn(point, diamond)

        with self.subTest(size=2, msg="Perimeter only"):
            # Ignore all of the "inner" positions of the diamond
            # We should be left with only the outer edge
            perimeter_only = diamond.difference(perimeter_of_1)

            self.assertEqual(len(perimeter_only), len(perimeter_of_2))

            for point in diamond.difference(perimeter_of_1):
                self.assertIn(point, perimeter_of_2)
