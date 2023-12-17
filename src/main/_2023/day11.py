#!/usr/bin/python3
import sys

class Galaxy:
    def __init__(self, id_: int, x: int, y: int):
        self.id = id_
        self.x = x
        self.y = y

class Day11:
    """
    Solution for https://adventofcode.com/2023/day/11
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.grid: list = []

        self.galaxies: list = []

        self.empty_rows: list = []
        self.empty_cols: list = []

        self.shortest_paths: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, the input is a 2D image with empty space (.) and galaxies (#)
        """
        self.input = sys.stdin.read()

        # Keep the original image layout
        # The extra distance of expansion is accounted for when calculating distance between galaxies
        self.grid = self.input.splitlines(keepends=False)

        galaxy_id: int = 1
        for row, line in enumerate(self.grid):
            # Determine which rows are empty
            if '#' not in line:
                self.empty_rows.append(row)

            # Number and store all of the galaxies
            for col, char in enumerate(line):
                if char == '#':
                    galaxy = Galaxy(galaxy_id, col, row)
                    self.galaxies.append(galaxy)
                    galaxy_id += 1

        # Determine which cols are empty
        for col in range(len(self.grid[0])):
            if '#' not in [self.grid[row][col] for row in range(len(self.grid))]:
                self.empty_cols.append(col)

        # Initialise the shortest paths
        for _ in range(galaxy_id):
            row: list = []
            for _ in range(galaxy_id):
                row.append(0)
            self.shortest_paths.append(row)

    def calculate_shortest_paths(self, galaxy_multiple: int) -> None:
        """
        Calculate the shortest path between every galaxy and every other galaxy
        The reuslts are stored into self.shortest_paths
        Some space has expanded since the image was captured
        All empty rows and columns are actually `galaxy_multiple` times as big as they are in the image

        :param galaxy_multiple: How many times larger empty rows/columns are
        :type galaxy_multiple: int
        """

        # Look from each galaxy to each other galaxy
        # Only count unqiue combinations of galaxies
        # i.e. if we have the length from 1 to 2, don't both with 2 to 1
        for i, source_galaxy in enumerate(self.galaxies):
            for column in range(i+1, len(self.galaxies)):
                dest_galaxy = self.galaxies[column]
                # Find the number of steps between source_galaxy and self.galaxies[j]
                # This is the manhattan distance between the two galaxies
                # Record it into self.shortest_paths[i][j] and self.shortest_paths[j][i]
                x_diff: int = abs(source_galaxy.x - dest_galaxy.x)
                y_diff: int = abs(source_galaxy.y - dest_galaxy.y)

                min_x = min(source_galaxy.x, dest_galaxy.x)
                min_y = min(source_galaxy.y, dest_galaxy.y)
                max_x = max(source_galaxy.x, dest_galaxy.x)
                max_y = max(source_galaxy.y, dest_galaxy.y)

                # Account for expanded space
                # Each empty space has already been counted as 1 distance
                # So multiple each one that we passed through by galaxy_multiple-1
                empty_space: int = len([1 for col in range(min_x, max_x) if col in self.empty_cols])
                x_diff += empty_space * (galaxy_multiple - 1)
                empty_space = len([1 for row in range(min_y, max_y) if row in self.empty_rows])
                y_diff += empty_space * (galaxy_multiple - 1)

                # Store the distance
                distance: int = x_diff + y_diff
                self.shortest_paths[i][column] = distance

    def add_all_shortest_paths(self) -> int:
        """
        Add up all of the shortest paths between all of the galaxies
        Do not count the same path twice

        :return: The sum of path lengths between all galaxies
        :rtype: int
        """
        sum_lengths: int = 0
        for i in range(len(self.shortest_paths)):
            for j in range(i+1, len(self.shortest_paths[i])):
                sum_lengths += self.shortest_paths[i][j]
        return sum_lengths


    def part_one(self) -> int:
        """
        Find the sum of the shortest paths between all galaxies, assuming every column and row with an empty space is twice as big a it is
        """
        self.calculate_shortest_paths(2)
        return self.add_all_shortest_paths()

    def part_two(self) -> int:
        """
        Find the sum of the shortest paths between all galaxies, assuming every column and row with an empty space is 1,000,000 times as big as it is
        """
        self.calculate_shortest_paths(1_000_000)
        return self.add_all_shortest_paths()

def main() -> None:
    """
    Main
    """
    solver = Day11()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
