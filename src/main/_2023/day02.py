#!/usr/bin/python3
from math import prod
import sys

class Game:

    def __init__(self, id_: int):
        self.id: int = id_

        # A list of [# Red, # Green, # Blue]
        self._samples: list = []

        self._colour_to_index: dict = {
            'red': 0,
            'green': 1,
            'blue': 2
        }

    def add_sample(self, sample_str: str) -> None:
        """
        Record a sample into our samples.
        Regardless of the order of the given sample, always save is as [R, G, B]

        :param sample_str: A string like "3 blue, 4 red"
        :type sample_str: str
        """
        sample_result = [0, 0, 0]
        for sample_components in sample_str.split(', '):
            number, colour = sample_components.split(' ')
            sample_result[self._colour_to_index[colour]] = int(number)
            self._samples.append(sample_result)

    def minimum_possible_cubes(self) -> list:
        """
        Returns the potential maximum number of each colour of cubes in the bag
        Calculated based on the samples
        :return: A list of [R, G, B] of the potential maximum cubes the bag has
        :rtype: list
        """
        out = [0, 0, 0]
        for sample in self._samples:
            out[0] = max(out[0], sample[0])
            out[1] = max(out[1], sample[1])
            out[2] = max(out[2], sample[2])

        return out

    def can_be_played_with(self, contents: list) -> bool:
        """
        Return whether this game can be played with the given contents of [R, G, B]
        Calculated based on the samples

        :return: True if we can play a game with the given contents
        :rtype: bool
        """
        max_cubes: list = self.minimum_possible_cubes()
        return all(max_cubes[i] <= contents[i] for i in range(len(contents)))

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
        In this case, each line contains a game with a number of samples with numbers of coloured cubes
        """
        _input = sys.stdin.read()

        for line in _input.split('\n'):
            line = line.strip()
            if line:
                game_id_str, sample_str = line.split(': ')
                game_id: int = int(game_id_str[game_id_str.find(' ')+1:])
                g = Game(game_id)

                # Build up the list of samples the game has seen
                samples: list = sample_str.split('; ')
                for sample in samples:
                    g.add_sample(sample)

                self._games.append(g)

    def calculate_power(self, cubes: list) -> int:
        """
        The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together.

        :param cubes: A [R, G, B] list of cubes
        :type cubes: list
        :return: The product of the number of cubes
        :rtype: int
        """
        return prod(cubes)

    def part_one(self) -> int:
        """
        Return the sum of all of the game IDs that can be played with the available cubes
        """
        available_cubes: list = [12, 13, 14]
        return sum(x.id for x in self._games if x.can_be_played_with(available_cubes))

    def part_two(self) -> int:
        """
        Return the sum of the powers of the minimal possible set of cubes in a game
        """
        return sum(self.calculate_power(x.minimum_possible_cubes()) for x in self._games)

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
