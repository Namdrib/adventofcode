#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day22:
    """
    Solution for https://adventofcode.com/2024/day/22
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.initial_numbers: list = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.initial_numbers: list = list(map(int, self.input))

    def mix(self, num, value) -> int:
        """
        To mix a value into the secret number, calculate the bitwise XOR of the
        given value and the secret number. Then, the secret number becomes the
        result of that operation. (If the secret number is 42 and you were to
        mix 15 into the secret number, the secret number would become 37.)
        """
        return num ^ value

    def prune(self, num) -> int:
        """
        To prune the secret number, calculate the value of the secret number
        modulo 16777216. Then, the secret number becomes the result of that
        operation. (If the secret number is 100000000 and you were to prune the
        secret number, the secret number would become 16113920.)

        :param num: _description_
        :type num: _type_
        :return: _description_
        :rtype: int
        """
        return num % 16777216

    def next_secret_number(self, num) -> int:
        """
        _summary_
        Calculate the result of multiplying the secret number by 64. Then, mix
        this result into the secret number. Finally, prune the secret number.
        Calculate the result of dividing the secret number by 32. Round the
        result down to the nearest integer. Then, mix this result into the
        secret number. Finally, prune the secret number.  Calculate the result
        of multiplying the secret number by 2048. Then, mix this result into the
        secret number. Finally, prune the secret number.


        :param num: _description_
        :type num: _type_
        :return: _description_
        :rtype: int
        """
        # Step 1
        mult: int = num * 64
        num = self.mix(num, mult)
        num = self.prune(num)

        # Step 2
        div: int = int(num / 32)
        num = self.mix(num, div)
        num = self.prune(num)

        # Step 3
        mult_2048: int = num * 2048
        num = self.mix(num, mult_2048)
        num = self.prune(num)

        return num

    def part_one(self) -> int:
        """
        Return the ...
        """

        # num = 123
        # for x in range(10):
        #     num = self.next_secret_number(num)
        #     print(f'After {x=}, {num=}')
        count: int = 0

        for initial_num in self.initial_numbers:
            n = self.generate_nth_secret_number(initial_num)
            count += n

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
    solver = Day22()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
