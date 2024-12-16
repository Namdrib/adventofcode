#!/usr/bin/python3
import os
from queue import PriorityQueue, Queue
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Node:
    def __init__(self, char: str, x: int, y: int, dir_: int, total_score: int) -> None:
        self.char: str = char

        self.x: int = x
        self.y: int = y
        self.dir: int = dir_

        self.total_score: int = total_score

    # For use with set
    def __eq__(self, o) -> int:
        return self.x == o.x and self.y == o.y and self.dir == o.dir

    # For use with set and queue.PriorityQueue
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.dir))

    # For use with queue.PriorityQueue
    def __lt__(self, o) -> bool:
        return self.total_score < o.total_score

    def __repr__(self) -> str:
        return f'Node({self.char}, {self.x}, {self.y}, {helpers.arrow_directions[self.dir]}, {self.total_score})'

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
                for i, _ in enumerate(helpers.arrow_directions):
                    n: Node = Node(char, x, y, i, 9e99)
                    dir_dim.append(n)
                row.append(dir_dim)
            self.grid.append(row)

    def find_xy_position(self, position: str) -> tuple:
        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                if char[0].char == position:
                    return (x, y)

        return (-1, -1)

    def get_neighbours(self, node: Node) -> list:
        neighbours: list = []

        # Go straight (if we can)
        new_dir_deltas = next(helpers.get_directions([helpers.arrow_directions[node.dir]]))
        next_x = node.x + new_dir_deltas['x']
        next_y = node.y + new_dir_deltas['y']

        # Make sure we're in bounds and not in a wall
        if helpers.in_range_2d(self.grid, next_x, next_y):
            if self.grid[next_y][next_x][node.dir].char != '#':
                node_straight: Node = Node(node.char, next_x, next_y, node.dir, node.running_cost + 1)
                neighbours.append(node_straight)

        # Rotate left
        direction_left: int = node.dir - 1
        if direction_left < 0:
            direction_left += len(helpers.arrow_directions)
        node_left: Node = Node(node.char, node.x, node.y, direction_left, node.running_cost + 1000)
        neighbours.append(node_left)

        # Rotate right
        direction_right: int = node.dir + 1
        direction_right %= len(helpers.arrow_directions)
        node_right: Node = Node(node.char, node.x, node.y, direction_right, node.running_cost + 1000)
        neighbours.append(node_right)

        return neighbours

    def pathfind(self, start_x: int, start_y: int) -> int:
        fringe: PriorityQueue = PriorityQueue()

        start_node: Node = Node('.', start_x, start_y, helpers.arrow_directions.index('>'), 0)
        fringe.put(start_node)

        seen: set = set()

        counter: int = 0

        while not fringe.empty():
            current: Node = fringe.get()
            print(f'{current=}')

            if current in seen:
                continue

            # We've hit the end
            if self.grid[current.y][current.x][current.dir].char == 'E':
                print(f'Found end at {current.x}, {current.y} after {counter} iterations')
                return current.running_cost

            for neighbour in self.get_neighbours(current):
                if neighbour in seen:
                    continue

                existing_score: int = self.grid[neighbour.y][neighbour.x][neighbour.dir].total_score
                best_total_score: int = min(existing_score, neighbour.total_score)

                # Update the score on the map with the lowest score so far
                self.grid[neighbour.y][neighbour.x][neighbour.dir].total_score = best_total_score
                fringe.put(neighbour)

            seen.add(current)
            counter += 1

        # Shouldn't happen
        return -1

    def part_one(self) -> int:
        """
        Return the ...
        """
        for row in self.grid:
            for col in row:
                print(col[0].char, end='')
            print()
        print()

        start_x, start_y = self.find_xy_position('S')
        score: int = self.pathfind(start_x, start_y)
        return score

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
    solver = Day16()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
