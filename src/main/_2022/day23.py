#!/usr/bin/python3
import math
import sys

class Day23:
    """
    Solution for https://adventofcode.com/2022/day/23
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self._input: list = None

        # Represents a 2D grid of Elves and their positions
        self._elf_positions: list = []

        self._dx: list = [0, 0, -1, 1]
        self._dy: list = [-1, 1, 0, 0]

        # The first direction the Elves will consider when moving
        self._starting_dir: int = 0

        self._border_size: int = 1000

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line contains a grid of empty space (.) or an Elf (#)
        are separated by an empty line
        Each group contains the items carried by a single elf
        """
        _input = sys.stdin.read()

        input_height: int = len(_input.split('\n'))
        input_width: int = len(_input.split('\n')[0])

        # Initialise the Elf grid
        # There will be 10 rounds
        # So at most, a single Elf can move 10 steps away from their starting position
        # Initialise the grid to be the size of the input + 10 in every direction
        for y in range(input_height + (self._border_size * 2)):
            self._elf_positions.append(['.' for i in range(input_width + (self._border_size * 2))])

        # Represents the inventory of a single elf
        for y, line in enumerate(_input.split('\n')):
            line = line.strip()

            for x, char in enumerate(line):
                if char == '#':
                    # Set the elf's position
                    # Offset it by 10 in each direction
                    self._elf_positions[y+self._border_size][x+self._border_size] = '#'

    def calculate_bounding_rectangle(self) -> int:
        """
        Calculate the smallest rectangle that covers all of the elves
        Return the co-ordinates of the top-left and bottom-right coordinates of
        that rectangle
        """
        min_x: int = sys.maxsize
        min_y: int = sys.maxsize
        max_x: int = 0
        max_y: int = 0

        for y, line in enumerate(self._elf_positions):
            if '#' in line:
                min_y = min(min_y, y)
                max_y = max(max_y, y)

                min_x = min(min_x, ''.join(line).index('#'))
                max_x = max(max_x, ''.join(line).rfind('#'))

        print(f'Bounding rectangle spans from ({min_x},{min_y}) to ({max_x},{max_y})')
        return min_x, min_y, max_x, max_y

    def count_empty_ground_tiles_in(self, min_x, min_y, max_x, max_y) -> int:
        """
        Return the number of empty ground tiles described in a bounding rectangle
        """
        num_empty_ground_tiles: int = 0

        for y in range(min_y, max_y+1):
            tiles_in_row: int = ''.join(self._elf_positions[y]).count('.', min_x, max_x+1)
            num_empty_ground_tiles += tiles_in_row

        return num_empty_ground_tiles

    def is_elf_adjacent_to(self, x: int, y: int) -> bool:
        """
        Return whether there is an elf adjacent (including diagonals) to a given (x,y) position
        """
        return '#' in self._elf_positions[y-1][x-1:x+2] \
            or '#' in self._elf_positions[y+1][x-1:x+2] \
            or self._elf_positions[y][x-1] == '#' \
            or self._elf_positions[y][x+1] == '#'

    def print_positions(self) -> None:
        """
        Pretty print the Elf positions
        """
        digits = math.ceil(math.log10(len(self._elf_positions)))
        for i, item in enumerate(self._elf_positions):
            index_part: str = str(i).rjust(digits, '0')
            str_out: str = ''.join(item)
            print(f'{index_part}: {str_out}')

    def calculate_proposed_moves(self) -> dict:
        """
        Each Elf considers the eight positions adjacent to themself. If no
        other Elves are in one of those eight positions, the Elf does not do
        anything during this round. Otherwise, the Elf looks in each of four
        directions in the following order and proposes moving one step in the
        first valid direction:
        - If there is no Elf in the N, NE, or NW adjacent positions,
            the Elf proposes moving north one step.
        - If there is no Elf in the S, SE, or SW adjacent positions,
            the Elf proposes moving south one step.
        - If there is no Elf in the W, NW, or SW adjacent positions,
            the Elf proposes moving west one step.
        - If there is no Elf in the E, NE, or SE adjacent positions,
            the Elf proposes moving east one step.
        """
        # A dictionary of {new_location: [old_locations]}
        proposed_moves: dict = {}

        # For each position
        for y, line in enumerate(self._elf_positions):
            for x, char in enumerate(line):
                # If there is an Elf, check for neighbours
                if char == '#' and self.is_elf_adjacent_to(x, y):
                    # There is a neighbour, so look for a move
                    for dir_index in range(4):
                        # The proposed move direction
                        new_dir_index: int = (self._starting_dir + dir_index) % len(self._dx)
                        dx: int = self._dx[new_dir_index]
                        dy: int = self._dy[new_dir_index]

                        # The proposed move location
                        new_x: int = x + dx
                        new_y: int = y + dy

                        elf_in_dir: bool = False
                        # Check the three cells in that direction (e.g. for N, check N, NE, NW)
                        if dx:
                            elf_in_dir = self._elf_positions[new_y-1][new_x] == '#' or self._elf_positions[new_y][new_x] == '#' or self._elf_positions[new_y+1][new_x] == '#'
                        if dy:
                            elf_in_dir = '#' in self._elf_positions[new_y][x-1:x+2]

                        # The chosen location is vacant - propose a move
                        if not elf_in_dir:
                            # Announce that the Elf at (x, y) will move to (new_x, new_y)
                            new_location: tuple = (new_x, new_y)
                            if new_location in proposed_moves:
                                proposed_moves[new_location].append((x, y))
                            else:
                                proposed_moves[new_location] = [(x, y)]
                            # print(f'Elf at ({x},{y}) wants to move to ({new_x},{new_y})')
                            break

        # Update the starting direction
        self._starting_dir = (self._starting_dir + 1) % len(self._dx)

        return proposed_moves

    def apply_proposed_moves(self, proposed_moves: dict) -> None:
        """
        Simultaneously, each Elf moves to their proposed destination tile if
        they were the only Elf to propose moving to that position. If two or
        more Elves propose moving to the same position, none of those Elves move.
        """
        for new_pos, old_pos in proposed_moves.items():
            # Only move if there is exactly one Elf proposing to move to (x, y)
            if len(old_pos) == 1:
                # Move it from old_pos to new_pos
                self._elf_positions[old_pos[0][1]][old_pos[0][0]] = '.'
                self._elf_positions[new_pos[1]][new_pos[0]] = '#'

    def part_one(self) -> int:
        """
        Return the number of empty ground tiles contained by the smallest
        rectangle that contains every Elf.
        """
        print('== Initial State ==')
        # self.print_positions()

        # Run 10 rounds of movement
        for current_round in range(10000):
            proposed_moves: dict = self.calculate_proposed_moves()

            elves_will_move: bool = False
            for item in proposed_moves:
                if any(item):
                    elves_will_move = True

            if elves_will_move:
                self.apply_proposed_moves(proposed_moves)
            else:
                print(f'No movement in round {current_round+1}, stopping')
                break
            print(f'== End of Round {current_round+1} ==')
            # self.print_positions()

        min_x, min_y, max_x, max_y = self.calculate_bounding_rectangle()
        return self.count_empty_ground_tiles_in(min_x, min_y, max_x, max_y)

    def part_two(self) -> int:
        """
        Return the number of rounds after which the Elves stop moving
        """
        return 0

def main() -> None:
    """
    Main
    """
    solver = Day23()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()

