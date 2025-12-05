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

    def merge_ranges(self, r1: list, r2: list) -> bool:
        """
        Merge two ranges together, where each range is a list of [lower, upper]
        When the ranges merge, r1 is modified in-place, extending its range to
        include that of r2

        :param r1: The first range to consider. This is modified in-place
        :type r1: list
        :param r2: The second range to consider
        :type r2: list
        :return: True if the ranges were merged (and therefore r1 was modified),
        False otherwise
        :rtype: bool
        """
        # Record whether there was a modification to r1
        merged: bool = False

        # Extend the lower range of r1
        if r2[0] <= r1[0] and r2[1] >= r1[0]:
            r1[0] = min(r1[0], r2[0])
            merged = True

        # Extend the upper range of r1
        if r2[0] <= r1[1] and r2[1] >= r1[1]:
            r1[1] = max(r1[1], r2[1])
            merged = True

        return merged

    def add_new_range(self, ranges: list, range_: list) -> bool:
        """
        Add a new range to the list of existing ranges
        Attempt to merge range_ into all of the existing ranges
        If no merge is possible, add it to the ranges as a new range

        :param ranges: The list of existing ranges
        :type ranges: list
        :param range_: The new range to add
        :type range_: list
        :return: Whether the new range was added in as a unique range
        :rtype: bool
        """
        existing: bool = False
        for x in ranges:
            # If the queried range is contained within this range
            # Update the range to reflect the new bounds
            # Extend the lower range
            merged = self.merge_ranges(x, range_)
            if merged:
                existing = True

        # Otherwise it's a new unique range
        # Return true to signify we added a new range to the list
        if not existing:
            ranges.append(range_)
            return True

        return False

    def consolidate_ranges(self, unique_ranges: list) -> None:
        """
        Go each combination of ranges in the unique ranges, and merge them all
        together
        When merging, modify the list in-place, and delete any redundant ranges

        :param unique_ranges: A list of ranges that may or may not contain
        overlapping ranges. This is modified in-place
        :type unique_ranges: list
        """
        to_delete: list = []
        for i in range(len(unique_ranges)):
            for j in range(i+1, len(unique_ranges)):

                if self.merge_ranges(unique_ranges[i], unique_ranges[j]):
                    to_delete.append(j)

        for x in sorted(to_delete, reverse=True):
            val = unique_ranges.pop(x)

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
        unique_ranges: list = []

        # Merge all the ranges together, removing any duplicates
        for r in self.ranges:
            self.add_new_range(unique_ranges, r)
            self.consolidate_ranges(unique_ranges)

        # Finally, get the total number included by the unique ranges
        for r in unique_ranges:
            # +1 to include the very end of the range
            count += r[1] - r[0] + 1

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
