#e!/usr/bin/python3
import sys

class Day20:
    """
    Solution for https://adventofcode.com/2022/day/20
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.encrypted_file: list = []
        self.original: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()

        self.input = raw_input.splitlines()

        self.encrypted_file = list(map(int, self.input))
        print(self.encrypted_file)

        # Keep track of the original values and positions
        # This is used to determine which item to move at each step of the mixing
        self.original: list = [[x, i] for i, x in enumerate(self.encrypted_file)]

    def mix(self, encrypted_file: list) -> list:
        """
        Mix an encrypted file, returning the result
        To mix the file, move each number forward or backward in the file a
        number of positions equal to the value of the number being moved. The
        list is circular, so moving a number off one end of the list wraps back
        around to the other end as if the ends were connected.
        """
        # The order of the original numbers
        # TODO: make this work for subsequent runs.
        # The encrypted_file gets out of sync with self.original
        copy: list = [[x, i] for i, x in enumerate(encrypted_file)]
        # Set the i in copy to match the original index for that number
        for index, item in enumerate(copy):
            original_i = [i for x, i in self.original if x == item[0]][0]
            copy[index][1] = original_i
        # print(f'Copy: {copy}')

        for item, index in self.original:
            # print(f'  Looking for index {index} (value is {item})')
            # Find the index of the item that matches the original order
            item_index: int = [i for i, x in enumerate(copy) if x[1] == index][0]
            # Move the thing at that index to its new position
            # print(f'{item} is at {item_index} - deleting item at {item_index}')
            thing = copy.pop(item_index)
            new_index: int = (item_index + item) % len(copy)
            copy.insert(new_index, thing)
            # print(f'{thing} moves from {item_index} to {new_index}')

            # print(f'{[x[0] for x in copy]}\n')

        return [x for (x, i) in copy]

    def get_grove_coords(self, file) -> list:
        """
        Return the numbers at the 1000th, 2000th and 3000th pos after 0
        """
        zero_index = file.index(0)
        coords = [file[(zero_index+k) % len(file)] for k in [1000, 2000, 3000]]
        print(f'Coords: {coords}')
        return coords

    def part_one(self) -> int:
        """
        Return the sum of the grove coordinates after mixing the file once
        """
        decrypted_file: list = self.mix(self.encrypted_file)
        print(f'Decrypted: {decrypted_file}')

        grove_coordinates: list = self.get_grove_coords(decrypted_file)
        return sum(grove_coordinates)

    def part_two(self) -> int:
        """
        Apply the decryption key to the file
        Then return the sum of the grove coordinates after mixing the file ten times
        """
        decryption_key = 811589153
        file = [x * decryption_key for x in self.encrypted_file]
        self.original = [[x * decryption_key, i] for x, i in self.original]

        # print(f'Initial arrangement: {file}')
        for x in range(10):
            file = self.mix(file)
            # print(f'After {x+1} round of mixing: {file}')
        grove_coordinates: list = self.get_grove_coords(file)
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
