#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day07:
    """
    Solution for https://adventofcode.com/2024/day/7
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        # Can't use a dict because there's duplicate target values
        # Position 0 is always the target value. Everything else is an operand
        self.test_values: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line is a string of the format "N: X Y Z ..."
        where N is a number, and X Y Z ... are numbers of varying length
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        for item in self.input:
            # Sample input: "190: 19 19"
            nums: list = list(map(lambda x: int(x.strip(':')), item.split()))
            self.test_values.append(nums)

    def _can_be_made_r(self, target: int, operands: list, index: int, acc: int, part_two: bool) -> bool:
        """
        Recursive helper method to work out whether target can be made out of
        the operands.
        By default, the valid operators are + and *
        If part_two is set, also concatenate acc with the next operand

        :param target: The number we're trying to make
        :type target: int
        :param operands: The numbers we can use to make the target
        :type operands: list
        :param index: Which number we're looking at next
        :type index: int
        :param acc: The accumulated number
        :type acc: int
        :param part_two: Whether to concatenate numbers as an operator
        :type part_two: bool
        :return: True if the target can be made out of the operands and operators
        :rtype: bool
        """
        # Break early
        if acc > target:
            return False

        # Hit the target and used all the operands
        if acc == target and index >= len(operands):
            return True

        # Base case - ran out of numbers to try
        if index >= len(operands):
            return False

        # Keep searching - try adding and multiplying the next number with this one
        # For part two, add a new operator: Concatenate the next number to acc
        return  self._can_be_made_r(target, operands, index+1,       acc + operands[index]   , part_two) \
            or  self._can_be_made_r(target, operands, index+1,       acc * operands[index]   , part_two) \
            or (self._can_be_made_r(target, operands, index+1, int(f'{acc}{operands[index]}'), part_two) if part_two else False)

    def can_be_made(self, target: int, operands: list, part_two: bool) -> bool:
        """
        Return whether target can be made out of the operands.

        :param target: The number we're trying to make
        :type target: int
        :param operands: The numbers we can use to make the target
        :type operands: list
        :param part_two: Whether to concatenate numbers as an operator
        :type part_two: bool
        :return: True if the target can be made out of the operands and operators
        :rtype: bool
        """
        return self._can_be_made_r(target, operands, 1, operands[0], part_two)

    def part_one(self) -> int:
        """
        Return the sum of all values that can be made when using + and * as operators
        """
        calibration_value: int = 0

        for item in self.test_values:
            # item[0] is the target value
            if self.can_be_made(item[0], item[1:], False):
                calibration_value += item[0]

        return calibration_value

    def part_two(self) -> int:
        """
        Return the sum of all values that can be made when using +, *, and || as operators
        """
        calibration_value: int = 0

        for item in self.test_values:
            if self.can_be_made(item[0], item[1:], True):
                calibration_value += item[0]

        return calibration_value

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
