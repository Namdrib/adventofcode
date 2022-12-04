#!/usr/bin/python3
import sys

class Day01:
    """
    Solution for https://adventofcode.com/2022/day/1
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self._input: list = None

        # Represents the inventory of all the elves
        self._elf_inventory: list = []

        # The sum of each elf's inventory
        self._elf_inventory_sum: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line contains an integer, and groups of lines
        are separated by an empty line
        Each group contains the items carried by a single elf
        """
        _input = sys.stdin.read()

        # Represents the inventory of a single elf
        elf_inventory = []
        for line in _input.split('\n'):
            line = line.strip()

            if line:
                # Add contents to this elf's inventory
                elf_inventory.append(int(line))
            else:
                # Finished with the current elf, move on to the next
                self._elf_inventory.append(elf_inventory)
                elf_inventory = []

        # Get the total of each elf's inventory
        self._elf_inventory_sum = list(map(sum, self._elf_inventory))

    def part_one(self) -> int:
        """
        Return the elf with the highest total inventory
        """
        self._elf_inventory_sum.sort()
        return self._elf_inventory_sum[-1]

    def part_two(self) -> int:
        """
        Return the sum of the top 3 inventories
        """
        return sum(self._elf_inventory_sum[-3:])

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
