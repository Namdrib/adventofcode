#!/usr/bin/python3
import os
from queue import PriorityQueue
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Node:
    def __init__(self, bytes_: int, x: int, y: int) -> None:
        self.bytes: int = bytes_
        self.x: int = x
        self.y: int = y
        self.running_cost: int = 9e9

        self.parent: Node = None

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

    def path_find(self, start_x: int, start_y: int) -> Node:
        """
        Standard BFS to find a path from start_x, start_y to the bottom-right
        corner of the grid

        :param start_x: The x co-ordinate to start at
        :type start_x: int
        :param start_y: The y co-ordinate to start at
        :type start_y: int
        :return: The Node at the end, or None, if no path can be reached
        :rtype: Node
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
                return current

            # Explore each valid neighbour
            for neighbour_point in helpers.get_neighbours(current.x, current.y, self.grid):
                neighbour: Node = self.grid[neighbour_point.y][neighbour_point.x]

                if neighbour in closed:
                    continue

                # Into a wall
                if neighbour.bytes != 0:
                    continue

                # Is the current way to get to the neighbour the best way to get
                # to the neighbour so far?
                current_cost: int = neighbour.running_cost
                new_cost: int = current.running_cost + 1

                if new_cost < current_cost:
                    neighbour.running_cost = new_cost
                    neighbour.parent = current
                    fringe.put(neighbour)

            closed.add(current)

        # We couldn't get to the end. The path is blocked
        return None

    def get_path_points(self, node: Node) -> set:
        """
        Get all of the points on the path traversed by a given Node

        :param node: The node whose path to inspect
        :type node: Node
        :return: The set of points on the Node's path
        :rtype: set
        """
        # Use a set because the main operation on it will be a search
        out: set = set()

        x = node
        while x is not None:
            out.add(helpers.Point(x.x, x.y))
            x = x.parent

        return out

    def part_one(self) -> int:
        """
        Return how many steps are required to get to the end after a number of
        bytes have fallen
        """
        for byte in self.bytes[0:self.num_starting_bytes]:
            self.grid[byte.y][byte.x].bytes += 1

        for row in self.grid:
            for item in row:
                print(item.bytes, end='')
            print()

        num_steps = self.path_find(0, 0).running_cost
        return num_steps

    def part_two(self) -> int:
        """
        Return the co-ordinates of the first byte that completely blocks the
        path from the start to the end
        """
        # Get an initial path
        current = self.path_find(0, 0)
        path: set = self.get_path_points(current)

        # Keep dropping bytes, one-by-one, until there is no path.
        # Only update the path if the byte would have affected it
        for x in range(self.num_starting_bytes, len(self.bytes)):
            # Add a byte to the grid
            byte: helpers.Point = self.bytes[x]
            self.grid[byte.y][byte.x].bytes += 1

            # This byte disrupted the path. Re-calculate the path
            if byte in path:
                current = self.path_find(0, 0)
                path = self.get_path_points(current)

            # There's no path. This byte was the one that blocked the path
            if current is None:
                return f'{byte.x},{byte.y}'

        return '-1,-1'

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
