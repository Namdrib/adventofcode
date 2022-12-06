#!/usr/bin/python3
import sys

class Day06:
    """
    Solution for https://adventofcode.com/2022/day/6
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self._input: list = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()

        self._input = raw_input.split('\n')
        self._input = self._input[0:-1]

    def _find_marker(self, message: str, length: int = 4) -> str:
        """
        Given a message and a length, find the first sequence of that
        length where all the characters are different
        Return the marker
        """
        # Sliding window
        for i in range(len(message)-length):
            # Find the slice of that size
            candidate_marker: str = message[i:i+length]

            # All characters are unique
            if len(set(candidate_marker)) == length:
                return candidate_marker

        # No marker exists for that length
        return None

    def part_one(self) -> int:
        """
        Return how many characters have been received once the start of packet marker is detected
        The start of packet marker is a string where all 4 characters are different
        """
        marker: str = self._find_marker(self._input[0])
        marker_pos = self._input[0].find(marker)
        return marker_pos + len(marker)

    def part_two(self) -> int:
        """
        Return how many characters have been received once the start of message marker is detected
        The start of message marker is a string where all 14 characters are different
        """
        marker: str = self._find_marker(self._input[0], 14)
        marker_pos = self._input[0].find(marker)
        return marker_pos + len(marker)

def main() -> None:
    """
    Main
    """
    solver = Day06()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
