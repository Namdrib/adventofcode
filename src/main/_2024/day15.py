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

        reading_grid: bool = True
        for y, item in enumerate(self.input):
            if reading_grid:
                if item.strip() == '':
                    reading_grid = False
                    continue

                self.grid.append(list(item))
                if '@' in item:
                    self.robot_starting_x = item.find('@')
                    self.robot_starting_y = y
            else:
                self.moves.extend(list(item))

        for item in self.grid:
            print(item)
        print(f'Moves: {self.moves}')

    def attempt_move(self, x: int, y: int, move: str, grid: list) -> int:
        direction: dict = list(helpers.get_directions([move]))[0]

        # Where are we looking?
        target_x = x
        target_y = y

        # Did we find somewhere to move (or to push things onto)?
        found_space: bool = False

        # How many things are being moved? (Including the robot)
        length: int = 0

        while True:
            # The next space in the given direction
            target_x = target_x + direction['x']
            target_y = target_y + direction['y']

            thing: str = grid[target_y][target_x]

            # Can't move/push
            if thing == '#':
                print(f'Moving into a wall')
                length = 0
                break

            # There's a box. More things to move
            if thing == 'O':
                print(f'Found a box')
                length += 1

            # Is there an empty space we can move (or push) into?
            if thing == '.':
                print(f'Found empty space at ({target_x}, {target_y})')
                found_space = True
                length += 1
                break

        if found_space:
            # Move everything in this direction until we get to the space
            # Update the grid
            for i in range(length-1, -1, -1):
                dest_y: int = direction['y'] * (i+1)
                dest_x: int = direction['x'] * (i+1)
                src_y: int = direction['y'] * i
                src_x: int = direction['x'] * i
                print(f'Moving {grid[y + src_y][x + src_x]} at ({x + src_x}, {y + src_y}) to ({x + dest_x}, {y + dest_y})')
                grid[y + dest_y][x + dest_x] = grid[y + src_y][x + src_x]

            # The robot has moved off this space
            grid[y][x] = '.'

        # Return the robot's new position
        if found_space:
            return x + direction['x'], y + direction['y']
        return x, y

    def calc_gps_coord(self, x, y) -> int:
        return 100 * y + x

    def part_one(self) -> int:
        """
        Return the ...
        """
        x = self.robot_starting_x
        y = self.robot_starting_y
        grid: list = copy.deepcopy(self.grid)

        for i, move in enumerate(self.moves):
            print(f'Tick {i=}, {move=}')
            x, y = self.attempt_move(x, y, move, grid)

            # for item in grid:
            #     print(''.join(item))
            # print()

        count: int = 0

        for y, row in enumerate(grid):
            for x, item in enumerate(row):
                if item == 'O':
                    count += self.calc_gps_coord(x, y)

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
    solver = Day15()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
