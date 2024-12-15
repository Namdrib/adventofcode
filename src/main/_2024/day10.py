#!/usr/bin/python3
import os
from queue import Queue
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day10:
    """
    Solution for https://adventofcode.com/2024/day/10
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.grid: list = None
        self.trail_start_points: set = set()

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line is a row in a grid of numbers from 0-9
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.grid = []
        for y, item in enumerate(self.input):
            row: list = []
            for x, char in enumerate(item):
                # Just so we can run against some of the example test inputs
                if char == '.':
                    row.append(-1)
                else:
                    row.append(int(char))

                # Found a starting point
                if char == '0':
                    self.trail_start_points.add(helpers.Point(int(x), int(y)))

            self.grid.append(row)

    def calculate_reachable_endpoints(self, starting_point: helpers.Point) -> dict:
        """
        Perform breadth-first search (BFS) from the starting point to see how
        many endpoints (with value 9) we can reach

        :param starting_point: The starting point of the search
        :type starting_point: helpers.Point
        :return: A dictionary of all the endpoints we can reach, and how many
        different ways we can get there
        :rtype: dict
        """
        # Keep track of which endpoints we can get to, and how many different
        # ways we can get there. The number of ways is used for part 2
        reachable_endpoints: dict = {}

        # Keep track of our current search options
        fringe: Queue = Queue()
        fringe.put(starting_point)

        # Don't need to keep track of places we've seen, since we are only ever
        # exploring uphill - never coming back downhill

        while not fringe.empty():
            current: helpers.Point = fringe.get()

            # For each neighbour of the current spot
            for neighbour in helpers.get_neighbours(current.x, current.y, self.grid):
                value_at_current: int = self.grid[current.y][current.x]
                value_at_neighbour: int = self.grid[neighbour.y][neighbour.x]

                # Did we reach an endpoint?
                if value_at_neighbour == 9 and value_at_current == 8:
                    # Keep track of how many ways we ended up at this endpoint
                    reachable_endpoints[neighbour] = reachable_endpoints.get(neighbour, 0) + 1
                    continue

                # Our next step must be exactly one higher than we are
                if value_at_neighbour == value_at_current + 1:
                    fringe.put(neighbour)

        return reachable_endpoints

    def part_one(self) -> int:
        """
        Return the sum of number of unique endpoints that can be reached from
        each starting point
        """
        count: int = 0

        for start_point in self.trail_start_points:
            reachable_endpoints = self.calculate_reachable_endpoints(start_point)
            count += len(reachable_endpoints)

        return count

    def part_two(self) -> int:
        """
        Return the sum of number of unique ways we can get from each starting
        point
        """
        count: int = 0

        for start_point in self.trail_start_points:
            reachable_endpoints = self.calculate_reachable_endpoints(start_point)
            count += sum(x for x in reachable_endpoints.values())

        return count

def main() -> None:
    """
    Main
    """
    solver = Day10()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
