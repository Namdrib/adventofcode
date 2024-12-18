#!/usr/bin/python3
import os
from queue import PriorityQueue
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Node:
    def __init__(self, bytes_: int, x: int, y: int) -> None:
        self.bytes = bytes_
        self.x = x
        self.y = y
        self.running_cost = 9e9

    # For use with set/dict
    def __eq__(self, o) -> int:
        return self.x == o.x and self.y == o.y

    # For use with set/dict and queue.PriorityQueue
    def __hash__(self) -> int:
        return hash((self.x, self.y))

    # For use with queue.PriorityQueue
    def __lt__(self, o) -> bool:
        return self.running_cost < o.running_cost

class Day18:
    """
    Solution for https://adventofcode.com/2024/day/18
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.bytes: list = None
        self.grid: list = None

        self.num_starting_bytes: int = 1024
        self.grid_size: int = 70

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.bytes = []
        for item in self.input:
            x, y = list(map(int, item.split(',')))
            self.bytes.append(helpers.Point(x, y))

        # Initialise each item on the grid to be a Node with the same
        # co-ordinates
        self.grid = [
            [Node(0, x, y) for x in range(self.grid_size+1)]
            for y in range(self.grid_size+1)
        ]

    def populate_grid(self, bytes_: list) -> None:
        """
        Have bytes fall onto the grid

        :param bytes_: The list of bytes to add to the grid
        :type bytes_: list
        """
        for byte in bytes_:
            self.grid[byte.y][byte.x].bytes += 1

    def path_find(self, start_x: int, start_y: int) -> int:
        """
        Standard BFS to find a path from start_x, start_y to the bottom-right
        corner of the grid

        :param start_x: The x co-ordinate to start at
        :type start_x: int
        :param start_y: The y co-ordinate to start at
        :type start_y: int
        :return: The cost required to get to the end, or -1 if no path can be reached
        :rtype: int
        """
        fringe: PriorityQueue = PriorityQueue()

        # Initialise costs
        for row in self.grid:
            for node in row:
                node.running_cost = 9e9

        # The starting point costs 0
        self.grid[start_y][start_x].running_cost = 0
        start_node: Node = self.grid[start_y][start_x]
        fringe.put(start_node)

        closed: set = set()

        while not fringe.empty():
            current = fringe.get()

            # Reached the end
            if current.x == len(self.grid)-1 and current.y == len(self.grid[0])-1:
                return self.grid[current.y][current.x].running_cost

            # Explore each valid neighbour
            for neighbour_point in helpers.get_neighbours(current.x, current.y, self.grid):
                neighbour: Node = self.grid[neighbour_point.y][neighbour_point.x]

                if neighbour in closed:
                    continue

                # Into a wall
                if self.grid[neighbour.y][neighbour.x].bytes != 0:
                    continue

                # Is the current way to get to the neighbour the best way to get
                # to the neighbour so far?
                current_cost: int = self.grid[neighbour.y][neighbour.x].running_cost
                new_cost: int = self.grid[current.y][current.x].running_cost + 1

                if new_cost < current_cost:
                    self.grid[neighbour.y][neighbour.x].running_cost = min(new_cost, current_cost)
                    fringe.put(neighbour)

            closed.add(current)

        # We couldn't get to the end. The path is blocked
        return -1

    def part_one(self) -> int:
        """
        Return how many steps are required to get to the end after a number of
        bytes have fallen
        """
        self.populate_grid(self.bytes[0:self.num_starting_bytes])

        for row in self.grid:
            for item in row:
                print(item.bytes, end='')
            print()

        num_steps = self.path_find(0, 0)
        return num_steps

    def part_two(self) -> int:
        """
        Return the co-ordinates of the first byte that completely blocks the
        path from the start to the end
        """
        # Keep dropping bytes, one-by-one, until the path find returns -1
        # This takes a while to run.
        for x in range(self.num_starting_bytes, len(self.bytes)):
            self.populate_grid(self.bytes[x:x+1])

            if self.path_find(0, 0) == -1:
                return ','.join([str(self.bytes[x].x), str(self.bytes[x].y)])

def main() -> None:
    """
    Main
    """
    solver = Day18()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
