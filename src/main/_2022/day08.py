#!/usr/bin/python3
import sys

class Day08:
    """
    Solution for https://adventofcode.com/2022/day/8
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self._input: list = None

        self._trees: list = []

        self._visibility: list = []
        self._scenic_score: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each character in a grid is the height of a tree
        """
        raw_input = sys.stdin.read()

        self._input = raw_input.split('\n')
        self._input = self._input[0:-1]

        for item in self._input:
            row = [int(x) for x in item]
            self._trees.append(row)

    def update_visibility(self):
        """
        Calculate the visibility and scenic score of each tree
        The the visibility is True if the tree can be seen from any of the edges, False otherwise
        The scenic score is the product of the tree's viewing distance in each direction
        The viewing distance is how many other trees the tree can see
        """
        # For each position, see if it is visible from the edge
        # Start off assuming none of them are visible
        # Visibility is whether the given tree is visible from any edges
        self._visibility = []
        for item in self._trees:
            row: list = [False for x in item]
            self._visibility.append(row)

        # Scenic score is the product of how many trees can be seen in each direction
        # A tree on an edge will have at least one direction be zero
        self._scenic_score = []
        for item in self._trees:
            row: list = [1 for x in item]
            self._scenic_score.append(row)

        # For each tree
        for i, row in enumerate(self._trees):
            for j, tree_height in enumerate(row):
                # Look in each direction until we can see no further

                # Check visibility from the left
                visibility_left: bool = True
                viewing_distance_left: int = 0
                for k in range(j-1, -1, -1):
                    viewing_distance_left += 1
                    if tree_height <= self._trees[i][k]:
                        visibility_left = False
                        break

                # Check visibility from the right
                visibility_right: bool = True
                viewing_distance_right: int = 0
                for k in range(j+1, len(self._trees[i])):
                    viewing_distance_right += 1
                    if tree_height <= self._trees[i][k]:
                        visibility_right = False
                        break

                # Check visibility from above
                visibility_above: bool = True
                viewing_distance_above: int = 0
                for k in range(i-1, -1, -1):
                    viewing_distance_above += 1
                    if tree_height <= self._trees[k][j]:
                        visibility_above = False
                        break

                # Check visibility from below
                visibility_below: bool = True
                viewing_distance_below: int = 0
                for k in range(i+1, len(self._trees)):
                    viewing_distance_below += 1
                    if tree_height <= self._trees[k][j]:
                        visibility_below = False
                        break

                # Get the final verdict on whether the tree is visible
                self._visibility[i][j] = visibility_left or visibility_right or visibility_below or visibility_above

                # Set the final scenic score
                self._scenic_score[i][j] = viewing_distance_left * viewing_distance_right * viewing_distance_above * viewing_distance_below

    def part_one(self) -> int:
        """
        Return the number of trees that are visible from outside
        """
        self.update_visibility()

        num_visible: int = 0
        for item in self._visibility:
            num_visible += sum(item)
        return num_visible

    def part_two(self) -> int:
        """
        Return the highest scenic score of all the trees
        """
        max_scenic_score: int = 0
        for item in self._scenic_score:
            max_scenic_score = max(max_scenic_score, max(item))
        return max_scenic_score

def main() -> None:
    """
    Main
    """
    solver = Day08()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
