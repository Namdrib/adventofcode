#!/usr/bin/python3
import sys

class Day15:
    """
    Solution for https://adventofcode.com/2023/day/15
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.initialisation_sequence: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, the input is single line of comma-separated instructions
        """
        self.input = sys.stdin.read()

        self.initialisation_sequence = self.input.strip().split(',')

    def do_hash(self, string: str) -> int:
        """
        The HASH algorithm is a way to turn any string of characters into a single number in the range 0 to 255.
        To run the HASH algorithm on a string, start with a current value of 0.
        Then, for each character in the string starting from the beginning:
            - Determine the ASCII code for the current character of the string.
            - Increase the current value by the ASCII code you just determined.
            - Set the current value to itself multiplied by 17.
            - Set the current value to the remainder of dividing itself by 256.

        :param string: The string to hash
        :type string: str
        :return: hash value of the string
        :rtype: int
        """
        current_value: int = 0

        for char in string:
            ascii_code = ord(char)
            current_value += ascii_code
            current_value *= 17
            current_value %= 256

        return current_value

    def part_one(self) -> int:
        """
        Find the sum of the hash of every step in the initialisation sequence
        """
        return sum(self.do_hash(x) for x in self.initialisation_sequence)

    def part_two(self) -> int:
        """
        Find the total load on the north support beams after 1000000000 spin cycles
        See: do_spin_cycle(grid)
        """
        return 0

def main() -> None:
    """
    Main
    """
    solver = Day15()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
