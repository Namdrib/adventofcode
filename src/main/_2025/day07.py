#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day07:
    """
    Solution for https://adventofcode.com/2025/day/7
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.grid: list = None

        self.start_x: int = None
        self.start_y: int = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        # Load the grid
        self.grid = []
        for item in self.input:
            self.grid.append([x for x in item])

        # Locate the start
        found_start: bool = False
        for y, row in enumerate(self.grid):
            if found_start:
                break
            for x, cell in enumerate(row):
                if cell == 'S':
                    self.start_x = x
                    self.start_y = y
                    found_start = True
                    break

    def walk(self, x: int, y: int) -> int:
        split_count: int = self._walk(x, y, 0)
        return split_count

    def _walk(self, x: int, y: int, split_count: int) -> int:
        if y >= len(self.grid):
            return split_count

        # If the current cell is already a tachyon, stop
        if self.grid[y][x] == '|':
            return split_count

        # If the current cell is empty, move down
        if self.grid[y][x] == '.':
            self.grid[y][x] = '|'
            return self._walk(x, y+1, split_count)

        # If the current cell is a splitter, walk the cells to the left and
        # right
        if self.grid[y][x] == '^':
            split_count += 1
            return self._walk(x-1, y, split_count) + self._walk(x+1, y, 0)

    def part_one(self) -> int:
        """
        Return the number of times the beam is split
        """
        count: int = 0

        count = self.walk(self.start_x, self.start_y+1)

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
    solver = Day07()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
