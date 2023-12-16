#!/usr/bin/python3
from enum import Enum
import sys

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Beam:
    def __init__(self, x: int, y: int, direction: Direction):
        self.x = x
        self.y = y
        self.direction = direction

class Day16:
    """
    Solution for https://adventofcode.com/2023/day/16
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        # A 2D grid of spaces and mirrors
        self.grid: list = []

        # Keep track of which tiles in the grid are energised
        # Each element is a list of Directions
        self.beams: list = []

        # The indices of dx and dy line up with Direction
        self.dx: list = [0, 0, -1, 1]
        self.dy: list = [-1, 1, 0, 0]
        self.arrows: str = '^v<>'

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, the input is single line of comma-separated instructions
        """
        self.input = sys.stdin.read()

        self.grid = [x for x in self.input.splitlines(keepends=False)]
        for line in self.grid:
            self.beams.append([[] for x in line])

        self.visualise_grid()

    def calculate_next_directions(self, direction: Direction, tile: str) -> list:
        """
        The behavour of a beam will depend on what it encounters as it moves:
        - If the beam encounters empty space (.), it continues in the same direction
        - If the beam encounters a mirror (/ or \\), the beam is reflected 90 degrees depending on the angle fo the mirror
        - If the beam encounters the pointy end of a splitter (| or -), the beam passes through the splitter as if the splitter were empty space
        - If the beam encounters the flat side of a splitter (| or -), the beam is split into two beams going in each of the two directions the splitter's pointy ends are pointing

        :param direction: The direction the beam is moving in
        :type direction: Direction
        :param tile: The space it is encountering
        :type tile: str
        :return: The new directions it will move in next (0 or more)
        :rtype: list
        """
        # Continue in the same direction
        if tile == '.':
            return [direction]

        # Get reflected
        if tile == '/':
            if direction == Direction.UP:
                return [direction.RIGHT]
            if direction == Direction.DOWN:
                return [direction.LEFT]
            if direction == Direction.LEFT:
                return [direction.DOWN]
            if direction == Direction.RIGHT:
                return [direction.UP]

        # Get reflected
        if tile == '\\':
            if direction == Direction.UP:
                return [direction.LEFT]
            if direction == Direction.DOWN:
                return [direction.RIGHT]
            if direction == Direction.LEFT:
                return [direction.UP]
            if direction == Direction.RIGHT:
                return [direction.DOWN]

        if tile == '-':
            # Keep going
            if direction in [Direction.LEFT, Direction.RIGHT]:
                return [direction]
            # Get split
            return [Direction.LEFT, Direction.RIGHT]

        if tile == '|':
            # Keep going
            if direction in [Direction.UP, Direction.DOWN]:
                return [direction]
            # Get split
            return [Direction.UP, Direction.DOWN]

        # This should never happen!
        print(f'Unexpected direction, {direction=}, {tile=}')
        return direction

    def visualise_grid(self):
        """
        Beams are only shown on empty tiles
        Arrows indicate the direction of the beams
        If a tile contains beams moving in multiple directions, the number of distinct directions is shown instead.
        """
        for row, line in enumerate(self.grid):
            for col, char in enumerate(line):
                if char in '|-\\/':
                    print(char, end='')
                elif len(self.beams[row][col]) > 1:
                    print(len(self.beams[row][col]), end='')
                elif len(self.beams[row][col]) == 1:
                    direction_index: int = self.beams[row][col][0].value
                    arrow: str = self.arrows[direction_index]
                    print(arrow, end='')
                else:
                    print(char, end='')
            print()
        print()

    def propagate(self, beam: Beam):
        """
        Propagate a beam heading in a direction

        :param beam: The beam to propagate
        :type beam: Beam
        :return: The new beams created by this beam, if any
        :rtype: list
        """
        # If the beam is out of bounds, it cannot propagate
        if beam.x < 0 or beam.x >= len(self.grid[0]) or beam.y < 0 or beam.y >= len(self.grid):
            return

        # There is a loop. No point continuing down this path
        if beam.direction in self.beams[beam.y][beam.x]:
            return

        # Record the beam
        self.beams[beam.y][beam.x].append(beam.direction)

        # Energise this tile
        print(f'Lighting up tile ({beam.x}, {beam.y})')
        self.visualise_grid()

        # See what to do with the current beam
        current_tile: str = self.grid[beam.y][beam.x]
        next_directions: list = self.calculate_next_directions(beam.direction, current_tile)

        for next_direction in next_directions:
            direction_index: int = next_direction.value
            new_x: int = beam.x + self.dx[direction_index]
            new_y: int = beam.y + self.dy[direction_index]
            new_beam: Beam = Beam(new_x, new_y, next_direction)
            self.propagate(new_beam)

    def part_one(self) -> int:
        """
        Find the sum of the hash of every step in the initialisation sequence
        """
        beam_start: Beam = Beam(0, 0, Direction.RIGHT)

        self.propagate(beam_start)

        self.visualise_grid()
        return sum(sum(1 for tile in row if tile) for row in self.beams)

    def part_two(self) -> int:
        """
        """
        return 0

def main() -> None:
    """
    Main
    """
    solver = Day16()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
