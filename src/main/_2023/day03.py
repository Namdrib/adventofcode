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
        self._input: list = None

        # Represents the grid (2D list)
        self._grid: list = []

        self._numbers: list = []
        self._number_row: list = []

        self._numbers_regex: str = r'\d+'

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line contains a game with a number of samples with numbers of coloured cubes
        """
        self._input = sys.stdin.read()

        for row, line in enumerate(self._input.splitlines(keepends=False)):
            self._grid.append(line)
            matching_nums: list = [int(x) for x in re.findall(self._numbers_regex, line)]
            for item in matching_nums:
                self._numbers.append(item)
                self._number_row.append(row)

    def is_symbol(self, char) -> bool:
        """
        Return whether the given character is a symbol
        Symbols are anything that's not a number, and not `.`

        :param char: _description_
        :type char: _type_
        :return: True if the character is a symbol, False otherwise
        :rtype: bool
        """
        return (not char.isdigit()) and char != '.'

    def get_neighbours_of_pos(self, x, y, length) -> list:
        """
        Return a list of neighbouring locations of a given position
        If the position is the beginning of a number (e.g. 123), the neighbours are
        the locations surrounding the entire number
        Assumption: the length of the number is specified by length

        :param x: _description_
        :type x: _type_
        :param y: _description_
        :type y: _type_
        :return: _description_
        :rtype: list
        """
        out: list = []

        min_x: int = max(0, x-1)
        max_x: int = min(len(self._grid[y])-1, x+length+1)

        # Get top
        if y > 0:
            out.extend(self._grid[y-1][min_x:max_x])
            # print(f'Got top: {out}')

        # Get sides
        if x > 0:
            out.append(self._grid[y][x-1])
            # print(f'Got left: {out}')
        if x+length < len(self._grid[y]):
            out.append(self._grid[y][x+length])
            # print(f'Got right: {out}')

        # Get bottom
        if y < len(self._grid)-1:
            out.extend(self._grid[y+1][min_x:max_x])
            # print(f'Got bottom: {out}')

        # print(f'Neighbours of {x=},{y=}: {out}')
        return out


    def is_part_number(self, number, number_row) -> bool:
        """
        Return whether a given number is a part number
        A part number is any number adjacent to a symbol, even diagonally

        :param number: The number to test for
        :type number: _type_
        :return: True if `number` is a part number, False otherwise
        :rtype: bool
        """
        x_pos: int = 0
        line = self._grid[number_row]
        match_index: int = line.find(str(number), x_pos)
        if match_index == -1:
            return False

        x_pos = match_index
        neighbours: list = self.get_neighbours_of_pos(x_pos, number_row, len(str(number)))

        part_number: bool = any(self.is_symbol(x) for x in neighbours)
        print(f'Neighbours of {str(number).rjust(3)}: {"".join(neighbours).rjust(12)} -> {part_number}')
        return part_number

    def part_one(self) -> int:
        """
        Return the sum of all of the game IDs that can be played with the available cubes
        """
        print(self._numbers)
        total: int = 0
        for number, row in zip(self._numbers, self._number_row):
            if self.is_part_number(number, row):
                total += number
        return total

    def part_two(self) -> int:
        """
        Return the sum of the powers of the minimal possible set of cubes in a game
        """
        thing = []
        return sum(x for x in thing)

def main() -> None:
    """
    Main
    """
    solver = Day03()
    solver.read_input()

    # 535440 too low
    # 544733 too high
    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
