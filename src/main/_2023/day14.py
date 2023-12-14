#!/usr/bin/python3
import sys

class Day14:
    """
    Solution for https://adventofcode.com/2023/day/14
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.grid: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, the input is a grid of rocks, represented by:
        - '.': empty space
        - '#': supports that don't move
        - 'O': rocks that are free to move
        """
        self.input = sys.stdin.read()

        for line in self.input.splitlines(keepends=False):
            # Empty line, we've reached the end of a grid
            self.grid.append([x for x in line])

    def roll_rock_up(self, grid: list, x: int, y: int) -> int:
        """
        Calculate the new position of a rock rolling up

        :param grid: The layout of the rocks
        :type grid: list
        :param x: The x co-ordinate of the rock to roll
        :type x: int
        :param y: The y co-ordinate of the rock to roll
        :type y: int
        :return: The y position of the rock after moving
        :rtype: int
        """
        ret: int = y

        # See how far up we can roll the rock at grid[y][x]
        for new_y in range(y-1, -1, -1):
            potential_grid_position: str = grid[new_y][x]
            if potential_grid_position == '.':
                if new_y <= 0:
                    ret = 0
                    break
                ret = new_y
            else:
                break

        return ret

    def roll_rock_down(self, grid: list, x: int, y: int) -> int:
        """
        Calculate the new position of a rock rolling down

        :param grid: The layout of the rocks
        :type grid: list
        :param x: The x co-ordinate of the rock to roll
        :type x: int
        :param y: The y co-ordinate of the rock to roll
        :type y: int
        :return: The y position of the rock after moving
        :rtype: int
        """
        ret: int = y
        limit: int = len(grid)-1

        # See how far up we can roll the rock at grid[y][x]
        for new_y in range(y+1, len(grid)):
            potential_grid_position: str = grid[new_y][x]
            if potential_grid_position == '.':
                if new_y >= limit:
                    ret = limit
                    break
                ret = new_y
            else:
                break

        return ret

    def roll_rock_left(self, grid: list, x: int, y: int) -> int:
        """
        Calculate the new x position of a rock rolling left

        :param grid: The layout of the rocks
        :type grid: list
        :param x: The x co-ordinate of the rock to roll
        :type x: int
        :param y: The y co-ordinate of the rock to roll
        :type y: int
        :return: The x position of the rock after moving
        :rtype: int
        """
        ret: int = x

        # See how far left we can roll the rock at grid[y][x]
        for new_x in range(x-1, -1, -1):
            potential_grid_position: str = grid[y][new_x]
            if potential_grid_position == '.':
                if new_x <= 0:
                    ret = 0
                    break
                ret = new_x
            else:
                break

        return ret

    def roll_rock_right(self, grid: list, x: int, y: int) -> int:
        """
        Calculate the new x position of a rock rolling right

        :param grid: The layout of the rocks
        :type grid: list
        :param x: The x co-ordinate of the rock to roll
        :type x: int
        :param y: The y co-ordinate of the rock to roll
        :type y: int
        :return: The x position of the rock after moving
        :rtype: int
        """
        ret: int = x
        limit = len(grid[y]) - 1

        # See how far left we can roll the rock at grid[y][x]
        for new_x in range(x+1, len(grid[y])):
            potential_grid_position: str = grid[y][new_x]
            if potential_grid_position == '.':
                if new_x >= limit:
                    ret = limit
                    break
                ret = new_x
            else:
                break

        return ret

    def tilt_up_down(self, grid: list, up: bool) -> list:
        """
        Tilt the grid up or down, letting the rocks (O) roll until they hit an obstacle

        :param grid: The grid to tilt
        :type grid: list
        :param up: Whether to roll up (True) or down (False)
        :type up: bool
        :return: The new rock arrangement after tilting the grid
        :rtype: list
        """
        for pre_y, line in enumerate(grid):
            for x in range(len(line)):
                y = pre_y if up else len(grid)-pre_y-1
                if grid[y][x] == 'O':
                    new_y: int = self.roll_rock_up(grid, x, y) if up else self.roll_rock_down(grid, x, y)
                    grid[y][x] = '.'
                    grid[new_y][x] = 'O'

        return grid

    def tilt_left_right(self, grid: list, left: bool) -> list:
        """
        Tilt the grid left or right, letting the rocks (O) roll until they hit an obstacle

        :param grid: The grid to tilt
        :type grid: list
        :param up: Whether to roll left (True) or right (False)
        :type up: bool
        :return: The new rock arrangement after tilting the grid
        :rtype: list
        """
        for y, line in enumerate(grid):
            for pre_x in range(len(line)):
                x = pre_x if left else len(grid[y])-pre_x-1
                if grid[y][x] == 'O':
                    new_x: int = self.roll_rock_left(grid, x, y) if left else self.roll_rock_right(grid, x, y)
                    grid[y][x] = '.'
                    grid[y][new_x] = 'O'

        return grid

    def do_spin_cycle(self, grid: list) -> list:
        """
        A spin cycle rolls the rocks north, then west, then south, then east

        :param grid: The grid to perform the spin cycle on
        :type grid: list
        :return: The new rock arrangement after doing a spin cycle
        :rtype: list
        """
        north_grid: list = self.tilt_up_down(grid, True)
        west_grid: list = self.tilt_left_right(north_grid, True)
        south_grid: list = self.tilt_up_down(west_grid, False)
        east_grid: list = self.tilt_left_right(south_grid, False)
        return east_grid

    def calculate_load(self, grid: list) -> int:
        """
        The amount of load caused by a single rounded rock (O) is equal to
        the number of rows from the rock to the south edge of the platform,
        including the row the rock is on.

        :param grid: The grid to calculate the load of
        :type grid: list
        :return: The load on the north edge
        :rtype: int
        """
        num_rows: int = len(grid)

        total_load: int = 0
        for i, row in enumerate(grid):
            load_per_rock: int = num_rows - i
            total_load += row.count('O') * load_per_rock

        return total_load

    def part_one(self) -> int:
        """
        Find the total load on the north support beams after rolling the rocks north
        """
        north_grid: list = self.tilt_up_down(self.grid, True)

        total_load = self.calculate_load(north_grid)
        return total_load

    def part_two(self) -> int:
        """
        Find the total load on the north support beams after 1000000000 spin cycles
        See: do_spin_cycle(grid)
        """
        # Store each grid that is seen
        # seen[grid] = grid ID
        seen: dict = {}

        # cycle_load[grid ID] = load
        cycle_load: dict = {}

        # Used to detect the loop
        loop_start: int = -1

        ###
        # Perform spin cycles until we encounter a loop
        ###
        num_cycles: int = 1000000000
        for i in range(num_cycles):
            # Do a spin cycle
            spin_grid: list = self.do_spin_cycle(self.grid)

            # Make a representation of the grid that can go into a dict
            flattened_grid: str = ''.join(''.join(char for char in line) for line in spin_grid)

            # We've seen this grid before
            # Record the grid # (a unique ID for this particular grid layout)
            # In this case, it's simply the nth grid that has been seen
            # At this point, there's enough information to calculate where the last cycle will be
            if flattened_grid in seen:
                loop_start = seen[flattened_grid]
                # print(f'Seen grid {i+1} at #{loop_start}')
                break

            # Otherwise, put it into the known grid layouts
            grid_load: int = self.calculate_load(spin_grid)
            seen[flattened_grid] = len(seen)+1
            cycle_load[len(seen)+1] = grid_load

        ###
        # A loop has been observed
        # Calculate where the last cycle will end up
        ###

        # Each state is stored into `seen`, with the value being the unique ID of that grid
        # The loop starts at loop_start
        # The loop will always end at the highest-valued `seen` element (the length of `seen`)
        # This can be used to calculate the length of the loop
        loop_length: int = len(seen) - loop_start + 1

        # Out of the `num_cycles` cycles, loop_start+1 are not part of the loop
        looping_cycles: int = num_cycles - loop_start + 1
        # print(f'{looping_cycles=}')

        # Once we enter the cycle, calculate which cycle number we end up on
        ending_pos = looping_cycles % loop_length
        # Remember to offset by where the loop starts
        ending_pos += loop_start
        # print(f'{ending_pos=}')

        # Retrieve the load of the corresponding cycle
        return cycle_load[ending_pos]

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
