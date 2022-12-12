#!/usr/bin/python3
import sys

from Coord import Coord2D

class Day09:
    """
    Solution for https://adventofcode.com/2022/day/9
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self._input: list = None

        self._instructions: list = []

        # The number of times the tail has visited each location
        self._tail_visited: dict = {}

        # A list of Coord2Ds for each segment of the body
        self._body: list = []

        # All of the valid directions
        self._valid_directions: set = ('U', 'D', 'L', 'R')

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line is a direction followed by a number of steps
        """
        raw_input = sys.stdin.read()

        self._input = raw_input.split('\n')
        self._input = self._input[0:-1]

        for line in self._input:
            direction, steps = line.split()
            self._instructions.append((direction, int(steps)))

    def set_body_size(self, length: int) -> None:
        """
        Initialise a new body with size n
        Reset the places the tail has visited
        """
        self._body = [Coord2D(0, 0) for _ in range(length)]
        self._tail_visited = set()
        self.record_tail_location()

    def move_head(self, direction: str) -> None:
        """
        Move head in the given direction by one step
        This drags the next segment towards us if we get too far away
        """
        if direction not in self._valid_directions:
            print(f'{direction} is not a valid direction ({self._valid_directions})')
            return

        # Move the head
        if direction == 'U':
            self._body[0].y += 1
        elif direction == 'D':
            self._body[0].y -= 1
        elif direction == 'L':
            self._body[0].x -= 1
        elif direction == 'R':
            self._body[0].x += 1

        self.drag_segment(1)

    def drag_segment(self, my_pos: int) -> None:
        """
        Move the given body part towards its previous connection if it is no longer touching
        """
        parent_pos: Coord2D = self._body[my_pos-1]
        x_distance: int = abs(self._body[my_pos].x - parent_pos.x)
        y_distance: int = abs(self._body[my_pos].y - parent_pos.y)
        distance: int = x_distance + y_distance

        if x_distance <= 1 and y_distance <= 1:
            # we are adjacent to the previous part
            # no move movement required
            # because we're not moving, no other part has to either
            return

        # Calculate how we move in relation to where the parent is
        # If the parent is an L shape away from us, we move diagonally towards them
        x_change: int = 0
        y_change: int = 0
        if x_distance > 1 or distance > 2:
            if self._body[my_pos].x < parent_pos.x:
                x_change = 1
            else:
                x_change = -1

        if y_distance > 1 or distance > 2:
            if self._body[my_pos].y < parent_pos.y:
                y_change = 1
            else:
                y_change = -1

        # Apply the movement to the current segment
        self._body[my_pos].x += x_change
        self._body[my_pos].y += y_change

        # Record the tail location if we are the tail
        # Otherwise drag the next segment towards us
        if my_pos == len(self._body)-1:
            self.record_tail_location()
        else:
            self.drag_segment(my_pos+1)

    def record_tail_location(self) -> None:
        """
        Record where the tail is
        """
        tail_copy = Coord2D(self._body[-1].x, self._body[-1].y)
        self._tail_visited.add(tail_copy)

    def run_instructions(self) -> None:
        """
        Run through all the instructions, applying the moves
        """
        for item in self._instructions:
            for _ in range(item[1]):
                self.move_head(item[0])

    def part_one(self) -> int:
        """
        Return the number of spaces the tail visits for a body of length 2
        """
        self.set_body_size(2)
        self.run_instructions()
        return len(self._tail_visited)

    def part_two(self) -> int:
        """
        Return the number of spaces the tail visits for a body of length 10
        """
        self.set_body_size(10)
        self.run_instructions()
        return len(self._tail_visited)

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
