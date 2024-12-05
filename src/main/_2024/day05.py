#!/usr/bin/python3
import itertools
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day05:
    """
    Solution for https://adventofcode.com/2024/day/5
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.ordering_rules: list = []
        self.updates: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, there are two blocks of data.
        The first block is a list of page ordering rules in the format "N|M",
        which signifies that page N must come before page M
        Then, there is a blank line
        The second block is a list of page updates that must be made, which is a
        list of comma-separated list of numbers
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        mode: str = 'rules'
        for item in self.input:
            if mode == 'rules':
                if '|' in item:
                    left, right = item.split('|')
                    self.ordering_rules.append([int(left), int(right)])
                else:
                    mode = 'updates'
            elif mode == 'updates':
                update: list = list(map(int, item.split(',')))
                self.updates.append(update)

    def is_in_order(self, update: list) -> bool:
        """
        Return whether the update is in order according to the ordering rules

        :param update: The update (list of page numbers)
        :type update: list
        :return: True if the update is in order, False otherwise
        :rtype: bool
        """
        for left, right in itertools.pairwise(update):
            if [left, right] not in self.ordering_rules:
                return False
        return True

    def get_middle_page_number(self, update: list) -> int:
        """
        Return the middle page number of a given update

        :param update: The update to check the middle number of
        :type update: list
        :return: The value of the middle page number
        :rtype: int
        """
        mid: int = int(len(update) / 2)
        return update[mid]

    def fix_update(self, update: list) -> list:
        """
        Perform a sort to fix the update (so that all entries are sorted
        according to the ordering rules)

        :param update: The update to fix
        :type update: list
        :return: The new update, which has been sorted
        :rtype: list
        """
        # Perform bubble sort to fix the list
        n = len(update)-1
        for _ in range(n):
            for i in range(n):
                if [update[i], update[i+1]] not in self.ordering_rules:
                    update[i], update[i+1] = update[i+1], update[i]

        return update

    def part_one(self) -> int:
        """
        Return the sum of the middle pages of all the updates that are in order
        """
        return sum(
            self.get_middle_page_number(x)
                for x in self.updates if self.is_in_order(x)
        )

    def part_two(self) -> int:
        """
        Return the sum of the middle pages of all of the updates that are out of
        order, after fixing their order
        """
        return sum(
            self.get_middle_page_number(self.fix_update(x))
                for x in self.updates if not self.is_in_order(x)
        )

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
