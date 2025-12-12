#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Machine:
    def __init__(self, target: str, buttons: list, joltage_reqs: list) -> None:
        self.target = [x == '#' for x in target[1:-1]]
        self.lights: bool = [False for _ in len(self.target)]

        # Each button toggles some set of lights
        self.buttons: list = []
        for button in buttons:
            # Strip the parens
            nums: list = button[1:-1]
            self.buttons.append([num for num in nums])

        self.joltage_reqs: list = [j for j in joltage_reqs[1:-1].split()]

class Day10:
    """
    Solution for https://adventofcode.com/2025/day/10
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        for item in self.input:
            target_state, *buttons, joltage = self.input.split()
            pass

    def part_one(self) -> int:
        """
        Return the ...
        """
        count: int = 0

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
    solver = Day10()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
