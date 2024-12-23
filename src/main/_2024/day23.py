#!/usr/bin/python3
import itertools
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day23:
    """
    Solution for https://adventofcode.com/2024/day/23
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.connections: set = None
        self.all_connections: set = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.connections = set()
        for item in self.input:
            connection: tuple = tuple(item.split('-'))
            self.connections.add(connection)

    def compute_computer_sets(self) -> None:
        # {computer_name: [computer_names]}
        self.all_connections: dict = {}
        for c in self.connections:
            if c[0] not in self.all_connections:
                self.all_connections[c[0]] = []
            if c[1] not in self.all_connections:
                self.all_connections[c[1]] = []

            self.all_connections[c[0]].append(c[1])
            self.all_connections[c[1]].append(c[0])

    def get_sets_of_three(self) -> set:
        tri_connections: set = set()

        # We already know a and b are connected
        for a, b in self.connections:
            # See if there are any computers that are connected to both A and B
            for computer, connections in self.all_connections.items():
                if a in connections and b in connections:
                    tri_connections.add(tuple(sorted((a, b, computer))))

        return tri_connections

    def part_one(self) -> int:
        """
        Return the ...
        """
        self.compute_computer_sets()
        tri_connections: set = self.get_sets_of_three()

        # Count the tri-connections where any of the computers starts with t
        count: int = 0
        for tc in tri_connections:
            if any(x.startswith('t') for x in tc):
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
    solver = Day23()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
