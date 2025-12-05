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

        print(f"Solving {operands} and {operator} gives {out}")
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
        Return the ...
        """
        count: int = 0

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
