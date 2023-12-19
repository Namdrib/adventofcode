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

        # These are used to capture how many differences there are in each grid's rows and columns
        # Each element in the outer list represents a grid's rows/columns
        # Each element in the inner list represents how many differences there are in that grid's rows/columns
        # e.g. row_diffs[0] are the row differences for grids[0]
        self.row_diffs: list = []
        self.col_diffs: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, the input is a list of 2D grids, with each grid separated by an empty line
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

        # Set the size of each row_diffs and col_diffs entry to the the corresponding grid's size
        for grid in self.grids:
            self.row_diffs.append([-1 for x in grid])
            self.col_diffs.append([-1 for x in grid[0]])

    def scan_rows_for_diffs(self, grid_index: int, row: int) -> None:
        """
        Treat rows `row` and `row+1` as an axis of reflection
        Record how many differences there are between the sides of the reflection

        :param grid_index: The index of the grid to search for reflections
        :type grid_index: int
        :param row: The row to check for
        :type row: int
        """
        # Keep comparing rows, moving further away from the given row until either:
        # - we go out of bounds, or
        # - there is a mismatch
        grid: list = self.grids[grid_index]
        num_differences: int = 0
        for dy in range(len(grid)):
            row_number_above = row - dy
            row_number_below = row + dy + 1

            if row_number_above < 0:
                break
            if row_number_below >= len(grid):
                break

            # Find the hamming distance between the rows being compared
            num_differences += sum(c1 != c2 for c1, c2 in zip(grid[row_number_above], grid[row_number_below]))

        self.row_diffs[grid_index][row] = num_differences

    def scan_cols_for_diffs(self, grid_index: int, column: int) -> None:
        """
        Treat columns `col` and `col+1` as an axis of reflection
        Record how many differences there are between the sides of the reflection

        :param grid_index: The index of the grid to search for mirrors
        :type grid_index: int
        :param column: The column to check for
        :type column: int
        """
        # TODO: Would be nice to consolidate the logic of this and scan_rows_for_diffs
        # as they are pretty much the same code. Maybe work on a rotated grid?

        # Keep comparing columns, moving further away from the given column until either:
        # - we go out of bounds, or
        # - there is a mismatch
        num_differences: int = 0
        grid: list = self.grids[grid_index]
        for dx in range(len(grid[0])):
            column_number_left = column - dx
            column_number_right = column + dx + 1

            if column_number_left < 0:
                break
            if column_number_right >= len(grid[0]):
                break

            column_left: list = [row[column_number_left] for row in grid]
            column_right: list = [row[column_number_right] for row in grid]

            # Find the hamming distance between the columns being compared
            num_differences += sum(c1 != c2 for c1, c2 in zip(column_left, column_right))

        self.col_diffs[grid_index][column] = num_differences

    def get_mirror_position(self, grid_index: int, check_smudge: bool) -> tuple:
        """
        Find where the mirror is located for a given grid

        :param grid_index: The index of the grid to search for mirrors
        :type grid: list
        :param check_smudge: Whether to check for smudges when determining the reflection location
        :type check_smudge: bool
        :return: The (mirror_row, mirror_column) in the grid. One of them will be -1, signifying no mirror for that axis
        :rtype: tuple
        """
        # Normally, the point of reflection will be the row/column where there are no differences
        # along the axis of reflection
        # With the smudge, there will be exactly one difference
        try:
            mirror_row = self.row_diffs[grid_index].index(1 if check_smudge else 0) + 1
        except ValueError:
            mirror_row = -1

        try:
            mirror_column = self.col_diffs[grid_index].index(1 if check_smudge else 0) + 1
        except ValueError:
            mirror_column = -1

        return (mirror_row, mirror_column)

    def part_one(self) -> int:
        """
        Summarise a reflection line by doing the following:
        - Add up the number of columns to the left of each vertical line of reflection;
        to that, also add 100 multiplied by the number of rows above each horizontal line of reflection
        Find the sum of all summarised reflection lines
        """
        # This pre-processing will be used for both part_one and part_two
        for grid_index, grid in enumerate(self.grids):
            # Assess how many differences each potential axis of reflection has
            for row in range(0, len(grid)-1):
                self.scan_rows_for_diffs(grid_index, row)
            for col in range(0, len(grid[0])-1):
                self.scan_cols_for_diffs(grid_index, col)

        total: int = 0
        for grid_index, _ in enumerate(self.grids):
            # The original mirror position will have the axis of reflection where there are *no* differences
            mirror_row, mirror_column = self.get_mirror_position(grid_index, False)
            if mirror_row != -1:
                total += (100 * mirror_row)
            elif mirror_column != -1:
                total += mirror_column

        return total

    def part_two(self) -> int:
        """
        There is a smudge in the mirror. One pixel (either a '.' or a '#') should be flipped.
        This results in a new reflection line in each grid
        Find the sum of all summarised reflection lines
        """
        total: int = 0
        for grid_index, _ in enumerate(self.grids):
            # The smudged mirror position will have the axis of reflection where there is *one* difference
            mirror_row, mirror_column = self.get_mirror_position(grid_index, True)
            if mirror_row != -1:
                total += (100 * mirror_row)
            elif mirror_column != -1:
                total += mirror_column

        return total

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
