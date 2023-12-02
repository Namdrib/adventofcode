#!/usr/bin/python3
import sys

class Day01:
    """
    Solution for https://adventofcode.com/2023/day/1
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self._input: list = None

        # Represents the initial calibration document
        self._calibration_doc: list = []

        # Mapping of each digit word to a digit character
        self._digit_words: dict = {
            'one':   '1',
            'two':   '2',
            'three': '3',
            'four':  '4',
            'five':  '5',
            'six':   '6',
            'seven': '7',
            'eight': '8',
            'nine':  '9',
        }

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line contains an alphanumeric string
        """
        _input = sys.stdin.read()

        for line in _input.split('\n'):
            line = line.strip()
            if line:
                self._calibration_doc.append(line)

    def get_digits_from(self, line: str) -> str:
        """
        Extract all of the valid digits from a given line.
        This includes word digits (e.g. 'one' -> '1') and numeric digits (e.g. '1')
        Letters may overlap, so 'eightwone' -> '821', rather than '81'

        :param line: An alphanumeric line
        :type line: str
        :return: All of the digits contained in the line, as a string
        :rtype: str
        """
        out: str = ''

        for i, char in enumerate(line):
            # Keep digits as-is
            if char.isdigit():
                out += char
            else:
                # Convert any digit words to their corresponding digit
                for word, digit in self._digit_words.items():
                    # Don't look too far ahead
                    if line.find(word, i, i+len(word)) > -1:
                        out += digit
                        break

        return out

    def get_calibration_value(self, line: str) -> int:
        """
        Combine the first digit and the last digit to form a single two-digit number

        :param line: A line from the calibration document
        :type line: str
        :return: The concatenated two-digit number
        :rtype: int
        """
        # Keep it as a string so it can be concatenated
        digits: list = [x for x in line if x.isdigit()]
        calibration_value: str = digits[0] + digits[-1]
        return int(calibration_value)

    def part_one(self) -> int:
        """
        Return the sum of all of the calibration values
        """
        return sum(self.get_calibration_value(x) for x in self._calibration_doc)

    def part_two(self) -> int:
        """
        Return the sum of all of the calibration values after pre-processing the document
        """
        # Represents the calibration doc after translating the number words to digits
        converted_lines = [self.get_digits_from(x) for x in self._calibration_doc]
        return sum(self.get_calibration_value(x) for x in converted_lines)

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
