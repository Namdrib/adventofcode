#!/usr/bin/python3
import sys

class Day01:
    """
    Solution for https://adventofcode.com/2024/day/1
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.left: list = []
        self.right: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line is a pair of numbers separated by whitespace
        """
        raw_input = sys.stdin.read()

        self.input = raw_input.splitlines()

        for item in self.input:
            left, right = item.split()
            self.left.append(int(left))
            self.right.append(int(right))

    def part_one(self) -> int:
        """
        Pair up the smallest number in each list, and the second-smallest
        number in each list, and so on.
        Return the sum of differences between each of these pairs
        """
        total: int = 0
        for left, right in zip(sorted(self.left), sorted(self.right)):
            diff = abs(left - right)
            total += diff
        return total

    def part_two(self) -> int:
        """
        A number's similarity score is its value multiplied by how many times it
        appears in the other list.
        Return the sum of the similarity scores of the numbers in the left list.
        """
        total: int = 0
        for l in self.left:
            similarity_score = l * self.right.count(l)
            total += similarity_score
        return total

def main() -> None:
    """
    Main
    """
    solver = Day01()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
