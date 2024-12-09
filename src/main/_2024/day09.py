#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day09:
    """
    Solution for https://adventofcode.com/2024/day/9
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.file: list = []
        self.file_lengths: dict = {}

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()[0]

    def expand_file(self, disk_map: str) -> list:
        """
        Expand the given disk map into its full form

        The disk map is a series of numbers, where each number describes the
        length of something. The first number is the length of a file. The
        second number is the length of free space. The files and free spaces
        alternate. Each file has an ID, starting with 0, and increasing by 1 for
        each subsequent file.

        For example:
        12345
        Expands into:
        0..111....22222
        Because there is:
        - a 1-length file with ID 0
        - a 2-length empty space
        - a 3-length file with ID 1
        - a 4-length empty space
        - a 5-length file with ID 2

        :param disk_map: The disk map to expand
        :type disk_map: str
        :return: A list representation of the expanded disk layout
        :rtype: list
        """
        expanded_file: list = []
        id_: int = 0
        for index, value in enumerate(disk_map):
            if index % 2 == 0:
                expanded_file.extend([id_ for _ in range(int(value))])
                self.file_lengths.setdefault(id_, int(value))
                id_ += 1
            else:
                expanded_file.extend([None for _ in range(int(value))])

        return expanded_file

    def compact_file(self, expanded_file: list) -> list:
        """
        Compact the given file by moving, from right-to-left, each file block
        into the first available empty space.

        :param expanded_file: The expanded file to compact
        :type expanded_file: list
        :return: The compacted file with all empty parts truncated
        :rtype: list
        """
        left: int = 0
        right: int = len(expanded_file) - 1

        while left < right:
            # "Walk" the left up to the first empty space
            while expanded_file[left] is not None:
                left += 1
            # "Walk the right down to the first non-empty space
            while expanded_file[right] is None:
                right -= 1
            if left >= right:
                break
            expanded_file[left], expanded_file[right] = expanded_file[right], expanded_file[left]

        # Remove all of the empty space
        # return expanded_file
        return expanded_file[0:left]

    def compact_file_whole_files(self, expanded_file: list) -> list:
        """
        Compact the given file by moving, from right-to-left, each whole file
        into the first available empty space. If there are no available empty
        spaces big enough for the file, then try the next file.

        This runs quite slowly (takes 8-10 seconds on a 5700X3D). I'm sure
        there's a better way to solve this by using the numbers in the original
        input, rather than simulating the whole process, but I can't be bothered
        right now.
        TODO: Make it run without simulation

        :param expanded_file: The expanded file to compact
        :type expanded_file: list
        :return: The compacted file
        :rtype: list
        """
        # Search from the end of the file backwards to the first valid number
        # in case there are empty positions at the end
        first_of_id = len(expanded_file)-1
        while expanded_file[first_of_id] is None:
            first_of_id -= 1

        # We know what the largest ID is, and where the first one is
        max_id: int = expanded_file[first_of_id]
        first_of_id = expanded_file.index(max_id)

        # For each ID from the right
        for id_ in range(max_id, 0, -1):
            # Find the length and position of first instance of the current ID
            first_of_id = expanded_file.index(id_)
            length = self.file_lengths[id_]

            # Find the first free space it fits in
            left = expanded_file.index(None)

            # Search all of the valid free spaces
            while left < first_of_id:
                # Find the size of the current free space
                next_nonfree_space = left
                while expanded_file[next_nonfree_space] is None:
                    next_nonfree_space += 1
                free_space = next_nonfree_space - left

                # Is it big enough to insert the current file?
                if free_space >= length:
                    break

                # If not, look for the next free space
                left = next_nonfree_space + 1
                while expanded_file[left] is not None:
                    left += 1

            # Don't allow left to go past the first of the ID
            if left >= first_of_id:
                continue

            # Move the ID from the right to the free space by swapping it with the empty space
            expanded_file[left:left+length], expanded_file[first_of_id:first_of_id+length] = \
                expanded_file[first_of_id:first_of_id+length], expanded_file[left:left+length]

        return expanded_file

    def calculate_checksum(self, compacted_file: list) -> int:
        """
        Calculate the checksum value of a file. A checksum is defined as:
        [The sum of] the result of multiplying each of these blocks' position
        with the file ID number it contains. The leftmost block is in position 0

        For example, for a file like:
        00.11.2.3
        Would product the checksum:
          0 * 0
        + 0 * 1
        + 1 * 3
        + 1 * 4
        + 2 * 6
        + 3 * 8
        =======
             44

        :param compacted_file: The compacted file to take the checksum of
        :type compacted_file: list
        :return: The checksum value
        :rtype: int
        """
        out: int = 0
        for i, value in enumerate(compacted_file):
            if value:
                out += i * value
        return out

    def part_one(self) -> int:
        """
        Return the checksum of the file after compressing the file by moving
        individual file blocks
        """
        expanded_file: list = self.expand_file(self.input)
        compacted_file: list = self.compact_file(expanded_file)
        checksum = self.calculate_checksum(compacted_file)
        return checksum

    def part_two(self) -> int:
        """
        Return the checksum of the file after compressing the file by moving
        whole files
        """
        expanded_file: list = self.expand_file(self.input)
        compacted_file: list = self.compact_file_whole_files(expanded_file)
        checksum = self.calculate_checksum(compacted_file)
        return checksum

def main() -> None:
    """
    Main
    """
    solver = Day09()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
