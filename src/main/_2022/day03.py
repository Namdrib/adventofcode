#!/usr/bin/python3
import sys

class Day03:
    """
    Solution for https://adventofcode.com/2022/day/3
    """


    def __init__(self) -> None:
        """
        Constructor
        """
        self._input: list = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line contains a bunch of characters
        Each character represents a type of item
        """
        raw_input = sys.stdin.read()

        self._input = raw_input.split('\n')
        self._input = self._input[0:-1]

    def _find_common_component_in_rucksack(self, rucksack: str) -> str:
        """
        Divide the rucksack into halves (left, right)
        Find the items that appear in both halves
        """
        left: str = rucksack[:int(len(rucksack)/2)]
        right: str = rucksack[int(len(rucksack)/2):]

        # Intersection of sets
        common_component_set: set = set(left) & set(right)
        return list(common_component_set)[0]

    def _calculate_item_priority(self, component: str) -> int:
        """
        Calculate the priority of an item as follows:
        a-z is 1-26, respectively
        A-Z is 27-52, respectively
        """
        if component.isupper():
            return ord(component) - 38
        return ord(component) - 96

    def part_one(self) -> int:
        """
        Return the sum of the priorities of the common components of each individual rucksack
        """
        total_priority: int = 0
        for rucksack in self._input:
            common_component: str = self._find_common_component_in_rucksack(rucksack)
            priority: int = self._calculate_item_priority(common_component)
            total_priority += priority

        return total_priority

    def part_two(self) -> int:
        """
        Return the sum of the priorities of the common components across each group of 3 rucksacks
        """
        total_priority: int = 0
        for i in range(0, len(self._input), 3):
            # Intersection of sets
            common_component_set: set = set(self._input[i]) & set(self._input[i+1]) & set(self._input[i+2])
            common_component: str = list(common_component_set)[0]
            priority: int = self._calculate_item_priority(common_component)
            total_priority += priority

        return total_priority

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
