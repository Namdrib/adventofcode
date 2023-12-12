#!/usr/bin/python3
import itertools
import math
import sys

class Day09:
    """
    Solution for https://adventofcode.com/2023/day/9
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.sensor_readings: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line is a the cumulative values of a single sensor reading
        """
        self.input = sys.stdin.read()

        for line in self.input.splitlines(keepends=False):
            self.sensor_readings.append(list(map(int, line.split())))

        for sensor_reading in self.sensor_readings:
            print(sensor_reading)

    def next_sequence(self, values: list) -> list:
        out: list = []
        for i, value in enumerate(values):
            if i < len(values)-1:
                out.append(values[i+1] - value)

        return out

    def get_sequences(self, history: list) -> int:
        sequences: list = [list(history)]
        while not all(x == 0 for x in sequences[-1]):
            next_row = self.next_sequence(sequences[-1])
            sequences.append(next_row)
        
        return sequences

    def get_extrapolated_value(self, reading: list) -> int:
        sequences: list = self.get_sequences(reading)
        sequences[-1].append(0)

        for i in range(len(sequences)-1, 0, -1):
            next_value: int = sequences[i][-1] + sequences[i-1][-1]
            sequences[i-1].append(next_value)

        print(f'New sequences:')
        for sequence in sequences:
            print(f'  {sequence}')
        return sequences[0][-1]

    def part_one(self) -> int:
        """
        Find the sum of the extrapolated values of each sensor reading
        """
        return sum(self.get_extrapolated_value(x) for x in self.sensor_readings)

    def part_two(self) -> int:
        """
        Find how many steps it takes before all of the starting nodes are simultaneously on nodes that end with Z
        """
        ARRAY: list = []
        return sum(self.calc(x) for x in ARRAY)

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
