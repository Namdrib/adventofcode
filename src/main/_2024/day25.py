#!/usr/bin/python3
import sys

class Day25:
    """
    Solution for https://adventofcode.com/2024/day/25
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        # List of list of ints
        self.locks: list = []

        # List of list of ints
        self.keys: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each set of 7 lines (a header, 5 in the body, a footer)
        describes a key or a lock.
        The header of a lock is all '#' characters, and the footer is all '.'
        The header of a key is all '.' characters, and the footer is all '#'

        There is an empty lien separating each key/lock
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        for i in range(0, len(self.input), 8):
            # Read the next 5 lines to see the body of the lock/pin
            pins = list(x for x in self.input[i+1:i+6])
            # Transpose the 2D list
            pins = list(zip(*pins))

            pin_counts: list = []
            for pin in pins:
                # The length of the pin (for both keys and locks) is the number
                # of #
                # For locks, these would start from the top, down
                # For keys, these would start from the bottom, up
                pin_counts.append(pin.count('#'))

            # Determine whether the pins are for a key or a lock
            if self.input[i] == '#####':
                self.locks.append(pin_counts)
            else:
                self.keys.append(pin_counts)

    def could_match(self, key: list, lock: list) -> bool:
        """
        Return whether all of the pins in the key are able to fit with all of
        the pins in the lock
        This allows for key pins that are shorter that what the lock allows

        Key and lock are both lists of N ints, as long as N matches. Each of the
        ints are between 0-5 (inclusive)

        :param key: The key to try (N ints)
        :type key: list
        :param lock: The lock to try (N ints)
        :type lock: list
        :return: Whether the key could possibly work with the lock
        :rtype: bool
        """
        return all(x + y <= 5 for x, y in zip(key, lock))

    def part_one(self) -> int:
        """
        Return how many unique lock/key pairs fit together without overlapping
        in any column
        """
        count: int = 0

        # Try each key in each lock, counting how many could match
        for lock in self.locks:
            for key in self.keys:
                if self.could_match(key, lock):
                    count += 1

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
    solver = Day25()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
