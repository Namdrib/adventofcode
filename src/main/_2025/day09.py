#!/usr/bin/python3
import itertools
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day09:
    """
    Solution for https://adventofcode.com/2025/day/9
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.tiles: list = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line is a set of co-ordinates representing the X,Y
        location of a red tile
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.tiles = []
        for item in self.input:
            x, y = [int(x) for x in item.split(',')]
            self.tiles.append((x, y))

    def calculate_area_within_tiles(self, tile_1: tuple, tile_2: tuple) -> int:
        x1 = tile_1[0]
        y1 = tile_1[1]

        x2 = tile_2[0]
        y2 = tile_2[1]

        # +1 because we must include the row/column the tiles are on
        dx: int = abs(x1 - x2) + 1
        dy: int = abs(y1 - y2) + 1

        return dx * dy

    def part_one(self) -> int:
        """
        Rectangles of tiles can be formed by selecting two corner tiles
        Return the area of the largest rectangle of tiles that can be made from
        a pair of corner tiles
        """
        largest_area: int = 0

        # Calculate the area of each pair of tiles
        # Store the largest area
        for t1, t2 in itertools.combinations(self.tiles, 2):
            area: int = self.calculate_area_within_tiles(t1, t2)
            largest_area = max(largest_area, area)

        return largest_area

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
    solver = Day09()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
