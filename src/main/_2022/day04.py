#!/usr/bin/python3
import sys

class Day04:
    """
    Solution for https://adventofcode.com/2022/day/4
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self._input: list = None
        self._elf_section_ranges: list = []


    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line looks like "1-2,3-4"
        where each side of the comma describes an integer range
        """
        raw_input = sys.stdin.read()

        self._input = raw_input.split('\n')
        self._input = self._input[0:-1]

        self._elf_section_ranges = []

        # Here we're parsing this into a list of [((lower,upper), (lower,upper)] ints
        for item in self._input:
            sections: list = item.split(',')
            first_start, first_end = sections[0].split('-')
            second_start, second_end = sections[1].split('-')

            first_tuple: tuple = (int(first_start), int(first_end))
            second_tuple: tuple = (int(second_start), int(second_end))
            self._elf_section_ranges.append( (first_tuple, second_tuple) )

    def part_one(self) -> int:
        """
        Return the number of pairs that fully overlap
        e.g. 1-5,2-5 is a full overlap
        """
        num_full_overlap: int = 0

        for item in self._elf_section_ranges:
            # If all of the first is contained inside second
            # Or if all of the second is contained inside first
            if item[0][0] >= item[1][0] and item[0][1] <= item[1][1]:
                num_full_overlap += 1

            elif item[1][0] >= item[0][0] and item[1][1] <= item[0][1]:
                num_full_overlap += 1

        return num_full_overlap

    def part_two(self) -> int:
        """
        Return the number of pairs that have any overlap
        e.g. 1-2,3-4 has no overlap but 1-3,3-4 does
        """
        num_overlap: int = 0

        for item in self._elf_section_ranges:
            # If any from the first is contained inside second
            # Or if any from the second is contained inside first
            if item[0][0] in range(item[1][0], item[1][1] + 1):
                num_overlap += 1

            elif item[1][0] in range(item[0][0], item[0][1] + 1):
                num_overlap += 1

        return num_overlap

def main() -> None:
    """
    Main
    """
    solver = Day04()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
