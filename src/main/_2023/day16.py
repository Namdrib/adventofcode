#!/usr/bin/python3
from enum import Enum
from queue import Queue
import sys

class Direction(Enum):
    # The Directions can be mapped to their values to get
    # a useful index for determining change in position, and arrow type
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Beam:
    def __init__(self, x: int, y: int, direction: Direction):
        self.x: int = x
        self.y: int = y
        self.direction: Direction = direction

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

        self.grid = list(self.input.splitlines(keepends=False))

    def calculate_next_directions(self, direction: Direction, tile: str) -> list:
        """
        The behaviour of a beam will depend on what it encounters as it moves:
        - If the beam encounters empty space (.), it continues in the same direction
        - If the beam encounters a mirror (/ or \\), the beam is reflected 90 degrees depending on the angle fo the mirror
        - If the beam encounters the pointy end of a splitter (| or -), the beam passes through the splitter as if the splitter were empty space
        - If the beam encounters the flat side of a splitter (| or -), the beam is split into two beams going in each of the two directions the splitter's pointy ends are pointing

        :param direction: The direction the beam is moving in
        :type direction: Direction
        :param tile: The space it is encountering
        :type tile: str
        :return: The next directions it will move in next (0 or more)
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

    def visualise_grid(self, beams: list):
        """
        Beams are only shown on empty tiles
        Arrows indicate the direction of the beams
        If a tile contains beams moving in multiple directions, the number of distinct directions is shown instead.
        """
        for row, line in enumerate(self.grid):
            for col, char in enumerate(line):
                if char in '|-\\/':
                    print(char, end='')
                elif len(beams[row][col]) > 1:
                    print(len(beams[row][col]), end='')
                elif len(beams[row][col]) == 1:
                    direction_index: int = beams[row][col][0].value
                    arrow: str = self.arrows[direction_index]
                    print(arrow, end='')
                else:
                    print(char, end='')
            print()
        print()

    def propagate(self, starting_beam: Beam) -> list:
        """
        Bounce a beam around the grid, reflecting off mirrors and splitters

        :param starting_beam: The beam to propagate
        :type starting_beam: Beam
        :return: All of the beams that will be produced from this starting beam
        :rtype: list
        """
        # Keep track of which tiles in the grid are energised
        # Each element is a list of Directions
        beams: list = []
        for line in self.grid:
            beams.append([[] for x in line])

        # Using a queue (instead of a recursive stack) prevents the stack from overflowing
        beam_queue: Queue = Queue()
        beam_queue.put(starting_beam)

        while not beam_queue.empty():
            beam: Beam = beam_queue.get()

            # If the beam is out of bounds, it cannot propagate
            if beam.x < 0 or beam.x >= len(self.grid[0]) or beam.y < 0 or beam.y >= len(self.grid):
                continue

            # There is a loop. No point continuing down this path
            if beam.direction in beams[beam.y][beam.x]:
                continue

            # Energise this tile
            beams[beam.y][beam.x].append(beam.direction)

            # See how this beam behaves (where is it going next?)
            current_tile: str = self.grid[beam.y][beam.x]
            next_directions: list = self.calculate_next_directions(beam.direction, current_tile)

            # Create a new beam for each of those directions
            for next_direction in next_directions:
                direction_index: int = next_direction.value
                next_x: int = beam.x + self.dx[direction_index]
                next_y: int = beam.y + self.dy[direction_index]
                next_beam: Beam = Beam(next_x, next_y, next_direction)
                beam_queue.put(next_beam)

        return beams

    def count_energised_tiles(self, beams: list) -> int:
        """
        Return the number of energised tiles, given a beam pattern

        :param beams: Where the beams are pointing, and in which tiles
        :type beams: list
        :return: The number of energised tiles
        :rtype: int
        """
        return sum(sum(1 for tile in row if tile) for row in beams)

    def part_one(self) -> int:
        """
        Find the sum of the hash of every step in the initialisation sequence
        """
        beam_start: Beam = Beam(0, 0, Direction.RIGHT)

        beams: list = self.propagate(beam_start)

        self.visualise_grid(beams)

        return self.count_energised_tiles(beams)


    def part_two(self) -> int:
        """
        Beams may entry from any edge tile, heading away from that edge.
        Find the starting position that energises as many tiles as possible
        Note: takes a while to run
        """
        max_energised_tiles: int = 0
        for i in range(len(self.grid)):
            # Check all starting positions from the left edge
            beam_start: Beam = Beam(0, i, Direction.RIGHT)
            beams: list = self.propagate(beam_start)

            # Count the number of energised tiles, see if it is the max
            num_energised_tiles: int = self.count_energised_tiles(beams)
            max_energised_tiles = max(max_energised_tiles, num_energised_tiles)

            # Check all starting positions from the right edge
            beam_start: Beam = Beam(len(self.grid[i])-1, i, Direction.LEFT)
            beams: list = self.propagate(beam_start)

            # Count the number of energised tiles, see if it is the max
            num_energised_tiles: int = self.count_energised_tiles(beams)
            max_energised_tiles = max(max_energised_tiles, num_energised_tiles)

        for j in range(len(self.grid[0])):
            # Check all starting positions from the top edge
            beam_start: Beam = Beam(j, 0, Direction.DOWN)
            beams: list = self.propagate(beam_start)

            # Count the number of energised tiles, see if it is the max
            num_energised_tiles: int = self.count_energised_tiles(beams)
            max_energised_tiles = max(max_energised_tiles, num_energised_tiles)

            # Check all starting positions from the bottom edge
            beam_start: Beam = Beam(j, len(self.grid)-1, Direction.UP)
            beams: list = self.propagate(beam_start)

            # Count the number of energised tiles, see if it is the max
            num_energised_tiles: int = self.count_energised_tiles(beams)
            max_energised_tiles = max(max_energised_tiles, num_energised_tiles)

        return max_energised_tiles

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
