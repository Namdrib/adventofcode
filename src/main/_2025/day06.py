#!/usr/bin/python3
from functools import reduce
from operator import mul
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day06:
    """
    Solution for https://adventofcode.com/2025/day/6
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        # a 2D representation
        # Each of the **columns** is n arithmetic problem, using that column of operators
        self.operands: list = []
        self.operands2: list = []
        self.operators: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        for i, item in enumerate(self.input):
            # The last row is operators
            if i == len(self.input) - 1:
                self.operators.extend([x for x in item.split()])
            # All others are operands
            else:
                self.operands.append([int(x) for x in item.split()])
            self.operands2.append([x for x in item])

    def solve_problem(self, operands: list, operator: str) -> int:
        """
        A problem is given in terms of a list of numbers, and an operator to
        perform on those numbers

        :param operands: The list of numbers to act on
        :type operands: list
        :param operator: Either a '+' or a '*', describing whether to add or multiply the operands together
        :type operator: str
        :return: The result of solving the problrm
        :rtype: int
        """
        if operator == '+':
            out = sum(operands)
        else:
            out = reduce(mul, operands, 1)

        return out

    def part_one(self) -> int:
        """
        Return the sum of all problems, going left to right

        Each problem is top-to-bottom, with the operands being the numbers in
        each row, and an operand at the bottom of the problem
        """
        count: int = 0

        # Go down each column, solving that problem and storing the result
        for x in range(len(self.operands[0])):
            operands: list = [self.operands[y][x] for y in range((len(self.operands)))]
            res: int = self.solve_problem(operands, self.operators[x])
            count += res

        return count

    def part_two(self) -> int:
        """
        Return the sum of all problems

        Each problem is defined right-to-left, with the operands of that problem
        being a number read from top-to-bottom

        Each problem is separated by a column of white space
        """
        count: int = 0

        operands: list = []
        operator: str = ''

        # Used to keep track of whether the column is empty
        # Used to determine when we move on to the next problem, which invovles
        # clearing the operands
        end_of_problem: bool = False

        # From right to left
        for x in range(len(self.operands2[0])-1, -1, -1):
            # Skip the empty column, get ready for the next problem
            if end_of_problem:
                end_of_problem = False
                operands = []
                continue

            # Start a new operand
            operand: int = 0

            # Scan down the current column, building up the operand's digits
            for y in range(0, len(self.operands2)):
                # Each digit we find contributes to the operand
                current: str = self.operands2[y][x]
                # Add the "next digit" to this item
                if current.isdigit():
                    operand *= 10
                    operand += int(current)

                # Store the operator for this problem
                if current in '+*':
                    operator = current
                    end_of_problem = True

            # We got to the end of a column, store the operand
            operands.append(operand)

            # After reaching the end of the problem, we can solve it and store
            # the result
            if end_of_problem:
                res: int = self.solve_problem(operands, operator)
                count += res

        return count

def main() -> None:
    """
    Main
    """
    solver = Day06()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
