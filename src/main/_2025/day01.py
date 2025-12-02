#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day01:
    """
    Solution for https://adventofcode.com/2025/day/1
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.rotations: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line represents a rotation action on the dial,
        formatted like RN or LN, where N is a number
        R indicates a rotation to the right, L indicates a rotation to the left
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.rotations = []
        for item in self.input:
            number = int(item[1:])
            polarity = -1 if (item[0] == 'L') else 1
            self.rotations.append(number * polarity)

    def apply_roration(self, dial: int, rotation: int) -> int:
        dial += rotation
        # Handle underflow
        while dial < 0:
            dial += 100
        # Handle overflow
        if dial >= 100:
            dial = dial % 100
        
        return dial

    def part_one(self) -> int:
        """
        Return the number of times the dial is pointed at 0 after applying a
        rotation
        """
        count: int = 0

        dial: int = 50
        for rotation in self.rotations:
            dial = self.apply_roration(dial, rotation)
            print(f'Dial is rotated {rotation} to point at {dial}{" <---" if dial == 0 else ""}')
            if dial == 0:
                count += 1

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
    solver = Day01()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
