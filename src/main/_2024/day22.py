#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

class Day22:
    """
    Solution for https://adventofcode.com/2024/day/22
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.initial_numbers: list = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line is a starting secret number
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.initial_numbers: list = list(map(int, self.input))

    def mix(self, num: int, mixer: int) -> int:
        """
        To mix a value into the secret number, calculate the bitwise XOR of the
        given value and the secret number.
        Then, the secret number becomes the result of that operation.
        (If the secret number is 42 and you were to mix 15 into the secret
        number, the secret number would become 37.)

        :param num: The secret number
        :type num: int
        :param mixer: The number to mix into the secret number
        :type mixer: int
        :return: The value of the secret number after mixing
        :rtype: int
        """
        return num ^ mixer

    def prune(self, num: int) -> int:
        """
        To prune the secret number, calculate the value of the secret number
        modulo 16777216.
        Then, the secret number becomes the result of that operation.
        (If the secret number is 100000000 and you were to prune the secret
        number, the secret number would become 16113920.)

        :param num: The number to prune
        :type num: int
        :return: The number after pruning
        :rtype: int
        """
        return num % 16777216

    def next_secret_number(self, num: int) -> int:
        """
        Perform steps to generate the next iteration of a secret number
        Calculate the result of multiplying the secret number by 64.
        Then, mix this result into the secret number.
        Finally, prune the secret number.

        Calculate the result of dividing the secret number by 32.
        Round the result down to the nearest integer.
        Then, mix this result into the secret number.
        Finally, prune the secret number.

        Calculate the result of multiplying the secret number by 2048.
        Then, mix this result into the secret number.
        Finally, prune the secret number.


        :param num: The secret number to do stuff to
        :type num: int
        :return: The next iteration of the secret number, according to the steps
        :rtype: int
        """
        # Step 1
        mult: int = num * 64
        num = self.mix(num, mult)
        num = self.prune(num)

        # Step 2
        div: int = int(num / 32)
        num = self.mix(num, div)
        num = self.prune(num)

        # Step 3
        mult: int = num * 2048
        num = self.mix(num, mult)
        num = self.prune(num)

        return num

    def generate_buying_schedule(self, num: int, n: int) -> list:
        """
        Determine a buyer's buying schedule based on their initial secret number

        A single line in the buying schedule looks consists of three numbers:
        1. The current secret number
        2. The last digit of the secret number
        3. The difference between the last digit of the secret number, and the
        last digit of the previous secret number

        The first 3. is always 0, as there is no difference at the beginning

        :param num: The secret number to seed the buying schedule
        :type num: int
        :param n: How many items are in the buying schedule
        :type n: int
        :return: The full buying schedule of this buyer
        :rtype: list
        """
        out: list = [(num, num%10, 0)]

        for _ in range(n):
            num = self.next_secret_number(num)
            last_digit: int = num % 10
            previous_price: int = out[-1][1]
            diff: int = last_digit - previous_price

            out.append((num, last_digit, diff))

        return out

    def calculate_sequence_returns(self, buying_schedules: dict, window_size: int = 4) -> dict:
        """
        From a given set of buying schedules, work out all of the possible price
        change sequences, and how much each buyer would buy for when that price
        change sequence happens.

        :param buying_schedules: {buyer: buying schedule}
        :type buying_schedules: dict
        :param window_size: The length of the sliding window
        :type window_size: int
        :return: The return of each sliding window for each buyer
        :rtype: dict
        """
        # {change_sequence: {buyer: bananas}}
        # We don't know all of the keys (change sequences) yet, so the inner
        # dicts can't be initialised with placeholder values yet
        sliding_window_returns: dict = {}

        for buyer, schedule in buying_schedules.items():

            # Every position of a sliding window of size window_size
            for i in range(len(schedule) - window_size + 1):
                # Look for the price change sequence
                price_change_seq: tuple = tuple(x[2] for x in schedule[i:i+window_size])

                # Initialise so we don't get a KeyError
                if price_change_seq not in sliding_window_returns:
                    sliding_window_returns[price_change_seq] = {}

                # The selling price of the previous item in the schedule
                buying_price = schedule[i+window_size-1][1]

                # The buyer sells the first time the change sequence happens
                if buyer in sliding_window_returns[price_change_seq]:
                    continue

                # Track how much each price change sequence gives
                sliding_window_returns[price_change_seq][buyer] = buying_price

        return sliding_window_returns

    def part_one(self) -> int:
        """
        Return the sum of the 2000th secret number of each buyer
        """
        return sum(
            # The last secret number
            self.generate_buying_schedule(n, 2000)[-1][0]
            # Of each buyer, given their initial number
            for n in self.initial_numbers
        )

    def part_two(self) -> int:
        """
        Return the most bananas we could buy with a change sequence of 4
        """
        # Calculate the buying schedule for each buyer
        buying_schedules: dict = {n: self.generate_buying_schedule(n, 2000) for n in self.initial_numbers}

        # Calculate the potential earnings for each change sequence
        # This does most of the heavy lifting for this part
        sequence_returns: dict = self.calculate_sequence_returns(buying_schedules)

        return max(
            # The number of bananas we would get from the buying schedule
            sum(buyer_prices.values())
            for buyer_prices in sequence_returns.values()
        )

def main() -> None:
    """
    Main
    """
    solver = Day22()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
