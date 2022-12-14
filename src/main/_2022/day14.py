#!/usr/bin/python3
import sys

from Coord import Coord2D

class Day14:
    """
    Solution for https://adventofcode.com/2022/day/14
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.grid: list = []

        # These co-ordinates represent the bounds of the tiles
        # To get the "real" position in the grid, add the position to the top-left
        self.top_left: Coord2D = None
        self.bottom_right: Coord2D = None

        self.floor_y: int = None

        self.sand_entry: Coord2D = Coord2D(500, 0)

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line is a path of rocks in a grid
        """
        raw_input = sys.stdin.read()

        self.input = raw_input.split('\n')
        self.input = self.input[0:-1]

        self.build_map()

    def set_grid_pos(self, coord: Coord2D, char: str) -> None:
        """
        Set the material at a given absolute position
        Convert it to a relative position first
        """
        x = coord.x - self.top_left.x
        y = coord.y - self.top_left.y
        self.grid[y][x] = char

    def get_grid_pos(self, coord: Coord2D) -> str:
        """
        Get the material at a given absolute position
        Convert it to a relative position first
        """
        x = coord.x - self.top_left.x
        y = coord.y - self.top_left.y
        char = self.grid[y][x]
        return char


    def draw_rock_line(self, start_coord: Coord2D, end_coord: Coord2D) -> None:
        """
        Draw a single rock line in the grid from the coordinates
        """
        if start_coord.x == end_coord.x:
            # Draw a vertical line
            for y in range(min(start_coord.y, end_coord.y), max(start_coord.y, end_coord.y)+1):
                self.set_grid_pos(Coord2D(start_coord.x, y), '#')
        else:
            # Draw a horizontal line
            for x in range(min(start_coord.x, end_coord.x), max(start_coord.x, end_coord.x)+1):
                self.set_grid_pos(Coord2D(x, start_coord.y), '#')

    def build_map(self) -> None:
        self.top_left = Coord2D(self.sand_entry.x, self.sand_entry.y)
        self.bottom_right = Coord2D(self.sand_entry.x, self.sand_entry.y)

        # Do a first pass to work out relative dimensions - so we know how big to make the grid
        for path in self.input:
            path_coords = path.split(' -> ')
            for path_coord in path_coords:
                x, y = path_coord.split(',')
                x = int(x)
                y = int(y)

                self.top_left.x = min(self.top_left.x, x)
                self.top_left.y = min(self.top_left.y, y)

                self.bottom_right.x = max(self.bottom_right.x, x)
                self.bottom_right.y = max(self.bottom_right.y, y)

        # Construct the grid as all air to start with
        self.grid = [['.' for _ in range(self.bottom_right.x-self.top_left.x+1)] for _ in range(self.bottom_right.y-self.top_left.y+1)]

        # Do another pass of the input to record the rocks into the grid
        for path in self.input:
            path_coords = path.split(' -> ')
            for i in range(len(path_coords)-1):
                start_x, start_y = path_coords[i].split(',')
                end_x, end_y = path_coords[i+1].split(',')
                start: Coord2D = Coord2D(start_x, start_y)
                end: Coord2D = Coord2D(end_x, end_y)
                self.draw_rock_line(start, end)

        # Add the sand entry
        self.set_grid_pos(self.sand_entry, '+')

    def add_floor_to_scan(self) -> None:
        """
        In part 2, the grid gets an infinitely-wide floor added, 2 below the lowest rock scan
        Extend the grid 2 down, include the floor
        Because we are extending left and right, expand the grid left and right
        """
        self.floor_y = self.bottom_right.y + 2
        self.bottom_right.y = self.floor_y

        # Extend the floor by 200 in each direction
        for i in range(len(self.grid)):
            for _ in range(200):
                self.grid[i].insert(0, '.')
            self.grid[i].extend(['.' for _ in range(200)])

        self.top_left.x -= 200
        self.bottom_right.x += 200

        # Extend the grid down to accommodate the floor
        for _ in range(2):
            self.grid.append(['.' for _ in range(self.bottom_right.x-self.top_left.x+1)])

        # Draw the floor in
        self.draw_rock_line(Coord2D(self.top_left.x, self.bottom_right.y), Coord2D(self.bottom_right.x, self.bottom_right.y))

    def coord_in_bounds(self, coord: Coord2D) -> bool:
        """
        Check whether a given absolute coordinate is in the grid bounds
        """
        return coord.x in range(self.top_left.x, self.bottom_right.x+1) and coord.y in range(self.top_left.y, self.bottom_right.y+1)

    def spawn_and_drop_sand(self) -> Coord2D:
        """
        Spawn a unit of sand at the sand entry spot
        Drop the sand until it stops moving
        It moves down if possible
        If not possible, it moves diagonally down and to the left
        If that is not possible, it moves diagonally down and to the right
        If that is not possible, it comes to rest
        Return the position that the sand would come to rest
        Return None if it would overflow (go out of bounds)
        """
        # Spawn sand below the sand entry
        sand_pos: Coord2D = Coord2D(self.sand_entry.x, self.sand_entry.y)

        while self.coord_in_bounds(sand_pos):
            # See where the sand can go
            down_pos: Coord2D = Coord2D(sand_pos.x, sand_pos.y+1)
            down_left_pos: Coord2D = Coord2D(sand_pos.x-1, sand_pos.y+1)
            down_right_pos: Coord2D = Coord2D(sand_pos.x+1, sand_pos.y+1)

            potential_positions: list = [down_pos, down_left_pos, down_right_pos]

            # If it were to go out of bounds, it will overflow
            # This is relevant to part 1
            if any(not self.coord_in_bounds(pos) for pos in potential_positions):
                return None

            # Try all the positions
            found_valid_pos: bool = False
            for pos in potential_positions:
                if self.get_grid_pos(pos) == '.':
                    sand_pos = pos
                    found_valid_pos = True
                    break

            # If it couldn't move, it comes to rest here
            if not found_valid_pos:
                return sand_pos

        # This should never happen
        return sand_pos

    def fill_with_sand(self) -> None:
        """
        Fill the cave with sand until it overflows or stops
        """
        while True:
            sand_pos: Coord2D = self.spawn_and_drop_sand()
            if sand_pos:
                # Settle the sand here
                self.set_grid_pos(sand_pos, 'o')

                if sand_pos == self.sand_entry:
                    # The sand has stopped naturally (nowhere to go from entrance)
                    break
            else:
                # The sand has overflowed into the abyss
                break

    def part_one(self) -> int:
        """
        Return the units of sand that come to rest until the sand overflows from the rocks
        """
        self.fill_with_sand()
        amount_of_sand_at_rest: int = 0
        for item in self.grid:
            amount_of_sand_at_rest += item.count('o')
        return amount_of_sand_at_rest

    def part_two(self) -> int:
        """
        Return the units of sand that come to rest until the sand naturally stops
        """
        self.add_floor_to_scan()

        # This takes a while...
        self.fill_with_sand()
        amount_of_sand_at_rest: int = 0
        for item in self.grid:
            amount_of_sand_at_rest += item.count('o')
        return amount_of_sand_at_rest

def main() -> None:
    """
    Main
    """
    solver = Day14()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
