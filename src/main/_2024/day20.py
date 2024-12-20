#!/usr/bin/python3
from queue import PriorityQueue
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Node:
    def __init__(self, tile: str, x: int, y: int) -> None:
        self.tile: int = tile
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

class Day20:
    """
    Solution for https://adventofcode.com/2024/day/20
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.grid = None
        self.count: int = 0

        self.start = None
        self.end = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, the input is a grid of '#' and '.', representing walls,
        and empty spaces, respectively.
        There is also a 'S' and 'E' representing the start and end points.
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.grid = []
        for y, item in enumerate(self.input):
            row: list = []
            print(item)
            for x, char in enumerate(item):
                if char == 'S':
                    self.start = helpers.Point(x, y)
                if char == 'E':
                    self.end = helpers.Point(x, y)
                row.append(Node(char, x, y))
            self.grid.append(row)

    def path_find(self) -> Node:
        """
        Standard BFS to find a path from the self.start to self.end

        :return: The Node at the end, or None, if no path can be reached
        :rtype: Node
        """
        fringe: PriorityQueue = PriorityQueue()

        # Initialise costs
        for row in self.grid:
            for node in row:
                node.running_cost = 9e9

        # The starting point costs 0
        self.grid[self.start.y][self.start.x].running_cost = 0
        start_node: Node = self.grid[self.start.y][self.start.x]
        fringe.put(start_node)

        closed: set = set()

        while not fringe.empty():
            current = fringe.get()

            # Reached the end
            if current.x == self.end.x and current.y == self.end.y:
                return current

            # Explore each valid neighbour
            for neighbour_point in helpers.get_neighbours(current.x, current.y, self.grid):
                neighbour: Node = self.grid[neighbour_point.y][neighbour_point.x]

                if neighbour in closed:
                    continue

                # Into a wall
                if neighbour.tile == '#':
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

    def part_one(self) -> int:
        """
        Return the number of cheats that would allow saving at least 100 picoseconds
        """
        count: int = 0

        # How much would it cost to finish the race without cheating?
        normal_cost: int = self.path_find().running_cost

        # How many picoseconds does cheating on a certain point save us?
        # {helpers.Point, int}
        cheat_benefits: dict = {}

        # For each position
        for y, row in enumerate(self.grid):
            for x, node in enumerate(row):
                # We can only cheat through walls
                if node.tile != '#':
                    continue

                # See what the benefit would be for cheating here
                cheat_start = helpers.Point(x, y)

                # See whether it's worth checking if this cheat would save any time
                # i.e., can we actually make use of it?
                can_cheat: bool = False
                for d in helpers.get_directions():
                    cheat_end = helpers.Point(cheat_start.x + d['x'], cheat_start.y + d['y'])
                    if helpers.in_range_2d(self.grid, cheat_end.x, cheat_end.y) \
                            and self.grid[cheat_end.y][cheat_end.x].tile != '#':
                        can_cheat = True
                        break

                if can_cheat:
                    # Apply the cheat and see if it helps
                    original_start: str = self.grid[cheat_start.y][cheat_start.x].tile
                    self.grid[cheat_start.y][cheat_start.x].tile = '.'

                    new_cost: int = self.path_find().running_cost

                    # How much better is it now?
                    benefit: int = normal_cost - new_cost
                    cheat_benefits[cheat_start] = benefit

                    print(f'Cheat {cheat_start} saves {benefit} picoseconds')

                    # Put the board back the way it was for next round
                    # self.grid[cheat_end.y][cheat_end.x].tile = original_end
                    self.grid[cheat_start.y][cheat_start.x].tile = original_start

        # print(cheat_benefits)

        # Count how frequently each time saving happens
        savings_frequencies: dict = {}
        for savings in cheat_benefits.values():
            savings_frequencies[savings] = savings_frequencies.get(savings, 0) + 1

        count: int = 0
        for savings, frequency in savings_frequencies.items():
            if savings >= 100:
                count += frequency
        print(savings_frequencies)

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
    solver = Day20()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
