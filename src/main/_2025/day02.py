#!/usr/bin/python3
from collections import namedtuple
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

# Nicer naming for a range
IdRange = namedtuple('IdRange', ['start', 'end'])

class Day02:
    """
    Solution for https://adventofcode.com/2025/day/2
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.id_ranges: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, the one line is a bunch of comma-separated ranges, each
        range gives its first ID and last ID separated by a dash (-)
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.id_ranges = []
        # Separate each range
        for x in self.input[0].split(','):
            # Isolate the start and end ID of the range
            start, end = [int(n) for n in x.split('-')]
            self.id_ranges.append(IdRange(start, end))

    def is_valid_part_one(self, id_: int) -> bool:
        """
        Return whether a number is considered valid for part one

        A number is *invalid* if the first and second halves are the same

        :param id_: The input number to check
        :type id_: int
        :return: True if the number is valid, false otherwise
        :rtype: bool
        """
        a = str(id_)
        half_length: int = int(len(a)/2)

        h1 = a[0:half_length]
        h2 = a[half_length:]

        return h1 != h2

    def is_valid_part_two(self, id_: int) -> bool:
        """
        Return whether a number is considered valid for part one

        A number is *invalid* if it is made up of the same string, repeated

        :param id_: The input number to check
        :type id_: int
        :return: True if the number is valid, false otherwise
        :rtype: bool
        """
        a = str(id_)

        # For each factor of a, except for len(a) itself
        # e.g., if the length of a is 6, check [1, 2, 3]
        l: int = len(a)
        for n in range(1, l):
            if l % n == 0:
                # See if a is made up of a multiple of each of these:
                # a, aa, aaa -> [a a a a a a], [aa aa aa], [aaa aaa]
                mult = int(l / n)
                substr: str = a[0:n]
                if a == substr * mult:
                    return False

        return True

    def part_one(self) -> int:
        """
        Return the sum of invalid numbers
        """
        count: int = 0

        for id_range in self.id_ranges:
            for x in range(id_range.start, id_range.end+1):
                if not self.is_valid_part_one(x):
                    count += x

        return count

    def part_two(self) -> int:
        """
        Return the sum of invalid numbers
        """
        count: int = 0

        for id_range in self.id_ranges:
            for x in range(id_range.start, id_range.end+1):
                if not self.is_valid_part_two(x):
                    count += x

        return count

def main() -> None:
    """
    Main
    """
    solver = Day02()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
