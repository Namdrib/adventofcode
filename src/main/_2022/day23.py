#!/usr/bin/python3
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

        # Store all Elf positions in a set as a tuple of (x, y)
        # Makes it cheap to query if a given position is in the set
        self._elf_positions: set = set()

        self._dir_names: list = ['NORTH', 'SOUTH', 'WEST', 'EAST']
        self._dx: list = [0, 0, -1, 1]
        self._dy: list = [-1, 1, 0, 0]

        # The first direction the Elves will consider when moving
        # This changes after each round of movement
        self._start_dir: int = 0

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line contains a grid of empty space (.) or an Elf (#)
        Store each Elf's position into a set of tuples
        """
        _input = sys.stdin.read()

        for y, line in enumerate(_input.split('\n')):
            line = line.strip()

            for x, char in enumerate(line):
                if char == '#':
                    # Store the Elf's position
                    self._elf_positions.add((x, y))

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

        for position in self._elf_positions:
            min_y = min(min_y, position[1])
            max_y = max(max_y, position[1])

            min_x = min(min_x, position[0])
            max_x = max(max_x, position[0])

        print(f'Bounding rectangle spans from ({min_x},{min_y}) to ({max_x},{max_y})')
        return min_x, min_y, max_x, max_y

    def count_empty_ground_tiles_in(self, min_x, min_y, max_x, max_y) -> int:
        """
        Return the number of empty ground tiles described in a bounding rectangle
        """
        # The rectangle covers all elves, so calculate its area, minus the number of elves
        return (max_x - min_x + 1) * (max_y - min_y + 1) - len(self._elf_positions)

    def is_elf_adjacent_to(self, x: int, y: int) -> bool:
        """
        Return whether there is an elf adjacent (including diagonals) to a given (x,y) position
        """
        # For each position adjacent to the Elf, see if that position is in self._elf_positions
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                # Ignore the Elf's own position
                if (dx != 0) or (dy != 0):
                    neighbour = (x + dx, y + dy)
                    if neighbour in self._elf_positions:
                        # print(f'\tHas neighbour {neighbour}. Looks to move')
                        return True

        return False

    def print_positions(self) -> None:
        """
        Pretty print the Elf positions
        Very useful for debugging ;)
        """
        print(self._elf_positions)
        min_x, min_y, max_x, max_y = self.calculate_bounding_rectangle()

        for y in range(min_y, max_y+1):
            for x in range(min_x, max_x+1):
                position = (x, y)
                sys.stdout.write('#' if position in self._elf_positions else '.')
            sys.stdout.write('\n')

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
        # This makes it easier to tell if multiple Elves are moving to the same spot
        proposed_moves: dict = {}

        # For each position
        for position in self._elf_positions:
            if not self.is_elf_adjacent_to(position[0], position[1]):
                continue

            # There is an adjacent Elf, so it wants to move
            for dir_offset in range(len(self._dx)):
                # The proposed move direction
                new_dir_index: int = (self._start_dir + dir_offset) % len(self._dx)
                dx: int = self._dx[new_dir_index]
                dy: int = self._dy[new_dir_index]

                # The proposed move location
                new_x: int = position[0] + dx
                new_y: int = position[1] + dy

                # Check the three cells in that direction (e.g. for N, check N, NE, NW)
                if dx:
                    dir_spaces: list = [(new_x, new_y-1), (new_x, new_y), (new_x, new_y+1)]
                if dy:
                    dir_spaces: list = [(new_x-1, new_y), (new_x, new_y), (new_x+1, new_y)]
                elf_in_dir: bool = any([True for x in dir_spaces if x in self._elf_positions])

                # Nothing to do if an Elf is in that position
                if elf_in_dir:
                    continue

                # The chosen location is vacant - propose a move
                # Announce that the Elf at (x, y) will move to (new_x, new_y)
                new_location: tuple = (new_x, new_y)
                if new_location in proposed_moves:
                    proposed_moves[new_location].append((position[0], position[1]))
                else:
                    proposed_moves[new_location] = [(position[0], position[1])]
                break

        # Update the starting direction
        self._start_dir = (self._start_dir + 1) % len(self._dx)

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
                self._elf_positions.remove(old_pos[0])
                self._elf_positions.add(new_pos)
                # self._elf_positions[old_pos[0][1]][old_pos[0][0]] = '.'
                # self._elf_positions[new_pos[1]][new_pos[0]] = '#'

    def part_one(self) -> int:
        """
        Return the number of empty ground tiles contained by the smallest
        rectangle that contains every Elf.
        """
        print('== Initial State ==')
        # self.print_positions()

        current_round: int = 1
        empty_tiles: int = -1

        while True:
            proposed_moves: dict = self.calculate_proposed_moves()

            if any(proposed_moves):
                self.apply_proposed_moves(proposed_moves)
            else:
                # Part 2: the round in which the Elves stop moving
                print(f'No movement in round {current_round}, stopping')
                break

            print(f'== End of Round {current_round} ==')
            # self.print_positions()

            if current_round == 10:
                # The answer for part 1
                min_x, min_y, max_x, max_y = self.calculate_bounding_rectangle()
                empty_tiles = self.count_empty_ground_tiles_in(min_x, min_y, max_x, max_y)

            current_round += 1

        return empty_tiles, current_round

    def part_two(self) -> int:
        """
        Return the number of rounds after which the Elves stop moving
        """
        # This is rolled up into part_one because it relies on continuous running,
        # and I don't want to build in logic to start a new run again
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
