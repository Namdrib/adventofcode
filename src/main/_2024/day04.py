#!/usr/bin/python3
import sys

class Day04:
    """
    Solution for https://adventofcode.com/2024/day/4
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.grid: list = []
        self.a_count: list = []

        self.dir: list = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        self.dx: list = [ 0,  1, 1, 1, 0, -1, -1, -1]
        self.dy: list = [-1, -1, 0, 1, 1,  1,  0, -1]

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()

        self.input = raw_input.splitlines()

        for item in self.input:
            self.grid.append(list(item))
            self.a_count.append([0 for x in range(len(item))])

    def num_matches_at(self, x: int, y: int, target: str, mark_centre: bool = False) -> int:
        # See how many ways we can spell the target out
        # For each direction

        num_matches: int = 0
        for dir_index, direction in enumerate(self.dir):
            dx = self.dx[dir_index]
            dy = self.dy[dir_index]
            end_x: int = x + (len(target)-1) * dx
            end_y: int = y + (len(target)-1) * dy

            if 0 <= end_x < len(self.grid[0]) and 0 <= end_y < len(self.grid):
                word: str = ""
                for i, char in enumerate(target):
                    word += self.grid[y + i * dy][x + i * dx]

                    if word == target:
                        print(f'Found match at {y=}, {x=}, going {dy=}, {dx=}')
                        num_matches += 1

                        if dir_index % 2 == 1 and mark_centre:
                            print(f'Marking A at {y+dy}, {x+dx}')
                            self.a_count[y + dy][x + dx] += 1

        return num_matches

    def search_grid_for(self, target: str) -> int:
        """
        Count how many times the target string appears in the grid
        Allow forwards, backwards, up, down, left, right, diagonals

        :param grid: _description_
        :type grid: list
        :param target: _description_
        :type target: str
        :return: _description_
        :rtype: int
        """

    def part_one(self) -> int:
        """
        Return the ...
        """
        print(self.grid)
        count: int = 0

        # For each position
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                matches_at_pos: int = self.num_matches_at(x, y, 'XMAS')
                count += matches_at_pos

        return count

    def part_two(self) -> int:
        """
        Return the ...
        """
        count: int = 0

        # For each position
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                self.num_matches_at(x, y, 'MAS', True)

        for y in self.a_count:
            for x in y:
                if x >= 2:
                    count += 1
        return count

def main() -> None:
    """
    Main
    """
    solver = Day04()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
