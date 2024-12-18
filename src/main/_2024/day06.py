#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

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
        self.start_point: helpers.Point = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        for item in self.input:
            self.grid.append(list(item))
            # Find the guard's start position
            if '^' in item:
                x = item.find('^')
                y = len(self.grid)-1
                self.start_point = helpers.Point(x, y)

        # Don't get trapped
        self.grid[self.start_point.y][self.start_point.x] = '.'

    def traverse_grid(self, grid: list) -> set:
        # Start at the start, facing up
        next_dir = helpers.Point(0, -1)
        p = helpers.Point(self.start_point.x, self.start_point.y)

        # Used to determine whether we've already been here so we don't
        # double-count the same location
        seen = set()
        # Used to determine whether we're stuck in a loop
        seen_with_direction = set()

        # Walk forwards until we loop or exit the grid
        while True:
            if p in seen:
                p_with_direction = (p.x, p.y, next_dir.x, next_dir.y)
                # Been here in the same direction, it's a loop
                if p_with_direction in seen_with_direction:
                    return set()

                # But allow for crossing over a point we've been to before
                seen_with_direction.add(p_with_direction)

            seen.add(p.clone())

            next_point = helpers.Point(p.x + next_dir.x, p.y + next_dir.y)

            # Out of bounds, the guard made it out of the grid.
            # Return the set of points they've been to
            if not helpers.in_range_2d(grid, next_point.x, next_point.y):
                return seen

            # Space in front, walk forwards
            if grid[next_point.y][next_point.x] == '.':
                p.add(next_dir)

            # Obstacle in front, rotate 90 degrees clockwise
            elif grid[next_point.y][next_point.x] == '#':
                next_dir = helpers.rotate_clockwise(next_dir)

            else:
                print('What just happened?')

    def part_one(self) -> int:
        """
        Return the number of points the guard visits before they leave the map
        """
        return len(self.traverse_grid(self.grid))

    def part_two(self) -> int:
        """
        Return the number of new obstacle placements that would loop the guard
        This takes about 15-20 seconds to complete
        """
        count: int = 0

        points_visited: set = self.traverse_grid(self.grid)

        # All the possible places we can put an obstacle that may affect the
        # guard's path
        for p in points_visited:
            self.grid[p.y][p.x] = '#'

            # Did this cause a loop?
            if len(self.traverse_grid(self.grid)) == 0:
                count += 1

            # Put it back the way it was, ready for the next iteration
            self.grid[p.y][p.x] = '.'

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
