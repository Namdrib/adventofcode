#!/usr/bin/python3
import sys

class Mapping:
    def __init__(self, dest, source, length):
        self.dest = dest
        self.source = source
        self.length = length

        self.max = self.source + self.length

    def translate(self, n: int) -> int:
        """
        Translate a number by checking if it is in the range described by [source, source+length]
        If it is, translate it to the dest (+ the offset from the source)
        If it isn't, return the original number

        :param n: The number to translate
        :type n: int
        :return: The number after translation
        :rtype: int
        """
        if self.source <= n <= self.max:
            # print(f'  {n=} matches [{self.source=}, {self.max=}], resulting in {self.dest + (n - self.source)}')
            return self.dest + (n - self.source)
        return n

    def __str__(self) -> str:
        return f'source={self.source}, dest={self.dest}, length={self.length}'

class Day05:
    """
    Solution for https://adventofcode.com/2023/day/5
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = []

        self.seeds: list = []

        self.seed_to_soil_map: list = []
        self.soil_to_fertiliser_map: list = []
        self.fertiliser_to_water_map: list = []
        self.water_to_light_map: list = []
        self.light_to_temp_map: list = []
        self.temp_to_humidity_map: list = []
        self.humidity_to_location_map: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, the lines correspond to an Island Island Almanac
        """
        self.input = sys.stdin.read()

        map_name: str = 'seeds'
        lines = self.input.splitlines(keepends=False)
        for line in lines:
            # Empty line: do nothing
            if not line:
                continue

            # Seed line: store the seeds
            if map_name == 'seeds':
                numbers: list = line.split(': ')[1].split()
                self.seeds = list(map(int, numbers))
                map_name = 'not seeds'

            # A new map label: update our current map name
            elif line[0].isalpha():
                map_name = line.split()[0]

            # Number lines: store a map
            else:
                # Create a map out of the given numbers
                numbers: list = (list(map(int, line.split())))
                mapping = Mapping(numbers[0], numbers[1], numbers[2])

                # Probably can do better with getattr()
                if map_name == 'seed-to-soil':
                    self.seed_to_soil_map.append(mapping)
                elif map_name == 'soil-to-fertilizer':
                    self.soil_to_fertiliser_map.append(mapping)
                elif map_name == 'fertilizer-to-water':
                    self.fertiliser_to_water_map.append(mapping)
                elif map_name == 'water-to-light':
                    self.water_to_light_map.append(mapping)
                elif map_name == 'light-to-temperature':
                    self.light_to_temp_map.append(mapping)
                elif map_name == 'temperature-to-humidity':
                    self.temp_to_humidity_map.append(mapping)
                elif map_name == 'humidity-to-location':
                    self.humidity_to_location_map.append(mapping)

    def translate(self, n: int, map_: list) -> int:
        """
        _summary_

        :param n: The number to transform
        :type n: int
        :param map_: A list of all of the potential transformations
        :type map_: list
        :return: The result of translating `n`, if applicable. If not, then return n
        :rtype: int
        """
        old_n = n
        for mapping in map_:
            # print(f'Does {n=} fit in {mapping=}?')

            n = mapping.translate(n)
            if n != old_n:
                # print(f'Yes: {n=}')
                return n

        return n

    def get_location_from_seed(self, seed_num: int) -> int:
        """
        Translate a seed number through all the mappings to get the final location number

        :param seed_num: The seed number to start with
        :type seed_num: int
        :return: The final location of the seed after going through all the maps
        :rtype: int
        """
        print(f'Translating seed number {seed_num}')
        soil: int       = self.translate(seed_num, self.seed_to_soil_map)
        fertiliser: int = self.translate(soil, self.soil_to_fertiliser_map)
        water: int      = self.translate(fertiliser, self.fertiliser_to_water_map)
        light: int      = self.translate(water, self.water_to_light_map)
        temp: int       = self.translate(light, self.light_to_temp_map)
        humidity: int   = self.translate(temp, self.temp_to_humidity_map)
        location: int   = self.translate(humidity, self.humidity_to_location_map)
        print(f'  {seed_num} -> {soil} -> {fertiliser} -> {water} -> {light} -> {temp} -> {humidity} -> {location}')

        return location


    def part_one(self) -> int:
        """
        Return the lowest location number that corresponds to any of the initial seed numbers
        """
        return min(self.get_location_from_seed(x) for x in self.seeds)

    def part_two(self) -> int:
        """
        Return the number of scratchcards you end up with with the new scoring mechanism
        You win copies of the scratchcards below the winning card equal to the number of matches.
        So, if card 10 were to have 5 matching numbers, you would win one copy each of cards 11, 12, 13, 14, and 15.
        """
        lowest_location_number: int = 999999
        for i in range(0, len(self.seeds), 2):
            # print(f'Seed {self.seeds[i]} has range {self.seeds[i+1]}')
            for seed_num in range(self.seeds[i], self.seeds[i]+self.seeds[i+1]):
                location_number = self.get_location_from_seed(seed_num)
                lowest_location_number = min(lowest_location_number, location_number)

        return lowest_location_number

def main() -> None:
    """
    Main
    """
    solver = Day05()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
