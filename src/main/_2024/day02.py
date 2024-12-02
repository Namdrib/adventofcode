#!/usr/bin/python3
import itertools
import sys

def is_safe(report: list) -> bool:
    """
    Return whether a given report (a list of numbers) is safe or not.

    A report is a list of numbers (levels). It is safe if all of the following apply:
    - The levels are either all increasing or all decreasing.
    - Any two adjacent levels differ by at least one and at most three.

    :param report: A list of numbers
    :type report: list
    :return: True if the report is safe, False otherwise
    :rtype: bool
    """
    # Work out whether we should be increasing (1) or decreasing (-1) based
    # on the first two elements
    direction: int = 1 if report[0] < report[1] else -1

    # If any pair goes in the other direction, it's unsafe
    for left, right in itertools.pairwise(report):
        diff: int = right - left

        # Went the wrong way
        # Positive * positive -> 1
        # Negative * negative -> 1
        # Anything else means we're going in the wrong direction
        if diff * direction < 0:
            return False

        # Difference is too big
        if abs(diff) not in range(1, 4):
            return False

    # Safe!
    return True

class Day02:
    """
    Solution for https://adventofcode.com/2024/day/2
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.reports: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()

        self.input = raw_input.splitlines()

        for item in self.input:
            levels: list = item.split()
            self.reports.append(list(map(int, levels)))

    def part_one(self) -> int:
        """
        Return the number of reports that are safe
        """
        num_safe: int = 0
        for report in self.reports:
            if is_safe(report):
                num_safe += 1
        return num_safe

    def part_two(self) -> int:
        """
        Return the number of reports that are safe when the Problem Dampener is
        in place. It allows for one bad level (as though it wasn't there) before
        considering a report unsafe.
        """
        num_safe: int = 0
        for report in self.reports:
            # Check if safe
            if is_safe(report):
                num_safe += 1

            # If not, try permutations
            else:
                # Brute force, babey!
                for i in range(len(report)):
                    # Create a new list with one element missing
                    new_report = list(report)
                    new_report.pop(i)

                    # And try again :)
                    if is_safe(new_report):
                        num_safe += 1
                        # So we don't count the same report multiple times
                        break

        return num_safe

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
