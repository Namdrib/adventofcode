#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day03:
    """
    Solution for https://adventofcode.com/2025/day/3
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.banks: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        # Nested list, where the outer layer is the banks, and inner layer is
        # the batteries (individual single-digit integers)
        self.banks = [[int(battery) for battery in bank] for bank in self.input]

    def get_max_joltage(self, bank: list, num_batteries: int) -> int:
        """
        Get the maximum joltage of having num_batteries turned on
        Where the joltage is the concatenation of the string values of each battery

        :param bank: The collection of batteries we have available, each is a one-digit integer
        :type bank: list
        :param num_batteries: The number of batteries that must be turned on
        :type num_batteries: int
        :return: The maximum joltage we can achieve with num_batteries batteries
        :rtype: int
        """
        # maxes[i] is the highest battery we can use for battery i
        indices: list = [0 for x in range(num_batteries)]
        maxes: list = [0 for x in range(num_batteries)]

        # Repeat for each battery that contributes to the total joltage
        for battery_num in range(num_batteries):
            # Start looking from the location of the previous max
            # Special case 0 for the first battery
            start = 0 if battery_num == 0 else indices[battery_num-1]+1

            # Leave enough room for the remaining batteries
            end: int = len(bank)-(num_batteries-battery_num)+1

            # This is the search space for battery[battery_num]
            for i in range(start, end):
                battery = bank[i]
                # Store the first highest battery we can use, and its index
                # This is so we can re-use the same highest value for another
                # battery to get the highest possible joltage, if there are
                # multiple of the highest value
                # Subsequent batteries will be to the right of this position
                if battery > maxes[battery_num]:
                    maxes[battery_num] = battery
                    indices[battery_num] = i

        # Convert the max batteries into their final joltage value by
        # concatenating their individual values
        joltage: int = int(''.join(str(x) for x in maxes))
        return joltage

    def part_one(self) -> int:
        """
        Return the sum of the joltage with 2 batteries turned on
        """
        count: int = 0

        for bank in self.banks:
            joltage: int = self.get_max_joltage(bank, num_batteries=2)
            count += joltage

        return count

    def part_two(self) -> int:
        """
        Return the sum of the joltage with 12 batteries turned on
        """
        count: int = 0

        for bank in self.banks:
            joltage: int = self.get_max_joltage(bank, num_batteries=12)
            count += joltage

        return count

def main() -> None:
    """
    Main
    """
    solver = Day03()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
