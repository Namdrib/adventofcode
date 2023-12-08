#!/usr/bin/python3
import itertools
import math
import sys

class Node:
    def __init__(self, name, left, right):
        self.name = name
        self.left = left
        self.right = right

class Day08:
    """
    Solution for https://adventofcode.com/2023/day/8
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.instructions: str = ''
        self.nodes: dict = {}

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line contains an alphanumeric string
        """
        self.input = sys.stdin.read()

        line_type: str = 'instruction'
        for line in self.input.splitlines(keepends=False):
            if line_type == 'instruction':
                self.instructions = line
                line_type = 'blank'
            elif line_type == 'blank':
                line_type = 'node'
                continue
            else:
                name, options = line.split(' = ')
                options = options.strip('()')
                left, right = options.split(', ')

                self.nodes[name] = (left, right)

    def get_next_node(self, node: str, direction: str) -> str:
        """
        Return the name of the next node if we take the direction `direction` from node `node`

        :param node: The node we're currently on
        :type node: str
        :param direction: The direction to move in
        :type direction: str
        :return: The name of the node in that direction
        :rtype: str
        """
        return self.nodes[node][0] if direction == 'L' else self.nodes[node][1]

    def part_one(self) -> int:
        """
        Find the number of steps required to reach ZZZ, starting from AAA
        """
        current_node: str = 'AAA'
        ending_node: str = 'ZZZ'

        num_steps: int = 0

        # Keep following the instructions until we end up on ending_node
        for direction in itertools.cycle(self.instructions):
            next_node = self.get_next_node(current_node, direction)

            current_node = next_node
            num_steps += 1

            if current_node == ending_node:
                break

        return num_steps

    def part_two(self) -> int:
        """
        There are a number of nodes that start in a node starting with A
        Instead of moving one node at a time, they all simultaneously move in a direction until they are *all* on a node ending with Z at the same time
        Find how many steps it takes before all of the starting nodes are simultaneously on nodes that end with Z
        """
        starting_nodes: list = [x for x in self.nodes if x.endswith('A')]
        # Map how many steps each starting node takes to end on a node ending with Z
        steps_to_z: dict = {}

        num_steps: int = 0

        # For each node
        for node in starting_nodes:
            current_node = node
            # Calculate how long it'll take to get to a spot ending with Z
            # Assumes there is only one spot with Z that corresponds to this node
            num_steps: int = 0
            for direction in itertools.cycle(self.instructions):
                next_node = self.get_next_node(current_node, direction)
                current_node = next_node
                num_steps += 1

                if current_node.endswith('Z'):
                    steps_to_z[current_node] = num_steps
                    break

        # Find the lowest multiple that they will all end up on
        return math.lcm(*steps_to_z.values())


def main() -> None:
    """
    Main
    """
    solver = Day08()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
