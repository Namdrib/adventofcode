#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day09:
    """
    Solution for https://adventofcode.com/2024/day/9
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.file: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()[0]
        print(self.input)

    def expand_file(self, disk_map: str):
        expanded_file: list = []
        id_: int = 0
        for index, value in enumerate(disk_map):
            if index % 2 == 0:
                expanded_file.extend([id_ for _ in range(int(value))])
                id_ += 1
            else:
                expanded_file.extend([None for _ in range(int(value))])

        return expanded_file

    def compact_file(self, expanded_file: list) -> list:
        left: int = 0
        right: int = len(expanded_file) - 1

        while left < right:
            # "Walk" the left up to the first empty space
            while expanded_file[left] is not None:
                left += 1
            # "Walk the right down to the first non-empty space
            while expanded_file[right] is None:
                right -= 1
            if left >= right:
                break
            print(f'Swapping {expanded_file[left]} ({left}) and {expanded_file[right]} ({right})')
            expanded_file[left] = expanded_file[right]
            expanded_file[right] = None

        # Remove all of the empty space
        first_none_element: int = expanded_file.index(None)
        return expanded_file[0:first_none_element]

    def calculate_checksum(self, compacted_file: list) -> int:
        out: int = 0
        for i, value in enumerate(compacted_file):
            if value:
                out += i * value
        return out

    def part_one(self) -> int:
        """
        Return the ...
        """
        expanded_file: list = self.expand_file(self.input)
        print(expanded_file)
        compacted_file: list = self.compact_file(expanded_file)
        print(compacted_file)
        checksum = self.calculate_checksum(compacted_file)
        return checksum

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
    solver = Day09()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
