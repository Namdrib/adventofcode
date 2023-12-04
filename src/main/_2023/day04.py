#!/usr/bin/python3
import sys

class Card:
    def __init__(self, id_: int, winning_numbers: list, have_numbers: list):
        self.id = id_
        self.winning_numbers = winning_numbers
        self.have_numbers = have_numbers

    def num_winning_numbers(self) -> int:
        """
        The number of numbers we have that are also winning numbers

        :return: the number of winning numbers that overlap
        :rtype: int
        """
        return len(set(self.have_numbers).intersection(self.winning_numbers))

    def calculate_score(self) -> bool:
        """
        The score is defined as 1 for the first match, then doubled for each of the matches after the first

        :return: The score of a given card
        :rtype: int
        """
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
        You win copies of the scratchcards below the winning card equal to the number of matches.
        So, if card 10 were to have 5 matching numbers, you would win one copy each of cards 11, 12, 13, 14, and 15.
        """
        # Keep track of how many cards we have
        # Start with one of each, as we'll go through the entire list
        card_stash: dict = {card.id: 1 for card in self.cards}

        # As each card wins more cards, add those upcoming cards to the stash
        for card in self.cards:
            num_winning_numbers: int = card.num_winning_numbers()
            for j in range(num_winning_numbers):
                if card.id+j < len(self.cards):
                    card_stash[card.id+j+1] += card_stash[card.id]

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
