#!/usr/bin/python3
import copy
import re
import sys
import typing

class Day22:
    """
    Solution for https://adventofcode.com/2022/day/22
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.grid: list = []
        self.instructions: str = ''
        self.path: list = []

        # Translate a facing to somethign more meaningful
        # (x, y)
        self.facing_dirs: list = [
            (1, 0), (0, 1), (-1, 0), (0, -1)
        ]
        self.facing_chars: list = ['>', 'v', '<', '^']
        self.facing_words: list = ['right', 'down', 'left', 'up']

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()


        reading_grid: bool = True
        for item in self.input:
            if reading_grid:
                if not item:
                    reading_grid = False
                    continue

                self.grid.append(list(item))

            else:
                if item:
                    self.instructions = item

        for item in self.grid:
            print(item)
        print(f'Instructions: {self.instructions}')

    def get_next_position(self, x, y, facing) -> typing.Tuple:
        """
        Return the next position if we were to move forwards one step.
        This includes walls. This way we can break from calling this in a loop if the position is a wall
        The coordinates being returned should always be valid (i.e. on the grid)
        """
        dx, dy = self.facing_dirs[facing]
        next_x = x + dx
        next_y = y + dy

        # print(f'Potentially moving to {next_x},{next_y}')

        # Moving down
        if dy > 0:
            # Check for overflow
            # Too far, wrap around if we...
            # move down past the grid or
            # move into an x that doesn't exist
            if next_y >= len(self.grid) \
                    or next_x >= len(self.grid[next_y]) \
                    or self.grid[next_y][next_x] == ' ':
                # Find the first open space or wall from the top
                for i, row in enumerate(self.grid):
                    if next_x >= len(row):
                        continue
                    if row[next_x] == ' ':
                        continue
                    if row[next_x] in '.#':
                        next_y = i
                        break

        # Moving up
        if dy < 0:
            # Too far, wrap around
            if next_y < 0 \
                    or next_x >= len(self.grid[next_y]) \
                    or self.grid[next_y][next_x] == ' ':
                # Find first the open space or wall from the bottom
                for i in range(len(self.grid)-1, -1, -1):
                    if next_x >= len(self.grid[i]):
                        continue
                    if self.grid[i][next_x] == ' ':
                        continue
                    if self.grid[i][next_x] in '.#':
                        next_y = i
                        break

        # Moving right
        if dx > 0:
            # Too far, wrap around
            if next_x >= len(self.grid[next_y]) or self.grid[next_y][next_x] == ' ':
                # Find the first open space or wall from the left
                next_open = self.grid[next_y].index('.')
                if '#' in self.grid[next_y]:
                    next_wall = self.grid[next_y].index('#')
                    if next_open < next_wall:
                        next_x = next_open
                    else:
                        next_x = next_open
                else:
                    next_x = next_open

        # Moving left
        if dx < 0:
            # Too far, wrap around
            if next_x < 0 or self.grid[next_y][next_x] == ' ':
                # Find the first open space or wall from the right
                next_open = ''.join(self.grid[next_y]).rindex('.')
                if '#' in self.grid[next_y]:
                    next_wall = ''.join(self.grid[next_y]).rindex('#')
                    if next_open > next_wall:
                        next_x = next_open
                    else:
                        next_x = next_wall
                else:
                    next_x = next_open

        # print(f'Moving to {next_x}, {next_y}')
        return next_x, next_y

    def do_instruction(self, x, y, facing, instruction) -> typing.Tuple:
        """
        If instruction is numeric, move forward that many steps
        If we go off the rgid, wrap around. If we hit a wall, stop
        If it is R or L, rotate clockwise or counterclockwise, respectively
        """
        # print(f'Instruction: {instruction}. Starting at ({x},{y}), facing {self.facing_words[facing]}')
        if instruction.isnumeric():
            num_steps: int = int(instruction)

            # print(f'Moving {num_steps} steps {dx},{dy}')
            # Move forward dx (or dy) steps
            for _ in range(num_steps):
                # By this point, we have established a safe next_y and next_x
                next_x, next_y = self.get_next_position(x, y, facing)

                if self.grid[next_y][next_x] == '#':
                    # Next spot is a wall. Stop
                    break

                # Make the move
                x = next_x
                y = next_y
                self.path.append((x, y, facing))

            # print(f'New position: {x},{y}')
        else:
            # Rotate 90 edgrees left or right
            if instruction == 'L':
                facing -= 1
                if facing < 0:
                    facing += 4
            else:
                facing += 1
                facing %= 4

        self.path.append((x, y, facing))
        return (x, y, facing)

    def follow_instructions(self) -> typing.Tuple:
        """
        Startign at the left-most tile on the top row, follow the instructions
        Return the (x, y, facing) after following the last instruction
        """
        # Starting state: leftmost open time of the top row of tiles
        x: int = self.grid[0].index('.')
        y: int = 0
        facing: int = 0

        print(f'Starting at ({x},{y}), facing {facing}')

        steps: list = []
        m: list = re.findall(r'(\d+)', self.instructions)
        t: list = re.findall(r'[LR]', self.instructions)
        steps: list = [x for combined in zip(m, t) for x in  combined]
        steps.append(m[-1])

        self.path = [(x, y, facing)]
        for step in steps:
            x, y, facing = self.do_instruction(x, y, facing, step)
            self.path.append((x, y, facing))

            # self.draw_path()

        return x, y, facing

    def draw_path(self) -> None:
        """
        Print the original grid with our path overlaid on top
        """
        grid_copy: list = copy.deepcopy(self.grid)
        for x, y, facing in self.path:
            grid_copy[y][x] = self.facing_chars[facing]

        for row in grid_copy:
            print(''.join(row))

    def calculate_final_password(self, x, y, facing) -> int:
        """
        The final password is the sum of 1000 times the row, 4 times the column, and the facing
        """
        return 1000 * (y+1) + 4 * (x+1) + facing

    def part_one(self) -> int:
        """
        Return the final password after following the isntructions on the map
        """
        x, y, facing = self.follow_instructions()
        self.draw_path()
        result: int = self.calculate_final_password(x, y, facing)
        return result

    def part_two(self) -> int:
        """
        Return the final password after following the isntructions on the map
        This time, treat the map as a cube that wraps on itself
        Going off the edge on one face gives a new rotation and new face
        """
        result: int = 0
        return result

def main() -> None:
    """
    Main
    """
    solver = Day22()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
