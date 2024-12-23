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

        self.cost_from_points: dict = {}

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
            for x, char in enumerate(item):
                if char == 'S':
                    self.start = helpers.Point(x, y)
                if char == 'E':
                    self.end = helpers.Point(x, y)
                row.append(Node(char, x, y))
            self.grid.append(row)

    def path_find(self, start_x: int, start_y: int) -> Node:
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
        self.grid[start_y][start_x].running_cost = 0
        start_node: Node = self.grid[start_y][start_x]
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

    def calculate_cheat_benefits(self, cheat_time: int) -> dict:
        # How much would it cost to finish the race without cheating?
        normal_run_from_start: Node = self.path_find(self.start.x, self.start.y)
        normal_cost_from_start = normal_run_from_start.running_cost

        # Work back through the path: how much longer to go until the end?
        node = normal_run_from_start
        while node:
            self.cost_from_points[(node.x, node.y)] = normal_cost_from_start - node.running_cost
            node = node.parent

        # How much does each possible cheat (defined by start and end) give?
        # {(start_x, start_y, end_x, end_y): benefit}
        cheat_benefits: dict = {}

        # Working back through the path, how much benefit can we get from
        # cheating at each point?
        node = normal_run_from_start
        while node:
            # All of the possible places that cheating could take us to
            # Filter down to places we can actually end up when the cheat ends
            # i.e., be in bounds, don't re-appear in a wall
            reachable: set = {
                p for p in helpers.get_grid_diamond(node.x, node.y, cheat_time)
                if helpers.in_range_2d(self.grid, p[0], p[1]) and
                # This can't be == '.', as that doesn't take into account S/E
                self.grid[p[1]][p[0]].tile != '#'
            }

            for point in reachable:
                dx: int = abs(point[0] - node.x)
                dy: int = abs(point[1] - node.y)
                distance_travelled_in_cheat: int = dx + dy

                time_from_cheat_end_to_dest = self.cost_from_points[(point[0], point[1])]

                # 1. How far we travelled until we used the cheat
                # 2. How far we travelled while cheating
                # 3. How far left to go after we stop cheating
                cost_with_cheat: int = node.running_cost + distance_travelled_in_cheat + time_from_cheat_end_to_dest
                cheat_benefit: int = normal_cost_from_start - cost_with_cheat

                # Only record states where the cheat actually helps
                if cheat_benefit > 0:
                    cheat_benefits[(node.x, node.y, point[0], point[1])] = cheat_benefit

            node = node.parent

        return cheat_benefits

    def part_one(self) -> int:
        """
        Return the number of cheats that would save at least 100 picoseconds, if
        they could run for up to 2 picoseconds
        """
        count: int = 0

        cheat_benefits: dict = self.calculate_cheat_benefits(2)

        for benefit in cheat_benefits.values():
            if benefit >= 100:
                count += 1

        return count

    def part_two(self) -> int:
        """
        Return the number of cheats that would save at least 100 picoseconds, if
        they could run for up to 20 picoseconds
        """
        count: int = 0

        cheat_benefits: dict = self.calculate_cheat_benefits(20)

        for benefit in cheat_benefits.values():
            if benefit >= 100:
                count += 1

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
