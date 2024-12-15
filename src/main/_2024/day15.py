#!/usr/bin/python3
import copy
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day15:
    """
    Solution for https://adventofcode.com/2024/day/15
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.grid: list = None

        self.moves: list = None

        self.robot_starting_x: int = 0
        self.robot_starting_y: int = 0

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.grid: list = []
        self.moves: list = []

        # Whether we're reading the grid or the moves
        is_reading_grid: bool = True

        for y, item in enumerate(self.input):
            if is_reading_grid:
                if item.strip() == '':
                    is_reading_grid = False
                    continue

                self.grid.append(list(item))
                if '@' in item:
                    self.robot_starting_x = item.find('@')
                    self.robot_starting_y = y
            else:
                self.moves.extend(list(item))

    def find_robot(self, grid: list) -> tuple:
        for y, row in enumerate(grid):
            for x, item in enumerate(row):
                if item == '@':
                    return (x, y)

        # Shouldn't happen
        return (0, 0)

    def atomic_move(self, src_x: int, src_y: int, dest_x: int, dest_y: int, grid: list) -> None:
        """
        Helper method to move something from the source to the destination

        :param src_x: The x co-ordinate of the thing to move
        :type src_x: int
        :param src_y: The y co-ordinate of the thing to move
        :type src_y: int
        :param dest_x: The x co-ordinate of where to move it to
        :type dest_x: int
        :param dest_y: The y co-ordinate of where to move it to
        :type dest_y: int
        :param grid: The grid on which to move them. It is modified in-place
        :type grid: list
        """
        # print(f'Moving {grid[src_y][src_x]} from ({src_x}, {src_y}) to ({dest_x}, {dest_y})')
        grid[dest_y][dest_x] = grid[src_y][src_x]
        grid[src_y][src_x] = '.'

    def can_move(self, x: int, y: int, move: str, grid: list) -> bool:
        """
        Recursively determine whether the item at (x, y) can move in move direction
        Big boxes can only be moved vertically if the whole box can be moved

        :param x: The x co-ordinate of the item to move
        :type x: int
        :param y: The y co-ordinate of the item to move
        :type y: int
        :param move: The direction in which to move, one of <>^v
        :type move: str
        :param grid: The grid to check
        :type grid: list
        :return: True if the item cam be moved, False otherwise. Takes into account big boxes
        :rtype: bool
        """
        direction: dict = list(helpers.get_directions([move]))[0]

        # The next space in the given direction
        target_x = x + direction['x']
        target_y = y + direction['y']

        next_item: str = grid[target_y][target_x]

        # Base case: Can't move
        if next_item == '#':
            return False

        # Base case: Can move
        if next_item == '.':
            return True

        # Special case: Vertical movement for large boxes
        # We can only move if the other half can move
        if next_item in '[]' and direction['y']:
            x_modifier = 1 if next_item == '[' else -1
            return self.can_move(target_x, target_y, move, grid) and self.can_move(target_x + x_modifier, target_y, move, grid)

        # Small boxes and large boxes moving horizontally exhibit the same
        # behaviour
        return self.can_move(target_x, target_y, move, grid)

    def attempt_move(self, x: int, y: int, move: str, grid: list) -> tuple:
        """
        Move the item given at (x, y) in the direction specified by move.
        Large boxes may only be moved vertically if both sides can be moved.

        :param x: The x co-ordinate of the item to move
        :type x: int
        :param y: The y co-ordinate of the item to move
        :type y: int
        :param move: The direction in which to move, one of <>^v
        :type move: str
        :param grid: The grid to check
        :type grid: list
        :return: The new (x, y) position of the robot
        :rtype: tuple
        """
        direction: dict = list(helpers.get_directions([move]))[0]

        # The next space in the given direction
        target_x = x + direction['x']
        target_y = y + direction['y']

        next_item: str = grid[target_y][target_x]

        # Base case: Can't move, don't do anything
        if not self.can_move(x, y, move, grid):
            return (x, y)

        # Base case: There's a free spot - go in
        if next_item == '.':
            self.atomic_move(x, y, target_x, target_y, grid)
            return (target_x, target_y)

        # Special case: Vertical movement for large boxes
        # Move both halves together
        if next_item in '[]' and direction['y']:
            x_modifier = 1 if next_item == '[' else -1

            # We already know both halves can move because of the can_move check
            # So move both pieces, then move us into place
            self.attempt_move(target_x, target_y, move, grid)
            self.attempt_move(target_x + x_modifier, target_y, move, grid)
            self.atomic_move(x, y, target_x, target_y, grid)
            return (target_x, target_y)

        # General case: Everything else
        # The next thing can be moved, so move it, then move us into place
        self.attempt_move(target_x, target_y, move, grid)
        self.atomic_move(x, y, target_x, target_y, grid)
        return (target_x, target_y)

    def calc_gps_coord(self, x, y) -> int:
        return 100 * y + x

    def enlarge_map(self) -> tuple:
        """
        Make everything twice as large, except for the robot

        :return: _description_
        :rtype: tuple
        """
        grid: list = []

        robot_x: int = 0
        robot_y: int = 0

        for y, row in enumerate(self.grid):
            new_row: list = []
            for x, item in enumerate(row):
                if item in '#.':
                    # Walls and empty space are simply twice as big
                    new_row.extend([item, item])
                elif item == 'O':
                    # Small boxes turn into large boxes with two parts
                    new_row.extend(['[', ']'])
                elif item == '@':
                    # The robot occupies the left side after enlargement
                    new_row.extend(['@', '.'])
                    robot_y = y
                    robot_x = x * 2
            grid.append(new_row)

        return (grid, robot_x, robot_y)

    def part_one(self) -> int:
        """
        Move the robot, pushing boxes around
        Return the sum of the GPS co-ordinate score of the boxes
        """
        x = self.robot_starting_x
        y = self.robot_starting_y
        grid: list = copy.deepcopy(self.grid)

        for i, move in enumerate(self.moves):
            x, y = self.attempt_move(x, y, move, grid)

        count: int = 0

        for y, row in enumerate(grid):
            for x, item in enumerate(row):
                if item == 'O':
                    count += self.calc_gps_coord(x, y)

        return count

    def part_two(self) -> int:
        """
        Enlarge the map by making everything twice as large, except for the robot
        Move the robot, pushing boxes around
        Return the sum of the GPS co-ordinate score of the boxes, using the left
        side of the large boxes
        """
        grid, x, y = self.enlarge_map()

        for i, move in enumerate(self.moves):
            x, y = self.attempt_move(x, y, move, grid)

        count: int = 0

        for y, row in enumerate(grid):
            for x, item in enumerate(row):
                # Only count the left side of the boxes
                if item == '[':
                    count += self.calc_gps_coord(x, y)

        return count

def main() -> None:
    """
    Main
    """
    solver = Day15()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
