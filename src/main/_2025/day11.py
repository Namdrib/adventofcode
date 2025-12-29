#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day11:
    """
    Solution for https://adventofcode.com/2025/day/11
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.device_outputs: dict = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line describes a *device* and all other connected
        devices
        The structure is:
        aaa: bbb ccc
        Which says that device aaa has outputs to devices bbb and ccc
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.device_outputs: dict = dict()

        for item in self.input:
            device, outputs = item.split(': ')
            outputs = outputs.split()
            self.device_outputs[device] = outputs

    def count_paths_from(self, start: str, end: str) -> int:
        # Memoise how many times each node can reach the end
        paths_to_end: dict = dict()

        self._count_paths_from(start, end, [], paths_to_end)
        return paths_to_end[start]

    def _count_paths_from(self, current: str, end: str, path: list, memo: dict) -> int:
        if current in memo:
            return memo[current]

        # Add the current path
        path.append(current)

        # We've reached the end
        if current == end:
            copy = [x for x in path]

            memo[current] = 1
            path.pop(-1)
            return memo[current]

        total_paths_to_end: int = 0
        for neighbour in self.device_outputs.setdefault(current, []):
            if neighbour not in memo:
                num_paths = self._count_paths_from(neighbour, end, path, memo)
                memo[neighbour] = num_paths

            total_paths_to_end += memo[neighbour]
        memo[current] = total_paths_to_end
        return memo[current]

        # Backtrack
        path.pop(-1)

    def part_one(self) -> int:
        """
        Return the number of unique paths from the device `you` to the device
        `out`
        """
        count: int = 0
        count = self.count_paths_from('you', 'out')
        return count

    def part_two(self) -> int:
        """
        Return the number of unique paths from the device `svr` to the device
        `out` that also pass through `dac` and `fft`
        """
        count: int = 0

        # How many paths from svr -> fft -> dac -> out
        p1_1: int = self.count_paths_from('svr', 'fft')
        p1_2: int = self.count_paths_from('fft', 'dac')
        p1_3: int = self.count_paths_from('dac', 'out')
        p1: int = p1_1 * p1_2 * p1_3

        # How many paths from svr -> dac -> fft -> out
        p2_1: int = self.count_paths_from('svr', 'dac')
        p2_2: int = self.count_paths_from('dac', 'fft')
        p2_3: int = self.count_paths_from('fft', 'out')
        p2: int = p2_1 * p2_2 * p2_3

        count = p1 + p2
        return count

def main() -> None:
    """
    Main
    """
    solver = Day11()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
