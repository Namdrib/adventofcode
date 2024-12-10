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
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.grid = []
        for y, item in enumerate(self.input):
            row: list = []
            for x, char in enumerate(item):
                if char == '.':
                    row.append(-1)
                else:
                    row.append(int(char))

                if char == '0':
                    self.trail_start_points.add(helpers.Point(int(x), int(y)))
            self.grid.append(row)

    def get_neighbours(self, p: helpers.Point) -> list:
        neighbours: list = []
        for direction in helpers.cardinal_directions:
            new_x: int = p.x + direction['x']
            new_y: int = p.y + direction['y']

            if helpers.in_range(self.grid, new_y) and helpers.in_range(self.grid[0], new_x):
                neighbours.append(helpers.Point(new_x, new_y))

        return neighbours
        
    def calculate_reachable_endpoints(self, starting_point: helpers.Point):
        # Perform a graph search to see how many endpoints (9) we can reach
        print(f'Searching for reachable endpoints at {starting_point=}')

        reachable_endpoints: set = set()

        fringe: Queue = Queue()
        fringe.put(starting_point)

        seen: set = set()

        while not fringe.empty():
            current: helpers.Point = fringe.get()

            # All of the valid neighbours on the grid
            neighbours: list = self.get_neighbours(current)

            for neighbour in neighbours:
                value_at_current: int = self.grid[current.y][current.x]
                value_at_neighbour: int = self.grid[neighbour.y][neighbour.x]
                if value_at_neighbour == 9 and value_at_current == 8:
                    print(f'\tFound endpoint at {neighbour=}')
                    reachable_endpoints.add(neighbour)
                    continue

                # Must be in increments of 1
                elif value_at_neighbour == value_at_current + 1:
                    fringe.put(neighbour)

            seen.add(current)

        print(f'\tGot {len(reachable_endpoints)} points!')
        return reachable_endpoints

    def part_one(self) -> int:
        """
        Return the ...
        """
        count: int = 0

        for start_point in self.trail_start_points:
            reachable_endpoints = self.calculate_reachable_endpoints(start_point)
            count += len(reachable_endpoints)

        return count

    def part_two(self) -> int:
        """
        Return the ...
        """
        count: int = 0

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
