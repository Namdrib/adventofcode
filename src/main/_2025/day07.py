#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Node:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.left = None
        self.right = None

    def __str__(self) -> str:
        self_str: str = f"({self.x}, {self.y})"
        left_str: str = f"({self.left.x}, {self.left.y})" if self.left else 'None'
        right_str: str = f"({self.right.x}, {self.right.y})" if self.right else 'None'
        return f"{self_str} -> {left_str} and {right_str}"

class Day07:
    """
    Solution for https://adventofcode.com/2025/day/7
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.grid: list = None

        self.start_x: int = None
        self.start_y: int = None

        self.root: Node = None
        self.nodes: dict = dict()

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        # Load the grid
        self.grid = []
        for item in self.input:
            self.grid.append([x for x in item])

        # Locate the start
        found_start: bool = False
        for y, row in enumerate(self.grid):
            if found_start:
                break
            for x, cell in enumerate(row):
                if cell == 'S':
                    self.start_x = x
                    self.start_y = y
                    found_start = True
                    break

        # Create a tree data structure from the inputs
        self.create_tree(self.start_x, self.start_y)

    def create_tree(self, x: int, y: int) -> None:
        """
        Create a tree from the input graph

        Stores the root in self

        :param x: Starting x position to create the tree from
        :type x: int
        :param y: Starting y position to create the tree from
        :type y: int
        """
        # Find the first node by moving down from the start to the first
        # splitter
        new_y: int = y
        while self.input[new_y][x] != '^':
            new_y += 1

        # This is where the root of the tree is
        self.root = Node(x, new_y)
        self._create_tree(x, new_y, self.root, None)

    def _create_tree(self, x: int, y: int, parent: Node, left: bool) -> None:
        """
        Recursive helper method to create the tree

        Essentially simulates the path of the beam as it goes down the input grid

        :param x: The x position of the space in the input grid
        :type x: int
        :param y: The y position of the space in the input grid
        :type y: int
        :param parent: The parent node we descended from, to set its child
        :type parent: Node
        :param left: True if this call was descended to the left, False otherwise
        :type left: bool
        :return: Nothing
        :rtype: None
        """
        # There are no more nodes beyond the end of the grid
        if y >= len(self.grid):
            return

        # If the current cell is empty, move down
        if self.grid[y][x] in 'S.|':
            self._create_tree(x, y+1, parent, left)
            return

        # If the current cell is a splitter, create a new node, and set the
        # parent's child to the new node
        # We need to know whether we are the left or right child
        if self.grid[y][x] == '^':

            # Check whether this node has been seen before
            seen: bool = False
            if (x, y) in self.nodes.keys():
                seen = True

            # Create a new node for the current position
            current = Node(x, y)
            # If this is the first node we've seen, set the root node
            if len(self.nodes) == 0:
                self.root = current
            self.nodes[(x, y)] = current

            # Set the parent's child
            if left:
                parent.left = current
            else:
                parent.right = current

            # There is no need to go re-traverse nodes we've visited
            # Their children have already been recorded
            # If we do this too early, some nodes might not get their children
            # set properly
            if seen:
                return

            # Walk to the left and right
            self._create_tree(x-1, y, current, True)
            self._create_tree(x+1, y, current, False)

    def count_nodes(self) -> int:
        """
        Return the number of nodes in the tree

        :return: The number of nodes in the tree
        :rtype: int
        """
        # Who needs to recursively walk the tree when we already have all the
        # nodes ;)
        return len(self.nodes)

    def count_paths(self, current: Node) -> int:
        """
        Count the number of ways the current node can reach its leaves

        :param current: The node to search from
        :type current: Node
        :return: The number of paths from the current node to the leaves
        :rtype: int
        """
        memo: dict = {}
        num_timelines: int = self._count_paths(current, memo)
        return num_timelines

    def _count_paths(self, current: Node, memo: dict) -> int:
        """
        Recursive helper method to traverse the tree

        Uses memoisation to store the number of paths from any given node to its
        leaves

        :param current: The current node to traverse from
        :type current: Node
        :param memo: A dictionary of {(x, y): num_paths}
        :type memo: dict
        :return: the number of paths from the current node to the leaves
        :rtype: int
        """
        pos: tuple = (current.x, current.y)

        # Memoise the number of pathways from any given node to the end
        if pos in memo:
            return memo[pos]

        # The else covers the recursive base case - there is no child on that side
        left_timelines: int = self._count_paths(current.left, memo) if current.left else 1
        right_timelines: int = self._count_paths(current.right, memo) if current.right else 1

        num_timelines: int = left_timelines + right_timelines

        # Store the number of timelines for the current node
        memo[pos] = num_timelines
        return memo[pos]

    def part_one(self) -> int:
        """
        Return the number of times the beam is split
        """
        count: int = 0

        count = self.count_nodes()

        return count

    def part_two(self) -> int:
        """
        Return the number of paths from the root node to the leaves
        """
        count: int = 0

        count = self.count_paths(self.root)

        return count

def main() -> None:
    """
    Main
    """
    solver = Day07()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
