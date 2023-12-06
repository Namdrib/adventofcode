#!/usr/bin/python3
import sys

class Day06:
    """
    Solution for https://adventofcode.com/2023/day/6
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self._input: list = None

        self.times: list = []
        self.distances: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line contains an alphanumeric string
        """
        self._input = sys.stdin.read()

        times, distances = self._input.splitlines(keepends=False)
        self.times = list(map(int, times.split(': ')[1].split()))
        self.distances = list(map(int, distances.split(': ')[1].split()))

    def calculate_distance(self, total_time: int, time_accelerating: int) -> int:
        """
        Calculate the distance travelled given a length of time, if `time_accelerating` was spent accelerating

        :param total_time: The amount of time available to race
        :type total_time: int
        :param time_accelerating: The time spent accelerating before moving
        :type time_accelerating: int
        :return: The total distance travelled
        :rtype: int
        """
        if total_time <= 0:
            return 0
        if time_accelerating >= total_time:
            return 0

        return time_accelerating * (total_time - time_accelerating)

    def calculate_ways_to_win(self, time: int, distance: int) -> int:
        """
        Calculate the number of ways to beat `distance` with the available time

        :param time: The amount of available time
        :type time: int
        :param distance: The distance to beat
        :type distance: int
        :return: The number of ways to beat `distance` with the available time
        :rtype: int
        """
        first_win: int = 0
        for i in range(time+1):
            distance_travelled: int = self.calculate_distance(time, i)
            if distance_travelled > distance:
                first_win = i
                print(f'Start winning at {first_win=}')
                break

        last_win: int = 0
        for i in range(time+1, 0, -1):
            distance_travelled: int = self.calculate_distance(time, i)
            if distance_travelled > distance:
                print(f'Stop winning at {last_win=}')
                last_win = i+1
                break

        return last_win - first_win

    def concat(self, nums: list) -> int:
        """
        Treat an array of numbers as a single big number, as though the digits were concatenated

        :param nums: The numbers to concatenate
        :type nums: list
        :return: The final number after concatenation
        :rtype: int
        """
        s: str = ''.join(str(num) for num in nums)
        return int(s)

    def part_one(self) -> int:
        """
        Find all of the numbers of ways to win each race, and multiple these numbers together
        """
        result: int = 1
        for time, distance in zip(self.times, self.distances):
            ways_to_win: int = self.calculate_ways_to_win(time, distance)
            result *= ways_to_win

        return result

    def part_two(self) -> int:
        """
        Find the number of ways to win if the times and distances were actually just one big(ger) number
        """
        actual_time: int = self.concat(self.times)
        actual_distance: int = self.concat(self.distances)

        return self.calculate_ways_to_win(actual_time, actual_distance)

def main() -> None:
    """
    Main
    """
    solver = Day06()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
