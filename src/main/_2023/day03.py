#!/usr/bin/python3
import re
import sys

class Day03:
    """
    Solution for https://adventofcode.com/2023/day/3
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        # Represents the grid (2D list)
        self.grid: list = []

        # Each element is a tuple of a number and its x and y co-ordinates (n, x, y)
        self.numbers: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line is a row in a grid. The grid contains numbers mixed in with other symbols
        Store all of the numbers, along with their co-ordinates in the grid
        """
        self.input = sys.stdin.read()

        for row, line in enumerate(self.input.splitlines(keepends=False)):
            # Add another column so the regex in is_part_number works...
            line += '.'
            self.grid.append(line)

            # Loop over the line, looking for numbers
            # These are delimited by non-digit characters
            col: int = 0
            while col < len(line):
                if line[col].isdigit():
                    match_ = re.search(r'[^\d]', line[col:])
                    non_digit_pos = match_.start()

                    # Store the number, along with its position
                    number: int = int(line[col:col+non_digit_pos])
                    self.numbers.append((number, col, row))
                    col += non_digit_pos

                else:
                    col += 1

    def is_symbol(self, char: str) -> bool:
        """
        Return whether the given character is a symbol
        Symbols are anything that's not a number, and not `.`

        :param char: The character to check for symbol-ness
        :type char: str
        :return: True if the character is a symbol, False otherwise
        :rtype: bool
        """
        return (not char.isdigit()) and char != '.'

    def get_neighbours_of_thing_starting_at_pos(self, length: int, x_pos: int, y_pos: int) -> list:
        """
        Return a list of neighbouring locations of a given position
        If the position is the beginning of a number (e.g. 123), the neighbours are
        the locations surrounding the entire number
        Assumption: the length of the number is specified by length

        :param length: The length of the thing to get neighbours of
        :type length: int
        :param x_pos: The x position of the start of the number in the grid
        :type x_pos: int
        :param y_pos: The y position of the start of the number in the grid
        :type y_pos: int
        :return: A list of neighbours of the number in the grid
        :rtype: list
        """
        out: list = []

        min_x: int = max(0, x_pos-1)
        max_x: int = min(len(self.grid[y_pos])-1, x_pos+length+1)

        # Get top
        if y_pos > 0:
            out.extend(self.grid[y_pos-1][min_x:max_x])
            # print(f'Got top: {out}')

        # Get sides
        if x_pos > 0:
            out.append(self.grid[y_pos][x_pos-1])
            # print(f'Got left: {out}')
        if x_pos+length < len(self.grid[y_pos]):
            out.append(self.grid[y_pos][x_pos+length])
            # print(f'Got right: {out}')

        # Get bottom
        if y_pos < len(self.grid)-1:
            out.extend(self.grid[y_pos+1][min_x:max_x])
            # print(f'Got bottom: {out}')

        # print(f'Neighbours of {x=},{y=}: {out}')
        return out

    def is_part_number(self, number, x_pos, y_pos) -> bool:
        """
        Return whether a given number is a part number
        A part number is any number adjacent to a symbol, even diagonally

        :param number: The number to test for
        :type number: int
        :param x_pos: The x position of the start of the number in the grid
        :type x_pos: int
        :param y_pos: The y position of the start of the number in the grid
        :type y_pos: int
        :return: True if `number` is a part number, False otherwise
        :rtype: bool
        """
        neighbours: list = self.get_neighbours_of_thing_starting_at_pos(len(str(number)), x_pos, y_pos)
        print(f'Neighbours of {str(number).rjust(3)}: {"".join(neighbours).rjust(12)} -> {number}')
        return any(self.is_symbol(x) for x in neighbours)

    def part_one(self) -> int:
        """
        Return the sum of all of the part numbers in the engine schematic
        See: self.is_part_number(...)
        """
        return sum(number for number, col, row in self.numbers if self.is_part_number(number, col, row))

    def part_two(self) -> int:
        """
        A gear is any `*` symbol that is adjacent to exactly two part numbers.
        Its gear ratio is the result of multiplying those two numbers together.
        Return the sum of all of the gear ratios in the engine schematic
        """
        total: int = 0
        for i, line in enumerate(self.grid):
            j: int = 0
            while j < len(line):
                # Found a potential gear
                if line[j] == '*':
                    neighbours: list = self.get_neighbours_of_thing_starting_at_pos(1, j, i)
                    print(f'Neighbours of {j=},{i=}: {neighbours}')

                    neighbouring_numbers: list = []

                    for neighbour in neighbours:
                        if neighbour.isdigit():
                            # TODO: Look left and right for the number to figure out what it is
                            pass

                    # It is a gear! Calculate its ratio, and add that to the total
                    if len(neighbouring_numbers) == 2:
                        total += neighbouring_numbers[0] * neighbouring_numbers[1]
                j += 1

        return total

def main() -> None:
    """
    Main
    """
    solver = Day03()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
