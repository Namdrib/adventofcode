#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day05:
    """
    Solution for https://adventofcode.com/2025/day/5
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.grid: list = []
        self.ranges: list = []
        self.ingredients: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.ranges = []
        self.ingredients = []
        is_range: bool = True
        for item in self.input:

            if item == '':
                is_range = False
                continue
            if is_range:
                self.ranges.append([int(x) for x in item.split('-')])
            else:
                self.ingredients.append(int(item))

    def is_fresh(self, ingredient: int) -> bool:
        """
        Return whether a given ingredient is considered fresh

        An ingredient is fresh if its ID falls within any of the ID ranges

        :param ingredient: the ingredient ID to query
        :type ingredient: int
        :return: True if the ingredient is in a known ID range, False otherwise
        :rtype: bool
        """
        for r in self.ranges:
            if ingredient in range(r[0], r[1]+1):
                return True
        return False

    def part_one(self) -> int:
        """
        Return the total number of ingredients that are considered fresh
        """
        count: int = 0

        for i in self.ingredients:
            if self.is_fresh(i):
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
    solver = Day05()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
