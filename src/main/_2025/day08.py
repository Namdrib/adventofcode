#!/usr/bin/python3
import os
from queue import PriorityQueue
import sys
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
        self.circuits: set = None

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
        # Refer to the index of the box, rather than the box itself
        self.circuits = []
        for i in range(len(self.points)):
            self.circuits.append(set([i]))

    def calculate_shortest_distances(self) -> PriorityQueue:
        distances = PriorityQueue()

        # Calculate the straight-line distance for each pair of junction boxes
        # Store the distance and the pair, sorted by distance (shortest first)
        for i in range(len(self.points)):
            for j in range(i+2, len(self.points)):
                dist = helpers.calculate_euclidean_distance(self.points[i], self.points[j])
                distances.put([dist, (i, j)])

        return distances

    def prune(self) -> None:
        for c1 in self.circuits:
            for c2 in self.circuits:
                if not c1.isdisjoint(c2):
                    c1.update(c2)

        new: list = []
        for c in self.circuits:
            if c not in new:
                new.append(c)
        self.circuits = new

    def part_one(self) -> int:
        """
        Connecting junction boxes together puts them onto a circuit
        Return the product of the length of the three largest circuits after
        making the connections
        Note: The sample input has 10 connections. The real one has 1000
        """
        count: int = 0

        shortest_distances = self.calculate_shortest_distances()

        # A list of circuits
        # Each circuit is a set of junction boxes that are connected
        # self.circuits = []

        for _ in range(10):
            # The next pair of boxes with the shortest distance
            distance, boxes = shortest_distances.get()
            # print(f"Next closest: {self.points[boxes[0]]} and {self.points[boxes[1]]}, {distance=}")

            # See if it would intersect any existing circuits
            for circuit in self.circuits:
                if circuit.intersection(boxes):
                    # print(f"Intersection between {circuit} and {boxes}")
                    circuit.add(boxes[0])
                    circuit.add(boxes[1])
            # else:
            #     new_circuit: set = set(boxes)
            #     self.circuits.append(new_circuit)

            # Prune duplicate circuits
            self.prune()

            # for circuit in self.circuits:
            #     for box in circuit:
            #         print(self.points[box])
            #     print()

        # Find the size of the three largest circuits
        # Multiply their lengths together
        longest_circuits: list = sorted(self.circuits, reverse=True, key=lambda x: len(x))
        return len(longest_circuits[0]) * len(longest_circuits[1]) * len(longest_circuits[2])
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
    solver = Day08()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
