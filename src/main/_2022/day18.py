#!/usr/bin/python3
import sys

class Day18:
    """
    Solution for https://adventofcode.com/2022/day/18
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        # a 3D area of whether there is a lava cube or not
        # 1: lava
        # 0: empty space
        # 2: empty space reachable from zero
        self.lava_cubes: list = []

        # Used to bound the box later on
        self.max_x: int = 0
        self.max_y: int = 0
        self.max_z: int = 0

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()

        self.input = raw_input.split('\n')
        self.input = self.input[0:-1]

        # Calculate the size of the 3d space
        for item in self.input:
            numbers: list = list(map(int, item.split(',')))
            self.max_x = max(self.max_x, numbers[0])
            self.max_y = max(self.max_y, numbers[1])
            self.max_z = max(self.max_z, numbers[2])

        # Allocate the space
        # Allow a buffer space around so we can flood fill alter
        # Doesn't work with +2
        self.lava_cubes = [[[0 for _ in range(self.max_x+3)] for _ in range(self.max_y+3)] for _ in range(self.max_z+3)]

        # Populate the space
        for item in self.input:
            numbers: list = list(map(int, item.split(',')))
            # Increase everything by 1 so we have a boundary around
            self.lava_cubes[numbers[2]+1][numbers[1]+1][numbers[0]+1] = 1

        # For part 2: mark which parts are strictly outside
        self.mark_droplet_exterior()

    def mark_droplet_exterior(self) -> None:
        """
        Put a 2 in each spot in the lava cube if it is reachable by air
        Do a flood fill to see if a spot is reachable from 0,0,0, marking each spot with a 2
        Put the fringe in a set rather than in the program stack to avoid stack overflow
        """
        fringe: set = set()
        fringe.add((0,0,0))
        seen: set = set()

        while fringe:
            current = fringe.pop()

            # Current position not in bounds - ignore
            range_checks: list = [
                    current[0] in range(self.max_x+3),
                    current[1] in range(self.max_y+3),
                    current[2] in range(self.max_z+3)
            ]
            if not all(range_checks):
                continue

            # Current position is lava or already reachable - ignore
            if self.lava_cubes[current[2]][current[1]][current[0]] in [1,2]:
                continue

            # Mark this spot as reachable
            self.lava_cubes[current[2]][current[1]][current[0]] = 2

            # Flood fill each neighbour
            for d in [-1, 1]:
                fringe.add((current[0]+d,current[1],current[2]))
                fringe.add((current[0],current[1]+d,current[2]))
                fringe.add((current[0],current[1],current[2]+d))

            seen.add(current)

    def contributes_to_surface_area(self, x: int, y: int, z: int, exterior_only: bool) -> bool:
        """
        Return True if a block contributes to surface area
        """
        try:
            # For part 1, a block contributes to surface area if it is not another lava block
            condition = self.lava_cubes[z][y][x] != 1
            if exterior_only:
                # For part 2, a block contributes to surface area if it is just outside the droplet
                condition = self.lava_cubes[z][y][x] == 2
            return condition

        except IndexError:
            return False
        return False

    def calculate_surface_area_of_block(self, x, y, z, exterior_only: bool) -> int:
        """
        Calculate the surface area of the block at a given location if it was a lava block
        """
        num_exposed_sides = 0

        # For each neighbour in each dimension
        for d in [-1, 1]:
            if self.contributes_to_surface_area(x+d, y, z, exterior_only):
                num_exposed_sides += 1
            if self.contributes_to_surface_area(x, y+d, z, exterior_only):
                num_exposed_sides += 1
            if self.contributes_to_surface_area(x, y, z+d, exterior_only):
                num_exposed_sides += 1

        return num_exposed_sides

    def calculate_num_exposed_sides(self, exterior_only: bool) -> int:
        """
        Calculate the number of exposed sides of the lava droplets
        i.e. the sides where there aren't any adjacent lava droplets
        If exterior_only is set, don't count those that are not reachable by the outside
        e.g. if there's a hollowed out cube, don't count the inside space
        """
        total_exposed_sides: int = 0

        for z, outer in enumerate(self.lava_cubes):
            for y, mid in enumerate(outer):
                for x, inner in enumerate(mid):

                    # Only examine blocks that are lava
                    if inner == 1:
                        num_exposed_sides = self.calculate_surface_area_of_block(x, y, z, exterior_only)
                        total_exposed_sides += num_exposed_sides

        return total_exposed_sides

    def part_one(self) -> int:
        """
        Return the number of exposed sides (not adjacent to another lava cube)
        """
        num_exposed_sides: int = self.calculate_num_exposed_sides(False)
        return num_exposed_sides

    def part_two(self) -> int:
        """
        Return the number of exposed sides (side exposed to open air)
        This doesn't include air inside the droplet itself
        """
        num_exposed_sides: int = self.calculate_num_exposed_sides(True)
        return num_exposed_sides

def main() -> None:
    """
    Main
    """
    solver = Day18()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
