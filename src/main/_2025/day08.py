#!/usr/bin/python3
from functools import reduce
from operator import mul
import os
from queue import PriorityQueue
import sys

# See requirements.txt to get from PyPI
from disjoint_set import DisjointSet

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day08:
    """
    Solution for https://adventofcode.com/2025/day/8
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.points: list = None
        self.circuits: DisjointSet = None
        self.shortest_distances: PriorityQueue = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line is a set of co-ordinates in 3D space (X,Y,Z)
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.points = []
        for item in self.input:
            coords: tuple = tuple(int(x) for x in item.split(','))
            self.points.append(coords)

        # Each junction box starts off on its own circuit
        # As junction boxes are joined together, they merge to become the same
        # circuit - something that disjoint sets handle very well
        # Refer to the index of the box, rather than the box itself
        self.circuits = DisjointSet.from_iterable([i for i in range(len(self.points))])

        self.shortest_distances = self.calculate_shortest_distances()

    def calculate_shortest_distances(self) -> PriorityQueue:
        distances = PriorityQueue()

        # Calculate the straight-line distance for each pair of junction boxes
        # Store the distance and the pair, sorted by distance (shortest first)
        for i in range(len(self.points)):
            for j in range(i+2, len(self.points)):
                dist = helpers.calculate_euclidean_distance(self.points[i], self.points[j])
                distances.put([dist, (i, j)])

        return distances

    def part_one(self) -> int:
        """
        Connecting junction boxes together puts them onto a circuit
        Return the product of the length of the three largest circuits after
        making a number of connections.
        The sample input has 10 connections. The real one has 1000.
        """
        for _ in range(1000):
            # The next pair of boxes with the shortest distance
            distance, boxes = self.shortest_distances.get()

            # Connect these two boxes together
            self.circuits.union(boxes[0], boxes[1])

        # Find the size of the three largest circuits
        # Multiply their lengths together
        longest_circuits: list = sorted(self.circuits.itersets(), reverse=True, key=lambda x: len(x))
        count: int = reduce(mul, [len(x) for x in longest_circuits[0:3]], 1)
        return count

    def part_two(self) -> int:
        """
        Keep connecting junction boxes until they all form one circuit
        Return the product of the two X co-ordinates of the last two junction
        boxes that are joined together
        """
        count: int = 0

        # Note: This is NOT independent from part 1 - it continues building the
        # same circuit, from the same shortest_distances
        # Continue adding junction boxes to the circuits until there is only one
        # left that isn't part of the circuit
        while not self.shortest_distances.empty():
            distance, boxes = self.shortest_distances.get()
            self.circuits.union(boxes[0], boxes[1])

            # We have just merged into one big circuit!
            # Multiply the two X co-ordinates of the connection that joined the
            # last box to the circuit - this is the final result
            if len(list(self.circuits.itersets())) == 1:
                count = self.points[boxes[0]][0] * self.points[boxes[1]][0]
                break

        return count

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
