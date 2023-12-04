#!/usr/bin/python3
import re
import sys

class Card:
    def __init__(self, id_: int, winning_numbers: list, have_numbers: list):
        self.id = id_
        self.winning_numbers = winning_numbers
        self.have_numbers = have_numbers

    def num_winning_numbers(self):
        return len(set(self.have_numbers).intersection(self.winning_numbers))

    def calculate_score(self):
        wn: int = self.num_winning_numbers()
        if not wn:
            return 0

        exponent: int = wn - 1
        return 2**exponent

class Day04:
    """
    Solution for https://adventofcode.com/2023/day/4
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = []

        self.cards: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line contains a game with a number of samples with numbers of coloured cubes
        """
        self.input = sys.stdin.read()

        for line in self.input.splitlines(keepends=False):
            # Each line looks like:
            # Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
            print(f'Reading {line}')
            id_, rest = line.split(': ')
            _, id_ = id_.split(' ', 1)

            left, right = rest.split(' | ')
            winning_numbers: list = left.split()
            have_numbers: list = right.split()

            self.cards.append(Card(int(id_), winning_numbers, have_numbers))

    def part_one(self) -> int:
        """
        Return the sum of the points on each scratchcard
        """
        return sum(x.calculate_score() for x in self.cards)

    def part_two(self) -> int:
        """
        Return the number of scratchcards you end up with with the new scoring mechanism
        """
        card_stash: dict = {} # id: number of copies
        for card in self.cards:
            card_stash[card.id] = 1

        # For each card
        for i, card in enumerate(self.cards):
            num_winning_numbers: int = card.num_winning_numbers()
            for j in range(num_winning_numbers):
                if i+j+1 < len(self.cards):
                    card_stash[i+j+2] += card_stash[i+1]

        return sum(v for k, v in card_stash.items())

def main() -> None:
    """
    Main
    """
    solver = Day04()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
