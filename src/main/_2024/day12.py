#!/usr/bin/python3
import itertools
import os
from queue import Queue
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Region:
    def __init__(self, plot_id: str, points: set) -> None:
        self.plot_id: str = plot_id
        self.points: set = points

        self.perimeter: int = 0 # Used for part 1
        self.num_sides: int = 0 # Used for part 2

    def calculate_perimeter(self, grid: list) -> None:
        """
        A point contributes to the perimeter if it is adjacent to a point not in
        the region (or OOB)

        :param grid: The grid
        :type grid: list
        """
        perimeter = 0
        for point in self.points:
            # For each neighbour,
            for neighbour in helpers.get_neighbours(point.x, point.y, grid, include_oob=True):
                # The perimeter increases by 1 if:
                # The neighbour is out of bounds
                if not helpers.in_range(grid, neighbour.y) or not helpers.in_range(grid[0], neighbour.x):
                    perimeter += 1
                # Or the neighbour has another plot ID
                elif grid[neighbour.y][neighbour.x] != self.plot_id:
                    perimeter += 1

        self.perimeter = perimeter

    def num_corners(self, p: helpers.Point, grid: list) -> int:
        """
        Return how many corners there are at the given point

        :param p: The point in this Region to check for corners
        :type p: helpers.Point
        :param grid: The grid
        :type grid: list
        :return: How many corners there are at this point
        :rtype: int
        """
        num_corners: int = 0

        # Examine each L-shape section from the point p.
        # The x are where we're looking on each iteration
        # xx. ... .xx ...
        # xp. xp. .px .px
        # ... xx. ... .xx
        for row_offset, col_offset in itertools.product([-1, 1], repeat=2):
            # Look at the tiles horizontally, vertically, and diagonally adjacent
            adj_h: helpers.Point = helpers.Point(p.x + row_offset, p.y)
            adj_v: helpers.Point = helpers.Point(p.x, p.y + col_offset)
            adj_d: helpers.Point = helpers.Point(p.x + row_offset, p.y + col_offset)

            # Are they the same as us?
            h_in_region: bool = helpers.in_range_2d(grid, adj_h.x, adj_h.y) \
                            and grid[adj_h.y][adj_h.x] == self.plot_id
            v_in_region: bool = helpers.in_range_2d(grid, adj_v.x, adj_v.y) \
                            and grid[adj_v.y][adj_v.x] == self.plot_id
            d_in_region: bool = helpers.in_range_2d(grid, adj_d.x, adj_d.y) \
                            and grid[adj_d.y][adj_d.x] == self.plot_id

            # Exterior corner, e.g.:
            # xxx
            # pPx <-- The P on the corner is an exterior corner
            # ppx
            if not h_in_region and not v_in_region:
                num_corners += 1
            # Interior corner, e.g.:
            # ppx
            # pPp <-- The P in the centre is an interior corner
            # ppp     This isn't covered by exterior corners of the other ps
            #
            # Note that the X will also count itself as a corner when looking
            # through the Xs (depending on what it has around it)
            elif h_in_region and v_in_region and not d_in_region:
                num_corners += 1

        return num_corners

    def calculate_num_sides(self, grid: list) -> None:
        """
        The number of sides of a region is equal to the number of corners

        :param grid: _description_
        :type grid: list
        """
        num_sides = 0

        for point in self.points:
            num_sides += self.num_corners(point, grid)

        self.num_sides = num_sides

class Day12:
    """
    Solution for https://adventofcode.com/2024/day/12
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.grid: list = None

        # A dictionary representing the regions on the map, represented as:
        # dict(plot_id: dict(initial_point, Size)), where:
        # - plot_id is the letter representing the plot, noting that this plot_id may have multiple plots
        # - initial_point is the first point we've seen of that plot instance of
        # the plot, so we have a reference to it
        self.regions: list = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line is a row of a 2D grid, where each character is a
        letter representing a plant in a garden
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.grid = []
        for item in self.input:
            self.grid.append(list(item))

    def get_all_points_in_same_region(self, p: helpers.Point) -> set:
        """
        Perform a flood fill to find the set of points that belong
        to the same region as the given point

        :param p: The point to check
        :type p: helpers.Point
        :return: The points in the same region as the given point
        :rtype: set
        """
        points: set = set()
        points.add(p)

        plot_id: str = self.grid[p.y][p.x]

        queue: Queue = Queue()
        queue.put(p)

        seen: set = set()

        while not queue.empty():
            current: helpers.Point = queue.get()
            # print(f'Looking at {current=}')

            if self.grid[current.y][current.x] != plot_id:
                continue

            for neighbour in helpers.get_neighbours(current.x, current.y, self.grid):
                # Already explored here - save some CPU cycles
                if neighbour in seen or neighbour in points:
                    continue

                # Part of the same area
                if self.grid[neighbour.y][neighbour.x] == plot_id:
                    points.add(neighbour)
                    queue.put(neighbour)

            seen.add(current)

        return points

    def initialise_regions(self) -> None:
        """
        Populate all regions in the map with their plot ID and the corresponding
        points
        """
        self.regions = []
        # Go over every point
        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                p: helpers.Point = helpers.Point(x, y)

                # Are we part of any existing region?
                for region in self.regions:
                    if self.grid[y][x] == region.plot_id:
                        if p in region.points:
                            break
                else:
                    # If not, make a new region by flood filling all adjacent
                    # points
                    points: set = self.get_all_points_in_same_region(p)
                    region: Region = Region(char, points)
                    self.regions.append(region)

    def part_one(self) -> int:
        """
        Return the sum of the price of all regions, which is calculated by
        multiplying its perimeter with its area
        """
        self.initialise_regions()

        count: int = 0

        for region in self.regions:
            region.calculate_perimeter(self.grid)
            count += region.perimeter * len(region.points)

        return count

    def part_two(self) -> int:
        """
        Return the sum of the price of all regions, which is calculated by
        multiplying the number of sides with its area
        """
        count: int = 0

        for region in self.regions:
            region.calculate_num_sides(self.grid)
            count += region.num_sides * len(region.points)

        return count

def main() -> None:
    """
    Main
    """
    solver = Day12()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
