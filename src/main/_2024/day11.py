#!/usr/bin/python3
import copy
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day11:
    """
    Solution for https://adventofcode.com/2024/day/11
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.starting_stones: list = []

        # Memoisation for how many stones there are for a given stone when there are N steps left
        # dict[stone][steps_left] is how many stones there will be in place of
        # this stone after steps_left steps
        self.size_after_steps: dict = {}

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.starting_stones = list(map(int, self.input[0].split(" ")))

    def transform(self, stone: int) -> list:
        """
        Apply a tranformation to a stone

        :param stone: The stone to transform
        :type stones: list
        :return: The new stone(s) after transforming
        :rtype: list
        """
        # If the stone is 0, make it 1
        if stone == 0:
            return [1]

        # If the length of stone is even, split it down the middle
        stone_str: str = str(stone)
        if len(stone_str) % 2 == 0:
            half: int = int(len(stone_str)/2)
            left, right = stone_str[0:half], stone_str[half:]
            return list(map(int, [left, right]))

        # No other rules matched. Multiply it by 2024
        return [stone * 2024]

    def calculate_num_stones(self, stone: int, steps_left: int) -> int:
        """
        Calculate how many stones will be in the place of the given stone after
        a number of steps. For example, calculate_next_size(7, 3) will be how
        many stones exist for stone 7 after 3 steps

        :param stone: The stone to calculate
        :type stone: int
        :param steps_left: How many steps to take from this stone
        :type steps_left: int
        :return: How many stones will be in this stone's place
        :rtype: int
        """
        # We already know how big this stone will be when there's steps_left
        # left, so we can return that early
        if steps_left in self.size_after_steps.get(stone, {}):
            return self.size_after_steps[stone][steps_left]

        # At the end, each stone will no longer change
        if steps_left == 0:
            if stone in self.size_after_steps:
                self.size_after_steps[stone][0] = 1
            else:
                self.size_after_steps[stone] = {0: 1}
            return 1

        # Pull the size of each new stone from the dictionary, calculating the
        # new value if it isn't already in there
        next_stones: list = self.transform(stone)
        next_size: int = 0
        for next_stone in next_stones:
            next_size += self.size_after_steps.get(stone, {}).get(steps_left, self.calculate_num_stones(next_stone, steps_left-1))

        # Save the calculated value for _this_ stone
        if stone in self.size_after_steps:
            self.size_after_steps[stone][steps_left] = next_size
        else:
            self.size_after_steps[stone] = {steps_left: next_size}
        return next_size

    def part_one(self) -> int:
        """
        Return how many stones there are after 25 blinks

        I originally wanted to keep this as the original naive simulation
        solution, but running it with memoisation speeds part 2 up
        """
        n: int = 25
        stones: list = copy.deepcopy(self.starting_stones)

        return sum(self.calculate_num_stones(stone, n) for stone in stones)

    def part_two(self) -> int:
        """
        Return how many stones there are after 75 blinks

        Because part 1 already ran, the lookup table is already partially
        populated. That should make this part run faster, as there are fewer
        stone/step combinations to calculate from scratch
        """
        n: int = 75
        stones: list = copy.deepcopy(self.starting_stones)

        return sum(self.calculate_num_stones(stone, n) for stone in stones)

def main() -> None:
    """
    Main
    """
    solver = Day11()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
