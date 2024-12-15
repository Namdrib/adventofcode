#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day04:
    """
    Solution for https://adventofcode.com/2024/day/4
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.grid: list = []
        self.midpoint_match_count: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        for item in self.input:
            self.grid.append(list(item))
            self.midpoint_match_count.append([0 for x in range(len(item))])

    def num_matches_at(self, x: int, y: int, target: str, mark_centre: bool = False) -> int:
        # See how many ways we can spell the target out
        # For each direction, including diagonals
        num_matches: int = 0
        for direction in helpers.get_directions(helpers.ordinal_directions):
            dx = direction['x']
            dy = direction['y']
            end_x: int = x + (len(target)-1) * dx
            end_y: int = y + (len(target)-1) * dy

            if not helpers.in_range(self.grid[0], end_x):
                # x would be out of bounds if we kept searching
                continue

            if not helpers.in_range(self.grid, end_y):
                # y would be out of bounds if we kept searching
                continue

            # Build up the word from the starting point to the end
            word: str = ""
            for i, char in enumerate(target):
                word += self.grid[y + i * dy][x + i * dx]

            # If we have a match
            if word == target:
                num_matches += 1

                # We are going diagonally and doing part two
                if dx and dy and mark_centre:
                    # Mark the middle of the target word
                    half_length: int = int(len(target) / 2)
                    mid_x = x + dx * half_length
                    mid_y = y + dy * half_length
                    self.midpoint_match_count[mid_y][mid_x] += 1

        return num_matches

    def part_one(self) -> int:
        """
        Return the number of times 'XMAS' appears in the grid, in any direction
        """
        num_xmas: int = 0

        # For each position
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                matches_at_pos: int = self.num_matches_at(x, y, 'XMAS')
                num_xmas += matches_at_pos

        return num_xmas

    def part_two(self) -> int:
        """
        Return the number of times 'MAS' appears in an 'X' shape
        """
        num_x_mas: int = 0

        # Count how many times A is at the centre of a diagonal match
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                self.num_matches_at(x, y, 'MAS', True)

        # A point is part of an X-MAS if it has multiple diagonal matches
        for row in self.midpoint_match_count:
            num_x_mas += sum(1 for x in row if x >= 2)

        return num_x_mas

def main() -> None:
    """
    Main
    """
    solver = Day04()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
