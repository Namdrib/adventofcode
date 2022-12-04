#!/usr/bin/python3
import sys

class DayXX:
    """
    Solution for https://adventofcode.com/2022/day/XX
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self._input: list = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()

        self._input = raw_input.split('\n')
        self._input = self._input[0:-1]

    def part_one(self) -> int:
        """
        Return the ...
        """
        return 0

    def part_two(self) -> int:
        """
        Return the ...
        """
        return 0

def main() -> None:
    """
    Main
    """
    solver = DayXX()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
