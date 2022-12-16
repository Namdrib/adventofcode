#!/usr/bin/python3
import re
import sys

class Sensor:
    """
    A sensor
    """

    def __init__(self, x, y) -> None:
        """
        Sensor constructor
        """
        self.x: int = x
        self.y: int = y

        self.nearest_beacon_x: int = 0
        self.nearest_beacon_y: int = 0

        self.x_distance: int = 0
        self.y_distance: int = 0
        self.distance_to_beacon: int = 0

    def set_nearest_beacon(self, x, y) -> None:
        """
        Set where the nearest beacon is and calculate the distance to it
        """
        self.nearest_beacon_x = x
        self.nearest_beacon_y = y

        self.calculate_distance_to_nearest_beacon()

    def calculate_distance_to_nearest_beacon(self) -> None:
        """
        Calculate the manhattan distance to the nearest beacon
        """
        self.x_distance = abs(self.x - self.nearest_beacon_x)
        self.y_distance = abs(self.y - self.nearest_beacon_y)
        self.distance_to_beacon = self.x_distance + self.y_distance

    def get_fringe_coords(self, upper_x: int, upper_y: int) -> set:
        """
        Find all of the coordinates that just out of reach of this sensor
        i.e. one distance further than the nearest sensor
        """
        fringe_coords: set = set()

        # Start directly above the sensor, just out of its range
        # Move clockwise around the sensor, getting all the points just out of reach
        x = self.x
        y = self.y - self.distance_to_beacon - 1

        # Top-right quadrant
        while y != self.y:
            if x in range(0, upper_x+1) and y in range(0, upper_y+1):
                fringe_coords.add((x, y))
            x += 1
            y += 1

        # Bottom-right quadrant
        while x != self.x:
            if x in range(0, upper_x+1) and y in range(0, upper_y+1):
                fringe_coords.add((x, y))
            x -= 1
            y += 1

        # Bottom-left quadrandt
        while y != self.y:
            if x in range(0, upper_x+1) and y in range(0, upper_y+1):
                fringe_coords.add((x, y))
            x -= 1
            y -= 1

        # Top-left quadrant
        while x != self.x:
            if x in range(0, upper_x+1) and y in range(0, upper_y+1):
                fringe_coords.add((x, y))
            x += 1
            y -= 1

        return fringe_coords

class Day15:
    """
    Solution for https://adventofcode.com/2022/day/15
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.sensors: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()

        self.input = raw_input.split('\n')
        self.input = self.input[0:-1]

        for item in self.input:
            numbers: list = list(map(int, re.findall(r'\-?\d+', item)))
            sensor: Sensor = Sensor(numbers[0], numbers[1])
            sensor.set_nearest_beacon(numbers[2], numbers[3])
            self.sensors.append(sensor)

    def get_occupied_positions_at(self, y) -> int:
        """
        Get the number of places on a specific row that a sensor cannot possible be at
        """
        min_x: int = min(map(lambda s: s.x, self.sensors))
        max_x: int = max(map(lambda s: s.x, self.sensors))

        max_x_distance: int = max(map(lambda s: s.x_distance, self.sensors))

        num_occipied_positions: int = 0
        # for each reachable x in row x
        # extend past the bounds of the sensors by the maximum reachable distance
        for x in range(min_x - max_x_distance, max_x + max_x_distance + 1):
            for s in self.sensors:
                # We are on a beacon
                if x == s.nearest_beacon_x and y == s.nearest_beacon_y:
                    break

                # We are in range of a sensor
                distance_to_sensor: int = abs(x - s.x) + abs(y - s.y)
                if distance_to_sensor <= s.distance_to_beacon:
                    num_occipied_positions += 1
                    break

        return num_occipied_positions

    def get_all_fringe_coords(self) -> set:
        """
        Get all of the fringe coords for all of the sensors
        The full set is far too big to return at once so just do one at a time
        Go through each of the sensors, one-by-one and get their fringes
        """
        for s in self.sensors:
            s_fringe: set = s.get_fringe_coords(4000000, 4000000)

            yield s_fringe

    def calculate_tuning_frequency(self, x, y) -> int:
        """
        Calculate the tuning frequency of a particular coordinate
        """
        return x * 4000000 + y

    def locate_distress_beacon(self) -> tuple:
        """
        The distress beacon is a beacon that is in the one place not covered by the sensors
        Return the x, y coordinates of the distress beacon
        """
        for fringe_coords in self.get_all_fringe_coords():
            for x, y in fringe_coords:
                # For each co-ordinate, check whether we are in sensor range
                for s in self.sensors:
                    # We are on a beacon
                    if x == s.nearest_beacon_x and y == s.nearest_beacon_y:
                        break

                    # We are in range of a sensor
                    distance_to_sensor: int = abs(x - s.x) + abs(y - s.y)
                    if distance_to_sensor < s.distance_to_beacon+1:
                        break
                else:
                    # Not covered by any sensors or beacons - must be the distress beacon
                    print(f'Distress beacon at {x},{y}')
                    return x, y

        # Couldn't find a distress beacon
        return -1, -1

    def part_one(self) -> int:
        """
        Return the number of positions on a row (y) that cannot have a beacon
        Note: this takes about 15 seconds
        """
        # return self.get_occupied_positions_at(10) for the example input
        return self.get_occupied_positions_at(2000000)

    def part_two(self) -> int:
        """
        Find the one spot where the distress beacon can be (not covered by any sensor)
        Return its tuning frequency
        Note: this takes about a minute
        """
        # Find all of the coords just outside the sensor's closest beacon
        x, y = self.locate_distress_beacon()
        tuning_frequency: int = self.calculate_tuning_frequency(x, y)
        return tuning_frequency

def main() -> None:
    """
    Main
    """
    solver = Day15()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
