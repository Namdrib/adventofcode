#!/usr/bin/python3
import copy
import functools
from operator import mul
import os
import re
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Day14:
    """
    Solution for https://adventofcode.com/2024/day/14
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.robots: list = None

        # Fixed size of the map
        self.x = 101
        self.y = 103

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line is of the format:
        p=X,Y v=X,Y

        Where the p X and Y are always positive, and the v X and Y may be negative
        This represents the XY position of a robot, and the XY velocity of the robot
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.robots = []
        for item in self.input:
            px, py, vx, vy = list(map(int, re.findall(r'-?\d+', item)))
            self.robots.append([px, py, vx, vy])

    def step(self, robots: list, n: int = 1) -> None:
        """
        Move each robot by its velocity

        Passing n will move it n times

        :param robots: The robots to move
        :type robots: list
        :param n: How many times to move the robot, defaults to 1
        :type n: int, optional
        """

        for robot in robots:
            robot[0] += robot[2] * n
            robot[1] += robot[3] * n

            # Handle wrapping
            if robot[0] < 0:
                robot[0] += self.x
            if robot[1] < 0:
                robot[1] += self.y
            robot[0] = robot[0] % self.x
            robot[1] = robot[1] % self.y

    def plot_robots(self, robots: list) -> list:
        """
        Return a list of strings representing the 2D grid of the robot
        positions. Robots are marked with an X, empty space with a .

        Each element of the list is a row

        :param robots: The robots to plot
        :type robots: list
        :return: A list of strings representing the grid
        :rtype: list
        """
        # 2D grid of .
        out: list = []
        for _ in range(self.y):
            out.append(['.' for _ in range(self.x)])

        # Populate the robots. We don't care how many robots there are
        for robot in robots:
            out[robot[1]][robot[0]] = 'X'

        return out

    def calculate_safety_factor(self, robots: list) -> int:
        """
        Count how many robots are in each quadrant of the grid (given by self.x
        and self.y).
        Robots on a quadrant boudnary do not count
        The safety factor of the robots is given by multiplying the number of
        robots in each quadrant

        :param robots: The robots to calculate the safety factor for
        :type robots: list
        :return: The safety factor
        :rtype: int
        """
        # NW, NE, SW, SE
        quad_counts: list = [0, 0, 0, 0]

        for robot in robots:
            if robot[0] < self.x/2-1:
                # NW
                if robot[1] < self.y/2-1:
                    quad_counts[0] += 1
                # SW
                elif robot[1] > self.y/2:
                    quad_counts[2] += 1
            elif robot[0] > self.x/2:
                # NE
                if robot[1] < self.y/2-1:
                    quad_counts[1] += 1
                # SE
                elif robot[1] > self.y/2:
                    quad_counts[3] += 1

        return functools.reduce(mul, quad_counts, 1)

    def is_xmas_tree(self, plot: list) -> bool:
        """
        An approximate guess what what the Christmas tree would look like
        
        Surely there's at least one straight line

        :param robots: The position of the robots
        :type robots: list
        :return: True if the robots are in the shape of a Christmas tree, False otherwise
        :rtype: bool
        """
        return any('XXXXXXXXXXXXXXXXXX' in ''.join(x) for x in plot)

    def part_one(self) -> int:
        """
        Return the safety factor of the robots after 100 steps
        """
        temp_robots: list = copy.deepcopy(self.robots)
        self.step(temp_robots, 100)

        safety_factor: int = self.calculate_safety_factor(temp_robots)
        return safety_factor

    def part_two(self) -> int:
        """
        Return the how many steps are required until the robots arrange
        themselves into the pattern of a Christmas tree
        """
        count: int = 0

        temp_robots: list = copy.deepcopy(self.robots)

        # Keep moving the robots until they arrange themselves into a Christmas
        # tree pattern
        # When it happens, print the grid and return how many seconds has passed
        while True:
            self.step(temp_robots)
            count += 1

            plot: list = self.plot_robots(temp_robots)
            if self.is_xmas_tree(plot):
                for line in plot:
                    print(''.join(line))
                break

        return count

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
