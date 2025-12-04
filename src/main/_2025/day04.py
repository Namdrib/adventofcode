#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day04:
    """
    Solution for https://adventofcode.com/2025/day/4
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.grid: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.grid = []
        for item in self.input:
            self.grid.append([x for x in item])

    def num_occupied_neighbours(self, x: int, y: int) -> int:
        """
        Count the number of occupied spots around a given roll
        A spot is occupied if there is a roll present

        :param x: The x position of the cell to check
        :type x: int
        :param y: The y position of the cell to check
        :type y: int
        :return: The number of occupied spots for the given position
        :rtype: int
        """
        occupied_neighbours: int = 0

        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dy == 0 and dx == 0:
                    continue
                new_x: int = x + dx
                new_y: int = y + dy
                if helpers.in_range_2d(self.grid, x=new_x, y=new_y):
                    if self.grid[new_y][new_x] == '@':
                        occupied_neighbours += 1

        return occupied_neighbours

    def is_accessible(self, x: int, y: int) -> bool:
        """
        A roll is accessible if it has four or fewer other rolls in its eight
        adjacent tiles

        :param x: The x position of the cell to check
        :type x: int
        :param y: The y position of the cell to check
        :type y: int
        :return: True if the roll is accessible, False otherwise
        :rtype: bool
        """
        num_free_spots: int = 8 - self.num_occupied_neighbours(x, y)
        return num_free_spots > 4

    def part_one(self) -> int:
        """
        Return the number of rolls that are accessible by forklift
        """
        count: int = 0

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if self.grid[y][x] == '@':
                    if self.is_accessible(x, y):
                        count += 1


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
    solver = Day04()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
