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

    def is_valid(self, id_: int) -> bool:
        a = str(id_)
        half_length: int = int(len(a)/2)

        # Only consider invalidness for even-length numbers
        # if half_length % 2 == 0:
        #     return True

        h1 = a[0:half_length]
        h2 = a[half_length:]

        return h1 != h2

    def part_one(self) -> int:
        """
        Return the ...
        """
        count: int = 0

        for id_range in self.id_ranges:
            for x in range(id_range.start, id_range.end+1):
                if not self.is_valid(x):
                    print(f'{x} is invalid')
                    count += x

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
    solver = Day02()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
