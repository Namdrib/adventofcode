#!/usr/bin/python3
import os
from pprint import pprint
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

        pprint(self.device_outputs)

    def count_paths_from(self, start: str, end: str, problematic_devices: list = []) -> int:
        paths: list = []
        self._count_paths_from(start, end, [], paths, problematic_devices)
        return len(paths)

    def _count_paths_from(self, current: str, end: str, path: list, paths: list, problematic_devices: list = []):
        # Add the current path
        path.append(current)

        if current == end:
            copy = [x for x in path]
            if problematic_devices:
                if all(pd in copy for pd in problematic_devices):
                    pprint(copy)
                    paths.append(copy)
            else:
                paths.append(copy)
            path.pop(-1)
            return

        for neighbour in self.device_outputs[current]:
            if self._count_paths_from(neighbour, end, path, paths, problematic_devices):
                acc += 1
        
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
        count = self.count_paths_from('svr', 'out', ['dac', 'fft'])
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
