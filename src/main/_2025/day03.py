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

        self.banks = [x for x in self.input]

    def get_max_joltage(self, bank: str):
        earliest_max_idx: int = 0
        earliest_max: int = int(bank[earliest_max_idx])
        latest_max_idx: int = len(bank)-1
        latest_max: int = int(bank[latest_max_idx])

        for i in range(len(bank)-1):
            battery = int(bank[i])
            if battery > earliest_max:
                earliest_max = battery
                earliest_max_idx = i

        for i in range(earliest_max_idx+1, len(bank)):
            battery = int(bank[i])
            if battery >= latest_max:
                latest_max = battery
                latest_max_idx = i

        return (earliest_max_idx, latest_max_idx)

    def part_one(self) -> int:
        """
        Return the ...
        """
        count: int = 0

        for bank in self.banks:
            pos_1, pos_2 = self.get_max_joltage(bank)
            joltage: int = int(bank[pos_1] + bank[pos_2])
            print(f'Max joltage {joltage} at {pos_1}, {pos_2}')
            count += joltage

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
    solver = Day03()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
