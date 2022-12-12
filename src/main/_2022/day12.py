#!/usr/bin/python3
import sys
from queue import PriorityQueue

from Coord import Coord2D

class Day12:
    """
    Solution for https://adventofcode.com/2022/day/12
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self._input: list = None

        self.elevations: list = []

        self.start_coord: Coord2D = None
        self.end_coord: Coord2D = None

        # Coordinate deltas for up, down, left, right
        self.directions: list = [
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0)
        ]

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()

        self._input = raw_input.split('\n')
        self._input = self._input[0:-1]

        # Read the input into a 2D array of numbers
        # Reocrd the start and end positions
        for i, item in enumerate(self._input):
            if 'S' in item:
                self.start_coord = Coord2D(item.find('S'), i)
            if 'E' in item:
                self.end_coord = Coord2D(item.find('E'), i)

            numbers: list = [self.letter_to_height(x) for x in item]
            self.elevations.append(numbers)

    def letter_to_height(self, letter: str) -> int:
        """
        Convert a letter to a height so we can work with numbers
        'a' is 0, through to 'z' is 25
        'S' is equivalent to 'a', 'E' is equivalent to 'z'
        """
        if letter == 'S':
            return 0
        elif letter == 'E':
            return 25
        else:
            return ord(letter) - ord('a')

    def coord_in_bounds(self, query_coord: Coord2D) -> bool:
        """
        Return true if a given Coord is in our grid
        """
        return query_coord.x in range(0, len(self.elevations[0])) and query_coord.y in range(len(self.elevations))

    def get_elevation_at_coords(self, query_coord: Coord2D) -> int:
        """
        Return the elevation at the given Coord
        """
        if self.coord_in_bounds(query_coord):
            return self.elevations[query_coord.y][query_coord.x]
        return 9999 # So it never gets considered in pathfinding

    def pathfind(self, start_coord: Coord2D, end_coord: Coord2D) -> list:
        """
        Return the path from a given coordinate to another
        """
        current_coord: Coord2D = start_coord

        current_elevation: int = self.get_elevation_at_coords(current_coord)
        current_steps: int = 0

        seen: set = set()
        options: PriorityQueue = PriorityQueue()
        options.put((0, current_coord))

        while not options.empty():
            # Get the currently-best option
            current_steps, current_coord = options.get_nowait()
            current_elevation = self.get_elevation_at_coords(current_coord)

            # If we are going to step on the end, return
            if current_coord == end_coord:
                return current_steps

            # Look in each direction
            for direction in self.directions:
                new_coord = Coord2D(current_coord.x + direction[0], current_coord.y + direction[1])

                # Invalid coordinates
                if not self.coord_in_bounds(new_coord):
                    continue

                # We've already processed this coord, we don't want to go back!
                # I feel like this should be new_coord instead, but that doesn't work...
                if current_coord in seen:
                    continue

                # Get the elevation of the new coord
                next_elevation: int = self.get_elevation_at_coords(new_coord)

                # We can go down or up one level
                if next_elevation > current_elevation + 1:
                    continue

                options.put((current_steps+1, new_coord))

            seen.add(current_coord)

        # We didn't find the end...
        return 9999

    def part_one(self) -> int:
        """
        Return the minimum distance from the designated start to end
        """
        return self.pathfind(self.start_coord, self.end_coord)

    def part_two(self) -> int:
        """
        Return the minimum distance from any given lowest point to end
        """
        current_min: int = 999

        # This takes a little bit...
        # The pathfinding could probably be more optimised
        for y, item in enumerate(self.elevations):
            for x, start_elevation in enumerate(item):
                if start_elevation == 0:
                    potential_start_point: Coord2D = Coord2D(x, y)
                    num_steps = self.pathfind(potential_start_point, self.end_coord)
                    current_min = min(current_min, num_steps)

        return current_min

def main() -> None:
    """
    Main
    """
    solver = Day12()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
