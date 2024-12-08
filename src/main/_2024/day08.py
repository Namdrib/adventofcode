#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day08:
    """
    Solution for https://adventofcode.com/2024/day/8
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.grid: list = []
        self.antenna_locations: dict = {}

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line is a row in a grid representing antennas
        All non-empty (.) locations are different antennas of different types
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        for y, row in enumerate(self.input):
            self.grid.append(list(row))
            for x, char in enumerate(row):
                if char != '.':
                    if self.antenna_locations.get(char) is None:
                        self.antenna_locations.setdefault(char, [])
                    self.antenna_locations.get(char).append((x, y))

    def calculate_antinode_locations(self, part_two: bool):
        # The count of antinodes. Starts off all False
        # As we encounter antinodes, they are marked as True
        # We only care about unique locations, so bool is good enough
        antinode_locations: list = [[False for x in y] for y in self.grid]

        # Loop over the locations of each antenna type separately
        for locations in self.antenna_locations.values():
            # Loop over each pair of antennas of the same type
            for L1 in locations:
                for L2 in locations:
                    # For part 2, all antennas are implicitly antinodes
                    if not part_two and L1 == L2:
                        continue

                    # How many times to project forwards?
                    # For part one, only look one step ahead
                    # For part two, keep going until out of bounds
                    loops: int = 0
                    limit = 9999 if part_two else 1

                    new_x, new_y = L1[0], L1[1]
                    while loops < limit:
                        # Project one space forward by the difference
                        new_x += (L1[0] - L2[0])
                        new_y += (L1[1] - L2[1])

                        # If this step is in the grid, mark it as an antinode
                        if helpers.in_range(self.grid, new_y) and helpers.in_range(self.grid[0], new_x):
                            antinode_locations[new_y][new_x] = True
                        # We've gone off-grid, this is the last antinode for
                        # this pair of antennas
                        else:
                            break

                        loops += 1

        return antinode_locations

    def part_one(self) -> int:
        """
        Return the number of unique locations that are antinodes when allowing
        one step
        """
        counts: list = self.calculate_antinode_locations(part_two=False)
        # Count the number of locations in counts that have a non-zero number
        return sum(sum(row) for row in counts)

    def part_two(self) -> int:
        """
        Return the number of unique locations that are antinodes when allowing
        many steps
        """
        counts: list = self.calculate_antinode_locations(part_two=True)
        return sum(sum(row) for row in counts)

def main() -> None:
    """
    Main
    """
    solver = Day08()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
