#!/usr/bin/python3
import sys

class Day13:
    """
    Solution for https://adventofcode.com/2023/day/13
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.grids: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, the input is a list of 2D grids, with each grid separated by an empty lien
        """
        self.input = sys.stdin.read()

        grid: list = []
        for line in self.input.splitlines(keepends=False):
            if line:
                grid.append(line)
            else:
                # Empty line, we've reached the end of a grid
                self.grids.append(grid)
                grid = []

        # Capture the last grid. Assumes the input ends with a newline, and not a new line
        self.grids.append(grid)

    def is_mirror_row(self, grid: list, row: int) -> bool:
        """
        Check whether the given grid has a mirror between row `row` and `row+1`

        :param grid: The grid to check
        :type grid: list
        :param row: The row to check for
        :type row: int
        :return: True if there is a mirror, False otherwise
        :rtype: bool
        """
        # Keep comparing rows, moving further away from the given row until either:
        # - we go out of bounds, or
        # - there is a mismatch
        for dy in range(len(grid)):
            row_number_above = row - dy
            row_number_below = row + dy + 1
            print(f'Comparing row {row_number_above+1}, {row_number_below+1}')

            if row_number_above < 0:
                break
            if row_number_below >= len(grid):
                break

            print(f'  {grid[row_number_above]}')
            print(f'  {grid[row_number_below]}')
            if grid[row_number_above] != grid[row_number_below]:
                print(f'Asymmetry detected at row {row+1}/{row+2}')
                return False

        print(f'-----> Mirror at row {row+1}')
        return True


    def is_mirror_column(self, grid: list, column: int) -> bool:
        """
        Check whether the given grid has a mirror between column `column` and `column+1`

        :param grid: The grid to check
        :type grid: list
        :param column: The column to check for
        :type column: int
        :return: True if there is a mirror, False otherwise
        :rtype: bool
        """

        # Keep comparing columns, moving further away from the given column until either:
        # - we go out of bounds, or
        # - there is a mismatch
        for dx in range(len(grid[0])):
            column_number_left = column - dx
            column_number_right = column + dx + 1

            print(f'Comparing col {column_number_left+1}, {column_number_right+1}')

            if column_number_left < 0:
                break
            if column_number_right >= len(grid[0]):
                break

            column_left: list = [row[column_number_left] for row in grid]
            column_right: list = [row[column_number_right] for row in grid]

            if column_left != column_right:
                print(f'Asymmetry detected at column {column_number_left+1}/{column_number_right+1}')
                return False

        print(f'-----> Mirror at column {column+1}')
        return True

    def get_mirror_row_in_grid(self, grid: list) -> int:
        """
        Return the row where there is a mirror. Return -1 if there is no mirror

        :param grid: The grid to check for a mirror
        :type grid: list
        :return: The row where there is a mirror, if there is one
        :rtype: int
        """
        for row in range(0, len(grid)-1):
            if self.is_mirror_row(grid, row):
                return row+1

        return -1

    def get_mirror_column_in_grid(self, grid: list) -> int:
        """
        Return the column where there is a mirror. Return -1 if there is no mirror

        :param grid: The grid to check for a mirror
        :type grid: list
        :return: The column where there is a mirror, if there is one
        :rtype: int
        """
        for column in range(0, len(grid[0])-1):
            if self.is_mirror_column(grid, column):
                return column+1

        return -1

    def part_one(self) -> int:
        """
        Add up the number of columns to the left of each vertical line of reflection;
        to that, also add 100 multiplied by the number of rows above each horizontal line of reflection
        """

        total: int = 0
        for grid in self.grids:

            nums: str = ''.join(str(x+1) for x in range(len(grid[0])))
            print(f'   {nums}')
            for i, line in enumerate(grid):
                print(f'{i+1}: {line}')
            print()

            mirror_row: int = self.get_mirror_row_in_grid(grid)
            print()
            if mirror_row == -1:
                mirror_column: int = self.get_mirror_column_in_grid(grid)
                print()
                total += mirror_column
            else:
                total += (100* mirror_row)

        return total

    def part_two(self) -> int:
        """
        Find how many tiles are enclosed by the loop
        """
        return 0

def main() -> None:
    """
    Main
    """
    solver = Day13()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
