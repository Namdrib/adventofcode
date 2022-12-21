#!/usr/bin/python3
import operator
import sys

from sympy import solve, Symbol

class Day21:
    """
    Solution for https://adventofcode.com/2022/day/21
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.original_monkeys: dict = {}

        self.operators = {
                '*': operator.mul,
                '+': operator.add,
                '-': operator.sub,
                '/': operator.truediv
        }

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line corresponds to a monkey's number or job
        """
        raw_input = sys.stdin.read()

        self.input = raw_input.splitlines()

        for item in self.input:
            parts = item.split(': ')
            self.original_monkeys[parts[0]] = parts[1]

    def populate_monkeys(self, monkeys_dict: dict, solve_for_humn: bool=False) -> None:
        """
        Process the monkey job list and work out what the final state will be
        by calculating each equation as we get enough information
        For part 2, the root equation is changed from an operator to an equality test
        We need to figure out what humn needs to be to pass this equality test
        Set up a system of equations to solve for humn
        This makes use of the sympy library to solve the equations
        """
        monkeys: list = [[name, job] for name, job in monkeys_dict.items()]

        # Keep track of the equations which have been resolved
        known_monkeys: dict = {}

        # Keep track of a system of simultaneous equations to solve for humn
        # Part 2 only
        equations: dict = {}

        while monkeys:
            name, job = monkeys.pop(0)

            if job.isnumeric():
                known_monkeys[name] = int(job)
                if name == 'humn':
                    equations[name] = Symbol('humn')
                else:
                    equations[name] = int(job)

            else:
                left, op, right = job.split()
                # We can resolve this current job
                if left in known_monkeys and right in known_monkeys:
                    known_monkeys[name] = self.operators[op](known_monkeys[left], known_monkeys[right])
                    if name == 'root':
                        equations[name] = equations[left] - equations[right]
                    else:
                        equations[name] = self.operators[op](equations[left], equations[right])

                else:
                    # Not enough infromation yet - come back later
                    monkeys.append([name, job])

        if solve_for_humn:
            return equations
        else:
            return known_monkeys

    def part_one(self) -> int:
        """
        Return the number at root after resolving all the monkeys
        """
        known_monkeys: dict = self.populate_monkeys(self.original_monkeys)
        root_number: int = known_monkeys['root']
        return int(root_number)

    def part_two(self) -> int:
        """
        Return what value humn needs to be to pass root's equality check (left == right)
        """
        equations: dict = self.populate_monkeys(self.original_monkeys, True)
        solved = solve(equations['root'])

        return int(solved[0])

def main() -> None:
    """
    Main
    """
    solver = Day21()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
