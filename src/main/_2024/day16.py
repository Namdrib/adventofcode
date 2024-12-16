#!/usr/bin/python3
import os
from queue import PriorityQueue
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Node:
    """
    A node used for pathfinding in 3D space (x, y, direction)
    """
    def __init__(self, char: str, x: int, y: int, dir_: int, total_score: int) -> None:
        self.char: str = char

        self.x: int = x
        self.y: int = y
        self.dir: int = dir_

        self.total_score: int = total_score

        # To trace the path back from the end to the start
        self.parent: Node = None

    # For use with set/dict
    def __eq__(self, o) -> int:
        return self.x == o.x and self.y == o.y and self.dir == o.dir

    # For use with set/dict and queue.PriorityQueue
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.dir))

    # For use with queue.PriorityQueue
    def __lt__(self, o) -> bool:
        return self.total_score < o.total_score

    def __repr__(self) -> str:
        arrow: str = helpers.arrow_directions[self.dir]
        return f'Node({self.char}, {self.x}, {self.y}, {arrow}, {self.total_score})'

class Day16:
    """
    Solution for https://adventofcode.com/2024/day/16
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.grid: list = None

        self.start_x: int = -1
        self.start_y: int = -1

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.grid = []

        # 3-dimensional grid for the X, Y, and arrow dimension
        for y, item in enumerate(self.input):
            row: list = []
            for x, char in enumerate(item):
                dir_dim: list = []

                if char == 'S':
                    self.start_x = x
                    self.start_y = y

                # Consider all directions for all points
                for i, _ in enumerate(helpers.arrow_directions):
                    n: Node = Node(char, x, y, i, 9e99)
                    dir_dim.append(n)
                row.append(dir_dim)
            self.grid.append(row)

    def get_neighbours(self, node: Node) -> list:
        """
        Get the neighbours of the given Node

        The possible actions from a point are:
        - Go straight one space (cost: 1)
        - Rotate left 90 degrees (cost: 1000)
        - Rotate right 90 degrees (cost: 1000)

        :param node: The Node to get neighbours for
        :type node: Node
        :return: A list of all neighbours for the given Node
        :rtype: list
        """
        neighbours: list = []

        # Go straight (if we can)
        new_dir_deltas = next(helpers.get_directions([helpers.arrow_directions[node.dir]]))
        next_x = node.x + new_dir_deltas['x']
        next_y = node.y + new_dir_deltas['y']

        # Make sure we're in bounds and not in a wall
        if helpers.in_range_2d(self.grid, next_x, next_y):
            if self.grid[next_y][next_x][node.dir].char != '#':
                node_straight: Node = Node(node.char, next_x, next_y, node.dir, node.total_score + 1)
                node_straight.parent = node
                neighbours.append(node_straight)

        # Rotate left
        direction_left: int = node.dir - 1
        if direction_left < 0:
            direction_left += len(helpers.arrow_directions)
        node_left: Node = Node(node.char, node.x, node.y, direction_left, node.total_score + 1000)
        node_left.parent = node
        neighbours.append(node_left)

        # Rotate right
        direction_right: int = node.dir + 1
        direction_right %= len(helpers.arrow_directions)
        node_right: Node = Node(node.char, node.x, node.y, direction_right, node.total_score + 1000)
        node_right.parent = node
        neighbours.append(node_right)

        return neighbours

    def path_find(self, start_x: int, start_y: int, check_all_paths: bool = False) -> Node|list:
        """
        Use Dijkstra's algorithm to find the shortest path(s) from the given
        start position to the end (denoted with E).
        For part one, return the first shortest path to the end
        For part two, return all shortest paths

        :param start_x: The X position to start at
        :type start_x: int
        :param start_y: The Y position to start at
        :type start_y: int
        :param check_all_paths: Used for part two. Whether to check all paths, defaults to False
        :type check_all_paths: bool, optional
        :return: The shortest path (or paths, for part two)
        :rtype: Node|list
        """
        fringe: PriorityQueue = PriorityQueue()

        start_node: Node = Node('.', start_x, start_y, helpers.arrow_directions.index('>'), 0)
        fringe.put(start_node)

        # For part 2, keep track of {node, best_score_so_far}
        seen: dict = {}

        end_paths: list = []

        while not fringe.empty():
            current: Node = fringe.get()

            # Only stop exploring this node if we're worse than the best so far
            # Otherwise we might still have a chance to improve or be the same
            # Used for part 2 to track all best paths
            if current.total_score > seen.get(current, 9e99):
                continue

            # We've hit the end
            if self.grid[current.y][current.x][current.dir].char == 'E':
                # For part two, keep track of all the paths that have gotten here
                # Otherwise, just return the first path we get
                if check_all_paths:
                    # Force it to ignore all paths that have cost more (e.g., rotating on the spot)
                    if not end_paths or any(current.total_score <= x.total_score for x in end_paths):
                        end_paths.append(current)
                        continue
                else:
                    return current

            for neighbour in self.get_neighbours(current):
                if neighbour.total_score > seen.get(neighbour, 9e99):
                    continue

                # Record the best score to get to the neighbour so far
                existing_score: int = self.grid[neighbour.y][neighbour.x][neighbour.dir].total_score
                best_total_score: int = min(existing_score, neighbour.total_score)
                self.grid[neighbour.y][neighbour.x][neighbour.dir].total_score = best_total_score

                fringe.put(neighbour)

            # Allow multiple ways to get to the end from here
            seen[current] = min(seen.get(current, 9e99), current.total_score)

        return end_paths

    def part_one(self) -> int:
        """
        Return the score of the best path from S to E
        """
        end_path: Node = self.path_find(self.start_x, self.start_y)
        return end_path.total_score

    def part_two(self) -> int:
        """
        Return the number of (x, y) locations that are along any of the best
        paths from S to E
        """
        end_paths: list = self.path_find(self.start_x, self.start_y, True)

        unique_points_on_any_best_path: set = set()

        # Follow all of the best paths back to the start, keeping track of all
        # locations that have been visited
        for end_path in end_paths:
            current = end_path
            while current is not None:
                unique_points_on_any_best_path.add(helpers.Point(current.x, current.y))
                current = current.parent

        return len(unique_points_on_any_best_path)

def main() -> None:
    """
    Main
    """
    solver = Day16()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
