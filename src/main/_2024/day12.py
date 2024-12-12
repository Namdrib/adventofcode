#!/usr/bin/python3
import os
from queue import Queue
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

def get_neighbours(p: helpers.Point) -> list:
    out: list = []
    for direction in helpers.cardinal_directions:
        out.append(helpers.Point(p.x + direction['x'], p.y + direction['y']))
    return out

class Region:
    def __init__(self, plot_id: str, points: set) -> None:
        self.plot_id: str = plot_id
        self.points: set = points

        self.perimeter: int = 0 # Used for part 1
        self.num_sides: int = 0 # Used for part 2

    def calculate_perimeter(self, grid: list) -> None:
        perimeter = 0
        for point in self.points:
            # For each neighbour,
            for neighbour in get_neighbours(point):
                # The perimeter increases by 1 if:
                # The neighbour is out of bounds
                if not helpers.in_range(grid, neighbour.y) or not helpers.in_range(grid[0], neighbour.x):
                    perimeter += 1
                # Or the neighbour has another plot ID
                elif grid[neighbour.y][neighbour.x] != self.plot_id:
                    perimeter += 1

        self.perimeter = perimeter

    def is_corner(self, p: helpers.Point, grid: list) -> bool:
        # TODO: Not sure how to do this
        return True

    def calculate_num_sides(self, grid: list) -> None:
        """
        The number of sides of a region is equal to the number of corners

        :param grid: _description_
        :type grid: list
        """
        num_sides = 0

        for point in self.points:
            if self.is_corner(point, grid):
                num_sides += 1

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
                # if current in area:
                #     continue

            for neighbour in get_neighbours(current):
                # Already explored here - save some CPU cycles
                if neighbour in seen or neighbour in points:
                    continue

                # Bounds check y
                if not helpers.in_range(self.grid, neighbour.y):
                    continue

                # Bounds check x
                if not helpers.in_range(self.grid[0], neighbour.x):
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
