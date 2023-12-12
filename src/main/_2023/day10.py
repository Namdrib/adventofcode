#!/usr/bin/python3
import queue
import sys

class Tile:
    def __init__(self, x: int, y: int, char: str) -> None:
        self.x = x
        self.y = y

        self.steps_from_start: int = 0 if char in 'Ss' else 99999

        self.char: str = char

        self.connects_up: bool = char in '|LJS'
        self.connects_left: bool = char in '-J7S'
        self.connects_right: bool = char in '-LFS'
        self.connects_down: bool = char in '|7FS'

    def __repr__(self) -> str:
        return f'Tile(x={self.x}, y={self.y}, char={self.char}, steps={self.steps_from_start})'

    # For use with queue.PriorityQueue
    def __hash__(self) -> int:
        return self.x + (self.x * self.y) + 2 * self.y + self.steps_from_start

    # For use with queue.PriorityQueue
    def __lt__(self, o) -> bool:
        return self.steps_from_start < o.steps_from_start

class Day10:
    """
    Solution for https://adventofcode.com/2023/day/10
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.grid: list = []

        self.start_x: int = 0
        self.start_y: int = 0

        # Up, down, left, right
        self.dx: list = [0, 0, -1, 1]
        self.dy: list = [-1, 1, 0, 0]

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, the input is a grid of characters. The characters represent connections in a loop
        """
        self.input = sys.stdin.read()

        # Read the grid, storing the character and its co-ordinates
        for y, line in enumerate(self.input.splitlines(keepends=False)):
            print(line)
            row: list = []
            for x, char in enumerate(line):
                row.append(Tile(x, y, char))
                if char in 'Ss':
                    self.start_x = x
                    self.start_y = y
            self.grid.append(row)

    def pos_in_bounds(self, x: int, y: int) -> bool:
        """
        Return whether position represented by `x`, `y` is in the grid

        :param x: The x position to check
        :type x: int
        :param y: The y position to check
        :type y: int
        :return: Whether the x, y position is in bounds
        :rtype: bool
        """
        return (0 <= x < len(self.grid[0])) and (0 <= y < len(self.grid))

    def connects_to(self, tile: Tile, dx: int, dy: int) -> bool:
        """
        Whether the tile `tile` has a connection to a given neighbour

        :param tile: The tile to check
        :type tile: Tile
        :param dx: The relative x position of the tile
        :type dx: int
        :param dy: The relative y position of the tile
        :type dy: int
        :return: Whether the tile `tile` connects with its neighbour
        :rtype: bool
        """
        other_tile: Tile = self.grid[tile.y + dy][tile.x + dx]
        if dx == 1:
            return tile.connects_right and other_tile.connects_left
        if dx == -1:
            return tile.connects_left and other_tile.connects_right
        if dy == 1:
            return tile.connects_down and other_tile.connects_up
        if dy == -1:
            return tile.connects_up and other_tile.connects_down

    def get_neighbours_of(self, tile: Tile) -> list:
        """
        Return a list of neighbours of the tile `tile`
        A tile is a neighbout if it is in bounds, and shares a connection on the loop

        :param tile: The tile to check for neighbours
        :type tile: Tile
        :return: All the valid neighbours of the tile
        :rtype: list
        """
        neighbours: list = []
        for dx, dy in zip(self.dx, self.dy):
            new_x = tile.x + dx
            new_y = tile.y + dy

            if not self.pos_in_bounds(new_x, new_y):
                continue

            if not self.connects_to(tile, dx, dy):
                continue

            neighbours.append(self.grid[new_y][new_x])

        return neighbours

    def determine_distance_from_start(self) -> None:
        """
        Perform breadth-first search (BFS) to populate the number of steps from the start
        """

        fringe: queue = queue.PriorityQueue()
        closed: set = set()

        # Start at the start
        current_node: Tile = Tile(self.start_x, self.start_y, 'S')
        fringe.put(current_node)

        # Walk along the thing
        while not fringe.empty():
            current_node: Tile = fringe.get()

            if current_node in closed:
                continue

            for neighbour in self.get_neighbours_of(current_node):
                new_distance = min(current_node.steps_from_start + 1, self.grid[neighbour.y][neighbour.x].steps_from_start)
                neighbour.steps_from_start = new_distance
                self.grid[neighbour.y][neighbour.x] = neighbour

                fringe.put(neighbour)

            closed.add(current_node)

    def part_one(self) -> int:
        """
        Find the sum of the extrapolated values of each sensor reading
        """
        self.determine_distance_from_start()
        max_distance: int = 0

        for row in self.grid:
            for tile in row:
                if tile.steps_from_start == 99999:
                    # Don't count the placeholder as a real distance
                    # It is 99999 so we can use min in determine_distance_from_start
                    continue
                if tile.steps_from_start > max_distance:
                    max_distance = tile.steps_from_start

        return max_distance

    def part_two(self) -> int:
        """
        Find the sum of the extrapolated values of each sensor reading when extrapolating backwards
        """
        return 0

def main() -> None:
    """
    Main
    """
    solver = Day10()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
