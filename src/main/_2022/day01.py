#!/usr/bin/python3
import sys

class day01:

    def __init__(self) -> None:
        self._input: list = None

        # Represents the inventory of all the elves
        self._elf_inventory: list = []

        # The sum of each elf's inventory
        self._elf_inventory_sum: list = []
        return

    def read_input(self) -> None:
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
        self._elf_inventory_sum = list(map(lambda x: sum(x), self._elf_inventory))

    def part_one(self) -> int:
        # Return the elf with the highest inventory
        self._elf_inventory_sum.sort()
        return self._elf_inventory_sum[-1]

    def part_two(self) -> int:
        # Return the sum of the top 3 inventories
        return sum(self._elf_inventory_sum[-3:])

def main() -> None:
    solver = day01()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
