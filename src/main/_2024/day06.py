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
        # Using a tuple instead of helpers.Point for a performance boost (around
        # 15-20 seconds down to ~7 seconds for part 2)
        guard_pos = (self.start_point.x, self.start_point.y)

        # Used to determine whether we've already been here so we don't
        # double-count the same location
        visited = set()
        # Used to determine whether we're stuck in a loop
        visited_with_direction = set()

        # Walk forwards until we loop or exit the grid
        while True:
            if guard_pos in visited:
                guard_pos_with_direction = (
                    guard_pos[0], guard_pos[1], next_dir.x, next_dir.y
                )
                # Been here in the same direction, it's a loop
                if guard_pos_with_direction in visited_with_direction:
                    return set()

                # But allow for crossing over a point we've been to before
                visited_with_direction.add(guard_pos_with_direction)

            visited.add(guard_pos)

            next_pos = (guard_pos[0] + next_dir.x, guard_pos[1] + next_dir.y)

            # Out of bounds, the guard made it out of the grid.
            # Return the set of points they've been to
            if not helpers.in_range_2d(grid, next_pos[0], next_pos[1]):
                return visited

            # Space in front, walk forwards
            next_space: str = grid[next_pos[1]][next_pos[0]]
            if next_space == '.':
                guard_pos = (guard_pos[0] + next_dir.x, guard_pos[1] + next_dir.y)

            # Obstacle in front, rotate 90 degrees clockwise
            elif next_space == '#':
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

        # All the places where an obstacle may affect the guard's path
        for p in points_visited:
            # Place an obstacle
            self.grid[p[1]][p[0]] = '#'

            # Did this cause a loop?
            if len(self.traverse_grid(self.grid)) == 0:
                count += 1

            # Put it back the way it was, ready for the next iteration
            self.grid[p[1]][p[0]] = '.'

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
