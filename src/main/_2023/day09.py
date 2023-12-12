#!/usr/bin/python3
import itertools
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

    def next_sequence(self, values: list) -> list:
        """
        The next sequence is a list whose values are the differences of each
        value and its previous neighbour

        :param values: The values to generate a sequence from
        :type values: list
        :return: The next sequence of the values
        :rtype: list
        """
        return [b - a for a, b in itertools.pairwise(values)]

    def get_sequences(self, history: list) -> int:
        """
        Generate sequences from a reading until the last sequence is all zeros

        :param history: The history to generate sequences from
        :type history: list
        :return: All sequences generated from the history, until the last is all zeros
        :rtype: int
        """
        # So we don't modify history
        sequences: list = [list(history)]

        # Keep generating sequences till we get one that's all zeros
        while not all(x == 0 for x in sequences[-1]):
            sequences.append(self.next_sequence(sequences[-1]))

        return sequences

    def get_extrapolated_value(self, reading: list) -> int:
        """
        Extrapolate by adding 0 to the end of the sequence of 0s,
        then fill in the last values for each previous sequence

        :param reading: The sensor reading to extrapolate
        :type reading: list
        :return: The extrapolated value
        :rtype: int
        """
        sequences: list = self.get_sequences(reading)
        sequences[-1].append(0)

        # Starting from the last sequence, populate the last element of each sequence
        for i in range(len(sequences)-1, 0, -1):
            next_value: int = sequences[i-1][-1] + sequences[i][-1]
            sequences[i-1].append(next_value)

        return sequences[0][-1]

    def get_back_extrapolated_value(self, reading: list) -> int:
        """
        Extrapolate backwards by adding 0 to the beginning of the sequence of 0s,
        then fill in the first values for each previous sequence

        :param reading: The sensor reading to extrapolate backwards from
        :type reading: list
        :return: The extrapolated value
        :rtype: int
        """
        sequences: list = self.get_sequences(reading)
        sequences[-1].insert(0, 0)

        # Starting from the last sequence, populate the first element of each sequence
        for i in range(len(sequences)-1, 0, -1):
            next_value: int = sequences[i-1][0] - sequences[i][0]
            sequences[i-1].insert(0, next_value)

        return sequences[0][0]

    def part_one(self) -> int:
        """
        Find the sum of the extrapolated values of each sensor reading
        """
        return sum(self.get_extrapolated_value(x) for x in self.sensor_readings)

    def part_two(self) -> int:
        """
        Find the sum of the extrapolated values of each sensor reading when extrapolating backwards
        """
        return sum(self.get_back_extrapolated_value(x) for x in self.sensor_readings)

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
