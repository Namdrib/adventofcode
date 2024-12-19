#!/usr/bin/python3
import sys

class Day19:
    """
    Solution for https://adventofcode.com/2024/day/19
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.towels: list = None
        self.displays: list = None

        # Memoisation for how many ways there are to make a given display
        # num_ways[pattern] is the number of ways pattern can be formed with the
        # available towels
        self.num_ways: dict = {}

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, the first line is a comma-space separated line of towels
        The second line is empty
        All subsequent lines are a display

        Towels and displays are letters in [w,u,r,b,g]
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        # The first line is the towels
        # The second line is a blank
        # All other lines are displays
        towels, _, *self.displays = self.input
        self.towels: list = towels.split(', ')

    def num_ways_to_make_display(self, display: str, towels: list) -> int:
        # Cached case: We already know how many ways there are to make display
        if display in self.num_ways:
            return self.num_ways[display]

        # Base case: This was an exact match / new way
        if len(display) == 0:
            return 1

        num_ways: int = 0
        for towel in towels:
            if display.startswith(towel):
                # The remaining part of this display after using this towel
                sub_display: str = display[len(towel):]
                # How many ways can we make the remaining part?
                num_ways += self.num_ways_to_make_display(sub_display, towels)

        # Update the cache
        self.num_ways[display] = num_ways
        return num_ways

    def part_one(self) -> int:
        """
        Return the number of display patterns that can be made with the
        available towels
        """
        # A display can be made if there is a non-zero number of ways to make it
        return sum(bool(self.num_ways_to_make_display(display, self.towels)) for display in self.displays)

    def part_two(self) -> int:
        """
        Return the sum of the number of ways each display pattern can be made
        with the available towels
        Part one will have already populated the memoisation structure, so this
        should be really quick
        """
        # Count 'em up
        return sum(self.num_ways_to_make_display(display, self.towels) for display in self.displays)

def main() -> None:
    """
    Main
    """
    solver = Day19()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
