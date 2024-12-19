#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

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

        self.available_displays: set = set()
        self.unavailable_displays: set = set()

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.towels = []
        self.displays = []
        
        reading_towels: bool = True
        for item in self.input:
            if reading_towels:
                self.towels = item.split(', ')
                reading_towels = False
            else:
                if item:
                    self.displays.append(item)

    def can_make_display(self, display: str, towels: list) -> bool:
        # print(f'Seeing if we can make {display}')
        # if not display:
        #     return False

        if display in self.available_displays:
            return True

        if display in self.unavailable_displays:
            return False

        can_make: bool = False
        for towel in towels:

            if len(display) < len(towel):
                continue

            if display == towel:
                self.available_displays.add(display)
                return True

            if display.startswith(towel):
                sub_display: str = display[len(towel):]
                print(f'\tTrying with {towel}|{sub_display}')
                if self.can_make_display(sub_display, towels):
                    can_make = True
                    self.available_displays.add(display)
                    break
                # if self.can_make_display(sub_display, towels):
                #     return can_make

        if not can_make:
            self.unavailable_displays.add(display)

        return can_make

    def part_one(self) -> int:
        """
        Return the ...
        """
        count: int = 0

        # self.can_make_display(self.displays[0], self.towels)
        for display in self.displays:
            if self.can_make_display(display, self.towels):
                count += 1

        print(f'We can make {self.available_displays}')
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
    solver = Day19()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
