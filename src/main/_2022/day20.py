#!/usr/bin/python3
import sys

class MixData:
    """
    A data structure to assist with mixing
    Keep track of a value, its index, and its original index
    There may be multiple MixData objects that have the same value
    """

    def __init__(self, value, original_index) -> None:
        self.value = value
        self.original_index = original_index

    def __eq__(self, other) -> bool:
        return self.value == other.value and self.original_index == other.original_index

    def __repr__(self) -> str:
        return f'MixData({self.value}, {self.original_index})'

    def __str__(self) -> str:
        return f'{self.value}'

class Day20:
    """
    Solution for https://adventofcode.com/2022/day/20
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        # A list of MixData, used to keep track of the original values _and_ their positions
        # This is used to determine the order in which the items will move when mixing
        self.original: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()

        self.input = raw_input.splitlines()

        # Turn the input into a list
        input_list: list = list(map(int, self.input))

        # Create MixData out of each item in the input list
        self.original: list = [MixData(x, i) for i, x in enumerate(input_list)]

    def mix(self, encrypted_file: list) -> None:
        """
        Mix an encrypted file in place
        1) To mix the file, move each number forward or backward in the file a
        number of positions equal to the value of the number being moved. The
        list is circular, so moving a number off one end of the list wraps back
        around to the other end as if the ends were connected.
        2) The numbers are moved in the order they appeared in the original,
        pre-mixed list.
        """
        # Because the MixData class has both the value and the original index,
        # we won't accidentally operate on a different with the same value

        # Because of 2), the original list is used to determine the move order
        for item in self.original:
            # Find where the item is in the current list
            current_index = encrypted_file.index(item)

            # Move it to its new position
            data: MixData = encrypted_file.pop(current_index)
            new_index: int = (current_index + item.value) % len(encrypted_file)
            encrypted_file.insert(new_index, data)
            # print(f'Moved {data} from {item_index} to {new_index}')

    def get_grove_coords(self, file) -> list:
        """
        Return the numbers at the 1000th, 2000th and 3000th pos after 0
        Because the file is a circular list, it doesn't matter where 0 is
        """
        # Find where zero is
        zero_index = [x.value for x in file].index(0)

        coords = [file[(zero_index+k) % len(file)].value for k in [1000, 2000, 3000]]
        print(f'Coords: {coords}')
        return coords

    def part_one(self) -> int:
        """
        Return the sum of the grove coordinates after mixing the file once
        """
        # Mixing occurs in-place, so make a copy of the original
        decrypted_file: list = list(self.original)
        self.mix(decrypted_file)
        print(f'Decrypted: {decrypted_file}')

        grove_coordinates: list = self.get_grove_coords(decrypted_file)
        return sum(grove_coordinates)

    def part_two(self) -> int:
        """
        Apply the decryption key to the file
        Then return the sum of the grove coordinates after mixing the file ten times
        """
        # Apply the decryption key to the file, transforming all its values
        decryption_key: int = 811589153
        self.original = [MixData(x.value * decryption_key, x.original_index) for x in self.original]

        # Mixing occurs in-place, so make a copy of the original
        decrypted_file: list = list(self.original)

        for mix_round in range(10):
            self.mix(decrypted_file)
            print(f'After {mix_round+1} round of mixing: {decrypted_file}')

        grove_coordinates: list = self.get_grove_coords(decrypted_file)
        return sum(grove_coordinates)

def main() -> None:
    """
    Main
    """
    solver = Day20()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
