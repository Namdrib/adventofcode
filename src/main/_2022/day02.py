#!/usr/bin/python3
import sys

class day02:

    def __init__(self) -> None:
        self._input: list = None

        self._shape_value: dict = {
            'X': 1,
            'Y': 2,
            'Z': 3
        }

        return

    def read_input(self) -> None:
        raw_input = sys.stdin.read()

        self._input = raw_input.split('\n')
        self._input = self._input[0:-1]

    def _score_round(self, opp_shape: str, my_shape: str) -> int:
        # Return my score for a round
        # Loss: 0
        # Draw: 3
        # Win: 6
        # Plus the score of whatever shape I threw
        score = 0

        # Determine the outcome of the round
        if (opp_shape == 'A' and my_shape == 'X') or (opp_shape == 'B' and my_shape == 'Y') or (opp_shape == 'C' and my_shape == 'Z'):
            # Draw
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
        # Play a round, returning the score
        opponent_move, my_move = moves.split()

        score: int = self._score_round(opponent_move, my_move)
        return score

    def _determine_shape_for_outcome(self, opp_shape: str, desired_outcome: str) -> str:
        # Given the opponent's shape and the desired round outcome,
        # determine what shape I need to throw to achieve that outcome
        # e.g. if opp_shape is 'A' and I want a draw, I need to throw 'X'

        # Outcomes:
        # 'X': lose
        # 'Y': draw
        # 'Z': win

        # Kinda gross...
        if opp_shape == 'A':
            if desired_outcome == 'X':
                return 'Z'
            elif desired_outcome == 'Y':
                return 'X'
            else:
                return 'Y'
        elif opp_shape == 'B':
            if desired_outcome == 'X':
                return 'X'
            elif desired_outcome == 'Y':
                return 'Y'
            else:
                return 'Z'
        else:
            if desired_outcome == 'X':
                return 'Y'
            elif desired_outcome == 'Y':
                return 'Z'
            else:
                return 'X'

    def part_one(self) -> int:
        # The score assuming perfect play
        total_score: int = 0
        for item in self._input:
            round_score = self._play_round(item)
            total_score += round_score

        return total_score

    def part_two(self) -> int:
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
    solver = day02()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()

