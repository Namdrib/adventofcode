#!/usr/bin/python3
import re
import sys

class Day03:
    """
    Solution for https://adventofcode.com/2024/day/3
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        # Match pattern for multiply instructions - Used for part 1
        mul_str: str = r'mul\(\d+,\d+\)'
        self.mul_pattern: re.Pattern = re.compile(mul_str)

        # Also match with the enables and disables - Used for part 2
        mul_with_able_str: str = r'do\(\)|don\'t\(\)|mul\(\d+,\d+\)'
        self.mul_with_able_pattern: re.Pattern = re.compile(mul_with_able_str)

        # Used to extract numbers out of a string
        numbers_str: str = r'\d+'
        self.numbers_pattern: re.Pattern = re.compile(numbers_str)

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

    def run_multiply(self, string: str) -> int:
        """
        Execute a multiple instruction, returning the integer result

        :param string: A multiply instruction that looks like mul(X,Y), where X and Y are numbers
        :type string: str
        :return: The product of X and Y
        :rtype: int
        """
        left, right = self.numbers_pattern.findall(string)
        return int(left) * int(right)

    def part_one(self) -> int:
        """
        Multiply instructions are a function that multiply two given numbers
        Return the sum of the result of all the multiply instructions
        """
        total: int = 0
        for item in self.input:
            mul_commands: list = self.mul_pattern.findall(item)
            for command in mul_commands:
                total += self.run_multiply(command)
        return total

    def part_two(self) -> int:
        """
        Multiply instructions `mul(X,Y)` are functions that multiply two numbers
        Do instructions `do()` enable subsequent multiply instructions
        Don't instructions `don't()` disable subsequent multiply instructions
        Return the sum of the result of all the enabled multiply instructions
        """
        total: int = 0

        # Keep track of whether to take execute multiply instructions
        is_enabled: bool = True

        for item in self.input:
            mul_commands: list = self.mul_with_able_pattern.findall(item)
            for command in mul_commands:
                if command == 'do()':
                    is_enabled = True
                elif command == "don't()":
                    is_enabled = False
                else:
                    if is_enabled:
                        total += self.run_multiply(command)
        return total

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
