#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def add(self, p) -> None:
        self.x += p.x
        self.y += p.y

    def subtract(self, p) -> None:
        self.x -= p.x
        self.y -= p.y

    def clone(self):
        return Point(self.x, self.y)

    def __eq__(self, p) -> bool:
        return self.x == p.x and self.y == p.y

    def __repr__(self) -> str:
        return f'Point({self.x}, {self.y})'

class Day06:
    """
    Solution for https://adventofcode.com/2024/day/6
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.grid: str = []
        self.start_point: Point = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        for item in self.input:
            self.grid.append(list(item))
            if '^' in item:
                x = item.find('^')
                y = len(self.grid)-1
                self.start_point = Point(x, y)

        # Don't get trapped
        self.grid[self.start_point.y][self.start_point.x] = '.'

    def rotate_clockwise(self, p) -> list:
        return Point(-p.y if p.y else p.y, p.x)

    def traverse_grid(self, grid: list) -> int:
        # Start at the start, facing up
        next_dir = Point(0, -1)
        p: Point = Point(self.start_point.x, self.start_point.y)

        # We've been to the start
        points_traversed: int = 0

        # used to determine whether we've already been here so we don't
        # double-count the same location
        seen = set()
        seen.add((p.x, p.y))
        # Used to determine whether we're stuck in a loop
        seen_with_direction = set()

        # Walk forwards until we hit an obstacle (#)
        while True:
            if (p.x, p.y) not in seen:
                points_traversed += 1
                seen.add((p.x, p.y))

            else:
                if (p.x, p.y, next_dir.x, next_dir.y) not in seen_with_direction:
                    seen_with_direction.add((p.x, p.y, next_dir.x, next_dir.y))
                else:
                    # In a loop!
                    return -1

            next_point: Point = Point(p.x + next_dir.x, p.y + next_dir.y)

            # Out of bounds, the guard made it out of the grid.
            # Return how many points they've been to
            if not helpers.in_range(grid, next_point.y) or \
                    not helpers.in_range(grid[0], next_point.x):
                return points_traversed + 1

            # Space in front, walk forwards
            if grid[next_point.y][next_point.x] == '.':
                p.add(next_dir)

            # Obstacle in front, rotate 90 degrees clockwise
            elif grid[next_point.y][next_point.x] == '#':
                next_dir = self.rotate_clockwise(next_dir)

            else:
                print('What just happened?')

    def part_one(self) -> int:
        """
        Return the number of points the guard visits before they leave the map
        """
        return self.traverse_grid(self.grid)

    def part_two(self) -> int:
        """
        Return the number of new obstacle placements that would loop the guard
        This takes a while to complete...
        """
        count: int = 0

        # All the possible places we can put an obstacle
        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                if char == '.':
                    self.grid[y][x] = '#'

                    # If the return value is -1, there's a loop
                    if self.traverse_grid(self.grid) == -1:
                        count += 1

                    # Put it back the way it was, ready for the next iteration
                    self.grid[y][x] = '.'

        return count

def main() -> None:
    """
    Main
    """
    solver = Day06()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
