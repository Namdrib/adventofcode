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

    def apply_rotation(self, dial: int, rotation: int) -> tuple:
        """
        Apply a rotation of some magnitude and polarity to the dial

        A postiive rotation rotates to the right (increases dial)
        A negative rotation rotates to the left (decreases dial)

        :param dial: The starting position of the dial when the rotation is applied
        :type dial: int
        :param rotation: The magnitude and direction of the rotation
        :type rotation: int
        :return: (The new dial position, how many times it pointed at zero during the rotation)
        :rtype: tuple
        """
        # How many times rotation causes the dial to point at 0
        num_zeroes: int = 0

        # The numbers for each rotation are small enough that we can simulate
        # each click
        # If they were larger, we'd have to be smarter about treating each "lot"
        # of 100 as a full rotation
        for _ in range(abs(rotation)):
            # Simulate a single click
            if rotation > 0:
                dial += 1
            else:
                dial -= 1

            # Handle underflows
            if dial < 0:
                dial += 100
            # Handle overflows
            if dial >= 100:
                dial -= 100

            # Track each zero
            if dial == 0:
                num_zeroes += 1

        return dial, num_zeroes

    def part_one(self) -> int:
        """
        Return the number of times the dial is pointed at 0 after applying a
        rotation
        """
        count: int = 0

        dial: int = 50
        for rotation in self.rotations:
            dial, _ = self.apply_rotation(dial, rotation)
            # Count each time the dial ends up at zero
            if dial == 0:
                count += 1

        return count

    def part_two(self) -> int:
        """
        Return the number of times the dial is pointed at 0 after applying each
        click
        """
        count: int = 0

        dial: int = 50
        for rotation in self.rotations:
            dial, num_zeroes = self.apply_rotation(dial, rotation)
            # Count how many times the dial ended up pointing at zero
            if num_zeroes > 0:
                count += num_zeroes

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
