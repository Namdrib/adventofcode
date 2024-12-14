#!/usr/bin/python3
import os
import re
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import numpy as np

from util import helpers

class Machine:
    def __init__(self, ax, ay, bx, by, prize_x, prize_y) -> None:
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.prize_x = prize_x
        self.prize_y = prize_y

    def way_to_win(self) -> list:
        """
        Calculate how many times the A and B buttons need to be pressed to reach
        the prize location

        Solve the following system of equations for M and N:
        self.ax * M + self.bx * N = self.prize_x
        self.ay * M + self.by * N = self.prize_y

        :return: [A presses, B presses]
        :rtype: list
        """
        constraints = [
            [self.ax, self.bx],
            [self.ay, self.by]
        ]
        target = [self.prize_x, self.prize_y]

        # This returns a np.array of float64
        solution = np.linalg.solve(constraints, target)

        # Only look at solutions where an exact whole number of presses worked
        # Round, rather than typecast to int, to avoid rounding errors when
        # casting to int rolls it down, rather than going to the nearest whole
        # number. E.g., int(39.9) == 30, whereas round(39.9) == 40
        int_solution = [round(x) for x in solution]

        # Make sure the integer solution still satisfies the system of equations
        # Using np.allclose(np.dot(constraints, int_solution, target)) isn't
        # good enough for part 2 :(
        if self.ax * int_solution[0] + self.bx * int_solution[1] != self.prize_x:
            return [0, 0]
        if self.ay * int_solution[0] + self.by * int_solution[1] != self.prize_y:
            return [0, 0]

        return int_solution

    def cost_to_win(self) -> int:
        """
        Calculate how many tokens we need to reach the target
        Each press of the A button costs 3 tokens
        Each press of the B button costs 1 token

        :return: The number of tokens required to reach the prize. Return 0 if unreachable
        :rtype: int
        """
        presses: list = self.way_to_win()
        return 3 * presses[0] + presses[1]

    def __repr__(self):
        return f'Machine({self.ax}, {self.ay}, {self.bx}, {self.by}, {self.prize_x}, {self.prize_y})'

class Day13:
    """
    Solution for https://adventofcode.com/2024/day/13
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.machines: list = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        The input is formatted into paragraphs like:

        Button A: X+94, Y+34
        Button B: X+22, Y+67
        Prize: X=8400, Y=5400

        With an empty line between paragraphs
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.machines = []

        for i in range(0, len(self.input), 4):
            button_a: str = self.input[i]
            button_b: str = self.input[i+1]
            prize: str = self.input[i+2]

            a_nums: list = list(map(int, re.findall(r'\d+', button_a)))
            b_nums: list = list(map(int, re.findall(r'\d+', button_b)))
            prize_nums: list = list(map(int, re.findall(r'\d+', prize)))

            machine: Machine = Machine(a_nums[0], a_nums[1], b_nums[0], b_nums[1], prize_nums[0], prize_nums[1])
            self.machines.append(machine)

    def part_one(self) -> int:
        """
        Return the minimum number of tokens required to win all prizes
        """
        return sum(m.cost_to_win() for m in self.machines)

    def part_two(self) -> int:
        """
        Return the minimum number of tokens required to win all prizes after
        correcting the prize locations
        """
        cost: int = 0

        for m in self.machines:
            m.prize_x += 10000000000000
            m.prize_y += 10000000000000

            cost += m.cost_to_win()

        return cost

def main() -> None:
    """
    Main
    """
    solver = Day13()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
