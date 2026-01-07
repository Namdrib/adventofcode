#!/usr/bin/python3
import itertools
import os
from queue import PriorityQueue
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day09:
    """
    Solution for https://adventofcode.com/2025/day/9
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.tiles: list = None
        self.x_lines: set = None
        self.y_lines: set = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line is a set of co-ordinates representing the X,Y
        location of a red tile
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.tiles = []
        self.x_lines = set()
        self.y_lines = set()

        for item in self.input:
            x, y = [int(x) for x in item.split(',')]
            self.tiles.append((x, y))

        # Build the set of x- and y- lines
        prev_tile: tuple = self.tiles[-1]
        for tile in self.tiles:
            line = (min(tile, prev_tile), max(tile, prev_tile))
            if tile[0] == prev_tile[0]:
                self.y_lines.add(line)
            else:
                self.x_lines.add(line)
            prev_tile = tile

    def calculate_area_within_tiles(self, tile_1: tuple, tile_2: tuple) -> int:
        x1 = tile_1[0]
        y1 = tile_1[1]

        x2 = tile_2[0]
        y2 = tile_2[1]

        # +1 because we must include the row/column the tiles are on
        dx: int = abs(x1 - x2) + 1
        dy: int = abs(y1 - y2) + 1

        return dx * dy

    def line_intersects_rectangle(self, tile_1: tuple, tile_2: tuple, line: tuple) -> bool:
        """
        A point is described as a tuple of (x, y)
        A line is described as a tuple of (point 1, point 2)
        Assume all lines ahve their co-ordinates sorted. That is:
        line[0] < line[1] in whatever dimension that matters
        A rectangle is described as a tuple of (point 1, point 2)

        Return True if a given line intersects the rectangle described by tile_1
        and tile_2

        :param tile_1: The first tile in a rectangle
        :type tile_1: tuple
        :param tile_2: The second tile in a rectangle
        :type tile_2: tuple
        :param line: The line to query
        :type line: tuple
        :return: True if the line intersects the rectangle, False otherwise
        :rtype: bool
        """
        # Reframe the rectangle in terms of (min x, min y) and (max x, may x)
        # This makes it easier to refer to the extreme bounds of the rectangle
        # Also, "shrink" the rectangle in by 1 in each dimension to account for
        # lines that straddle the boudnary of the rectangle, since each line is also part of the rectangle
        min_point: tuple = (min(tile_1[0], tile_2[0])+1, min(tile_1[1], tile_2[1])+1)
        max_point: tuple = (max(tile_1[0], tile_2[0])-1, max(tile_1[1], tile_2[1])-1)

        # Deal with Y lines (vertical)
        # All the logic here refers to X and Y relationships between a line
        # along the Y axis
        # It can be "flipped" to refer to the X axis as well, by swapping all
        # references to X and Y
        if line[0][0] == line[1][0]:
            # A line along the Y axis (that is, vertical) can only intersect the
            # rectangle if the line's X points are contained within the rectangle's
            # min X and max X. That is, if it's too far to the left or right, it can
            # never intersect
            if line[0][0] < min_point[0] or line[0][0] > max_point[0]:
                return False


            # If the line's X points are contained within the rectangle's min X and
            # max X, the line can only intersect the rectange if it intersects the
            # rectangle's min X line, OR it intersects the rectangle's max X line
            # That is:
            # The line's min Y <= the rectangle's min Y and the line's max Y >= the rectangle's min Y
            # The line's min Y <= the rectangle's max Y and the line's max Y >= the rectangle's max Y
            intersects_min_x_line: bool = line[0][1] <= min_point[1] and line[1][1] >= min_point[1]
            intersects_max_x_line: bool = line[0][1] <= max_point[1] and line[1][1] >= max_point[1]
            if intersects_min_x_line or intersects_max_x_line:
                return True
            else:
                return False

        # Deal with X lines (horizontal)
        else:
            if line[0][1] < min_point[1] or line[0][1] > max_point[1]:
                return False

            intersects_min_y_line: bool = line[0][0] <= min_point[0] and line[1][0] >= min_point[0]
            intersects_max_y_line: bool = line[0][0] <= max_point[0] and line[1][0] >= max_point[0]
            if intersects_min_y_line or intersects_max_y_line:
                return True
            else:
                return False

            return False

    def region_is_red_or_green_only(self, tile_1: tuple, tile_2: tuple) -> bool:
        """
        Return whether the rectangle described by the points at tile_1 and
        tile_2 would contain only red or green tiles

        :param tile_1: The first tile in a rectangle
        :type tile_1: tuple
        :param tile_2: The second tile in a rectangle
        :type tile_2: tuple
        :return: True if all the tiles in the rectangle created by tile_1 and
        tile_2 would contain only red or green tiles, False otherwise
        :rtype: bool
        """
        # If any of the lines intersect, it is not a rectangle
        for line in self.x_lines:
            if self.line_intersects_rectangle(tile_1, tile_2, line):
                return False

        for line in self.y_lines:
            if self.line_intersects_rectangle(tile_1, tile_2, line):
                return False

        # If we got to this point, none of the lines intersect
        return True

    def part_one(self) -> int:
        """
        Rectangles of tiles can be formed by selecting two corner tiles
        Return the area of the largest rectangle of tiles that can be made from
        a pair of corner tiles
        """
        largest_area: int = 0

        # Calculate the area of each pair of tiles
        # Store the largest area
        for t1, t2 in itertools.combinations(self.tiles, 2):
            area: int = self.calculate_area_within_tiles(t1, t2)
            largest_area = max(largest_area, area)

        return largest_area

    def part_two(self) -> int:
        """
        A tile is green if it exists in the straight line between a red tile and
        either of the red tiles before or after it
        That is, the tiles between tiles N-1 and N, and the tiles between tiles
        N and N+1 are green
        These green tiles create a polygon. All tiles within this polygon are
        also green
        Return the area of the largest rectangle of tiles that can be made from
        a pair of corner tiles given the entire rectangle must be made of red or
        green tiles only
        """
        # Store the rectangles, sorted by area (largest first)
        # This means the first valid rectangle we come across is the largest
        rectangle_area: PriorityQueue = PriorityQueue()

        for t1, t2 in itertools.combinations(self.tiles, 2):
            area: int = self.calculate_area_within_tiles(t1, t2)
            # Because priority queues are always min-first, put the negative of
            # the area so we take the largest rectangles first
            rectangle_area.put((-area, (t1, t2)))

        while not rectangle_area.empty():
            area, rectangle = rectangle_area.get()
            if self.region_is_red_or_green_only(rectangle[0], rectangle[1]):
                # Two negatives make a positive
                return -area

def main() -> None:
    """
    Main
    """
    solver = Day09()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
