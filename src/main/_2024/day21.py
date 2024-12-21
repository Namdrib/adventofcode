#!/usr/bin/python3
import itertools
import os
import re
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day21:
    """
    Solution for https://adventofcode.com/2024/day/21
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.numeric_keypad: list = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            [' ', '0', 'A'],
        ]

        self.transitions: dict = {
            '0': {
                '0': '',
                '1': '^<', # The only way
                '2': '^', # The only way
                '3': '>^',
                '4': '^^<',
                '5': '^^', # The only way, in input
                '6': '>^^',
                '7': '^<^^',
                '8': '^^^', # The only way
                '9': '>^^^',
                'A': '>', # The only way
            },
            '1': {
                '0': '>v', # The only way
                '1': '',
                '2': '>', # The only way, in input
                '3': '>>', # The only way
                '4': '^', # The only way
                '5': '>^',
                '6': '>>^',
                '7': '^^', # The only way
                '8': '>^^',
                '9': '>>^^',
                'A': '>>v', # In input, no difference
            },
            '2': {
                '0': 'v', # The only way
                '1': '<', # The only way
                '2': '',
                '3': '>', # The only way
                '4': '<^',
                '5': '^', # The only way
                '6': '>^',
                '7': '<^^',
                '8': '^^', # The only way
                '9': '>^^', # Verified in example, in input
                'A': '>v',
            },
            '3': {
                '0': '<v',
                '1': '<<', # The only way
                '2': '<', # The only way
                '3': '',
                '4': '<<^',
                '5': '<^',
                '6': '^', # The only way
                '7': '<<^^', # Verified in example
                '8': '<^^', # In input, minimised
                '9': '^^', # The only way
                'A': 'v', # The only way
            },
            '4': {
                '0': '>vv',
                '1': 'v', # The only way
                '2': 'v>',
                '3': 'v>>',
                '4': '',
                '5': '>', # The only way
                '6': '>>',
                '7': '^', # The only way
                '8': '>^',
                '9': '>>^',
                'A': '>>vv', # In input, minimised
            },
            '5': {
                '0': 'vv', # The only way
                '1': '<v',
                '2': 'v', # The only way
                '3': 'v>',
                '4': '<', # The only way
                '5': '',
                '6': '>', # The only way
                '7': '<^',
                '8': '^', # The only way
                '9': '>^',
                'A': 'vv>', # In input, minimised
            },
            '6': {
                '0': '<vv',
                '1': '<<v',
                '2': '<v',
                '3': 'v', # The only way
                '4': '<<', # The only way
                '5': '<', # The only way
                '6': '',
                '7': '<<^', # In input, minimised
                '8': '<^',
                '9': '^', # The only way
                'A': 'vv', # Verified in example, in input
            },
            '7': {
                '0': '>vvv',
                '1': 'vv', # The only way, in input
                '2': 'vv>',
                '3': 'vv>>',
                '4': 'v', # The only way, in input
                '5': 'v>',
                '6': 'v>>',
                '7': '',
                '8': '>', # The only way
                '9': '>>', # The only way
                'A': '>>vvv',
            },
            '8': {
                '0': 'vvv', # Verified in example, in input
                '1': '<vv',
                '2': 'vv',
                '3': 'vv>',
                '4': '<v',
                '5': 'v',
                '6': 'v>', # In input, minimised
                '7': '<',
                '8': '',
                '9': '>',
                'A': 'vvv>',
            },
            '9': {
                '0': '<vvv',
                '1': '<<vv',
                '2': '<vv',
                '3': 'vv', # The only way
                '4': '<<v',
                '5': '<v',
                '6': 'v', # The only way
                '7': '<<', # The only way, in input
                '8': '<', # Verified in example
                '9': '',
                'A': 'vvv', # Verified in example, in input
            },
            'A': {
                '0': '<', # The only way
                '1': '^<<', # Verified in example, in input
                '2': '^<',
                '3': '^', # Verified in example
                '4': '<<^^', # Verified in example
                '5': '<^^',
                '6': '^^', # The only way, in input
                '7': '<<^^^',
                '8': '<^^^', # In input
                '9': '^^^', # Verified in example, in input
                'A': '',
                '^': '<', # The only way
                '<': 'v<<',
                'v': '<v',
                '>': 'v', # The only way
            },
            '^': {
                'A': '>', # The only way
                '^': '',
                '<': 'v<', # The only way
                'v': 'v', # The only way
                '>': 'v>',
            },
            '<': {
                'A': '>>^',
                '^': '>^', # The only way
                '<': '',
                'v': '>', # The only way
                '>': '>>', # The only way
            },
            'v': {
                'A': '>^',
                '^': '^', # The only way
                '<': '<', # The only way
                'v': '',
                '>': '>', # The only way
            },
            '>': {
                'A': '^', # The only way
                '^': '^<',
                '<': '<<', # The only way
                'v': '<', # The only way
                '>': '',
            },
        }

        self.arrow_keypad: list = [
            [' ', '^', 'A'],
            ['<', 'v', '>'],
        ]

        self.codes: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.codes = []

        for item in self.input:
            self.codes.append(item)

    def get_next_sequence(self, code: list) -> str:
        next_seq: str = ""
        for start, end in itertools.pairwise(code):
            next_seq += self.transitions[start][end] + 'A'

        return next_seq

    def enter_code(self, code: list) -> bool:
        first_arrow: str = self.get_next_sequence(f'A{code}')
        second_arrow: str = self.get_next_sequence(f'A{first_arrow}')
        third_arrow: str = self.get_next_sequence(f'A{second_arrow}')

        return third_arrow

    def get_numeric_value(self, code: str) -> int:
        return int("".join(x for x in code if x.isdigit()))

    def part_one(self) -> int:
        """
        Return the ...
        """
        count: int = 0

        for code in self.codes:
            result = self.enter_code(code)
            print(f'{code}: {result}')

            complexity: int = len(result) * self.get_numeric_value(code)
            count += complexity

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
    solver = Day21()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
