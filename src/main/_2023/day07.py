#!/usr/bin/python3
from enum import Enum
from functools import cmp_to_key
from math import prod
import sys

class Hand:
    def __init__(self, cards: str, bid: int):
        self.cards: str = cards
        self.bid: int = bid

    def __repr__(self) -> str:
        return f'Hand(\'{self.cards=}\', {str(self.bid).rjust(3)})'

class HandType(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

class Day07:
    """
    Solution for https://adventofcode.com/2023/day/7
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.hands: list = []

        # Cards in strength order, with the weakest on the left
        # This way we can use str.find() to get the index as a comparator
        self.card_strength_order: str = '23456789TJQKA'

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line contains a hand of Camel Cards and a bid
        """
        self.input = sys.stdin.read()

        for line in self.input.splitlines(keepends=False):
            hand, bid = line.split()
            h = Hand(hand, int(bid))
            self.hands.append(h)

    def get_hand_type(self, cards: str) -> HandType:
        """
        Return the type of the given hand

        :param cards: The cards to evaluate
        :type cards: str
        :return: The type of the hand
        :rtype: HandType
        """
        unique_cards: set = set(cards)
        sorted_hand: list = sorted(cards)
        if len(unique_cards) == 1:
            return HandType.FIVE_OF_A_KIND
        if len(unique_cards) == 2:
            # Full house or four or a kind
            if sorted_hand[0] == sorted_hand[3] or sorted_hand[1] == sorted_hand[4]:
                return HandType.FOUR_OF_A_KIND
            return HandType.FULL_HOUSE
        if len(unique_cards) == 3:
            # Two pair or three of a kind
            if sorted_hand[0] == sorted_hand[2] or sorted_hand[1] == sorted_hand[3] or sorted_hand[2] == sorted_hand[4]:
                return HandType.THREE_OF_A_KIND
            return HandType.TWO_PAIR
        if len(unique_cards) == 4:
            return HandType.ONE_PAIR
        return HandType.HIGH_CARD

    def compare_cards(self, card_1: str, card_2: str) -> int:
        """
        Return a comparison result of two cards, `card_1` and `card_2`

        :param card_1: A card to compare
        :type card_1: str
        :param card_2: Another card to compare
        :type card_2: str
        :return: -1 if card_1 is less than card_2, 1 if it is stronger, or 0 if they are equal
        :rtype: int
        """
        # Find how early the card is in the strength order
        # Earlier cards are weaker
        card_1_strength: int = self.card_strength_order.find(card_1)
        card_2_strength: int = self.card_strength_order.find(card_2)

        if card_1_strength < card_2_strength:
            return -1
        if card_1_strength > card_2_strength:
            return 1
        return 0

    def compare_hands(self, hand_1: Hand, hand_2: Hand) -> int:
        """
        Return a comparison result of two Hands, `hand_1` and `hand_2`

        :param hand_1: A hand to compare
        :type hand_1: str
        :param hand_2: Another hand to compare
        :type hand_2: str
        :return: -1 if hand_1 is less than hand_2, 1 if it is stronger, or 0 if they are equal
        :rtype: int
        """
        cards_1: str = hand_1.cards
        cards_2: str = hand_2.cards

        # Get the HandType and compare them
        hand_type_1: HandType = self.get_hand_type(cards_1)
        hand_type_2: HandType = self.get_hand_type(cards_2)
        if hand_type_1.value < hand_type_2.value:
            return -1
        if hand_type_1.value > hand_type_2.value:
            return 1

        # If the HandTypes were the same, look at the individual cards in order
        for card_1, card_2 in zip(cards_1, cards_2):
            compare_card_result: int = self.compare_cards(card_1, card_2)
            # If they are different, return the result
            # Otherwise, compare the next card in the hand
            if compare_card_result != 0:
                return compare_card_result

        # This shouldn't happen, but in case everything is equal, then the hands are equal
        return 0

    def part_one(self) -> int:
        """
        A hand's rank is 1 for the weakest hand, 2 for the second-weakest, ...
        A hand's winnings is its bid multiplied by its rank
        Find the total winnings of all the hands
        """
        sorted_hands = sorted(self.hands, key=cmp_to_key(self.compare_hands))
        for hand in sorted_hands:
            print(f'{hand} -> {self.get_hand_type(hand.cards)}')

        total_winnings: int = 0
        for i, hand in enumerate(sorted_hands, 1):
            total_winnings += hand.bid * i

        return total_winnings

    def part_two(self) -> int:
        """
        Js are now Jokers instead of Jacks. Jokers are wildcard cards, which are weak (< 2), but can act as any other card.
        Find the total winnings of all the hands with the Js as Jokers
        """
        return 0


def main() -> None:
    """
    Main
    """
    solver = Day07()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
