#!/usr/bin/python3
import sys

class Day02:
    """
    Solution for https://adventofcode.com/2022/day/2
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self._input: list = None

        self._shape_value: dict = {
            'X': 1,
            'Y': 2,
            'Z': 3
        }

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line contains two characters separated by a space
        The first character is one if [ABC], and the second is one of [XYZ]
        """
        raw_input = sys.stdin.read()

        self._input = raw_input.split('\n')
        self._input = self._input[0:-1]

    def _score_round(self, opp_shape: str, my_shape: str) -> int:
        """
        Return my score for a round as follows:
        Loss: 0
        Draw: 3
        Win: 6

        Plus the score of whatever shape I threw:
        X: 1
        Y: 2
        Z: 3
        """
        score = 0

        # Determine the outcome of the round
        if ord(my_shape) - ord(opp_shape) == 23:
            # Draw (AX, BY or CZ)
            score += 3
        elif (opp_shape == 'A' and my_shape == 'Y') or (opp_shape == 'B' and my_shape == 'Z') or (opp_shape == 'C' and my_shape == 'X'):
            # I win
            score += 6
        else:
            # I lose
            score += 0

        # My shape's value
        score += self._shape_value[my_shape]
        return score

    def _play_round(self, moves: int) -> int:
        """
        Play a round and return the score
        """
        # Play a round, returning the score
        opponent_move, my_move = moves.split()

        score: int = self._score_round(opponent_move, my_move)
        return score

    def _determine_shape_for_outcome(self, opp_shape: str, desired_outcome: str) -> str:
        """
        Given the opponent's shape and the desired round outcome,
        determine what shape I need to throw to achieve that outcome
        e.g. if opp_shape is 'A' and I want a draw, I need to throw 'X'
        """

        # Outcomes:
        # 'X': lose
        # 'Y': draw
        # 'Z': win

        my_throw: str = ''

        # Kinda gross...
        # Rock
        if opp_shape == 'A':
            if desired_outcome == 'X':
                my_throw = 'Z'
            elif desired_outcome == 'Y':
                my_throw = 'X'
            else:
                my_throw = 'Y'

        # Paper
        elif opp_shape == 'B':
            if desired_outcome == 'X':
                my_throw = 'X'
            elif desired_outcome == 'Y':
                my_throw = 'Y'
            else:
                my_throw = 'Z'

        # Scissors
        elif opp_shape == 'C':
            if desired_outcome == 'X':
                my_throw = 'Y'
            elif desired_outcome == 'Y':
                my_throw = 'Z'
            else:
                my_throw = 'X'

        return my_throw

    def part_one(self) -> int:
        """
        Return the score assuming the [XYZ] correspond to moves for perfect play
        """
        total_score: int = 0
        for item in self._input:
            round_score = self._play_round(item)
            total_score += round_score

        return total_score

    def part_two(self) -> int:
        """
        Return the score assuming the [XYZ] correspond to desired outcomes
        """
        total_score: int = 0
        for item in self._input:
            opp_shape, desired_outcome = item.split()

            # Figure out what shape I need to play
            my_shape: str = self._determine_shape_for_outcome(opp_shape, desired_outcome)

            # Then play that round and score it
            round_to_play: str = f'{opp_shape} {my_shape}'
            round_score = self._play_round(round_to_play)

            total_score += round_score

        return total_score

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
