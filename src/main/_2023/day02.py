#!/usr/bin/python3
from collections import namedtuple
from math import prod
import sys

class Game:

    def __init__(self, id_: int):
        self.id: int = id_
        # A list of {# Red, # Green, # Blue}
        self._samples: list = []

        self._colour_to_index: dict = {
            'red': 0,
            'green': 1,
            'blue': 2
        }

    def add_sample(self, sample_str: str) -> None:
        """
        Record a sample into our samples

        :param sample_str: A string like "3 blue, 4 red"
        :type sample_str: str
        """
        # print(f'Adding {sample_str=}')
        sample_result = [0, 0, 0]
        for sample_components in sample_str.split(', '):
            number, colour = sample_components.split(' ')
            sample_result[self._colour_to_index[colour]] = int(number)
            self._samples.append(sample_result)

    def potential_max_cubes(self):
        """
        Returns the potential maximum number of each colour of cubes in the bag
        Calculated based on the samples
        :return: A tuple of (R, G, B) of the potential maximum cubes the bag has
        :rtype: Tuple
        """
        out = [0, 0, 0]
        for sample in self._samples:
            out[0] = max(out[0], sample[0])
            out[1] = max(out[1], sample[1])
            out[2] = max(out[2], sample[2])

        print(f'{self.id} max: {out}')
        return out

    def can_be_played_with(self, contents: list) -> bool:
        """
        Return whether this game can be played with the given contents
        Calculated based on the samples

        :return: True if we can play a game with the given contents
        :rtype: Tuple
        """
        max_cubes: list = self.potential_max_cubes()
        return all(max_cubes[i] <= contents[i] for i in range(len(contents)))

    def calculate_power(self) -> int:
        return prod(self.potential_max_cubes())

class Day02:
    """
    Solution for https://adventofcode.com/2023/day/2
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self._input: list = None

        # Represents the Games we have
        self._games: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line contains an alphanumeric string
        """
        _input = sys.stdin.read()

        for line in _input.split('\n'):
            line = line.strip()
            if line:
                game_id_str, sample_str = line.split(': ')
                game_id: int = int(game_id_str[game_id_str.find(' ')+1:])
                g = Game(game_id)
                print(f'Creating game {game_id}')

                samples: list = sample_str.split('; ')
                for sample in samples:
                    g.add_sample(sample)

                print(g._samples)

                self._games.append(g)


    def get_calibration_value(self, line: str) -> int:
        """
        Combine the first digit and the last digit to form a single two-digit number

        :param line: A line from the calibration document
        :type line: str
        :return: The concatenated two-digit number
        :rtype: int
        """
        # Keep it as a string so it can be concatenated
        digits: list = [x for x in line if x.isdigit()]
        calibration_value: str = digits[0] + digits[-1]
        return int(calibration_value)

    def part_one(self) -> int:
        """
        Return the sum of all of the calibration values
        """
        return sum(x.id for x in self._games if x.can_be_played_with([12, 13, 14]))

    def part_two(self) -> int:
        """
        Return the sum of all of the calibration values after pre-processing the document
        """
        # Represents the calibration doc after translating the number words to digits
        return sum(x.calculate_power() for x in self._games)

def main() -> None:
    """
    Main
    """
    solver = Day02()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
