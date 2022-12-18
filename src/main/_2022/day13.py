#!/usr/bin/python3
from ast import literal_eval
from functools import cmp_to_key
import sys

class Day13:
    """
    Solution for https://adventofcode.com/2022/day/13
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.packets: list = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line is either a packet or empty
        The lines are grouped into pairs of packets with empty lines in between
        <packet>
        <packet>
        <blank>
        ...
        """
        raw_input = sys.stdin.read()

        self.input = raw_input.split('\n')
        self.input = self.input[0:-1]

        self.packets = []
        for item in self.input:
            if item:
                self.packets.append(literal_eval(item))

    def elements_in_order(self, a, b, depth: int=0, debug: bool=False) -> bool:
        """
        A lower-level implementation of in_correct_order
        Deals with a single list or number
        Depth is only used for debug outputs
        Return True if a < b
        False if a > b
        None if they are equal
        Recurse if they are lists
        """
        # Used for debug outputs
        indent: str = '  '*depth

        if debug:
            print(f'{indent}- Compare {a} vs {b}')

        # They are both ints - check for inequality
        # Equality is inconclusive
        if isinstance(a, int) and isinstance(b, int):
            if a < b:
                if debug:
                    print(f'{indent}- Left side is smaller, so inputs are in the right order')
                return True
            if a > b:
                if debug:
                    print(f'{indent}- Right side is smaller, so inputs are NOT in the right order')
                return False

            # They are equal
            return None

        # Exactly one is an int and one is a list - convert the int to a list
        if isinstance(a, int):
            if debug:
                print(f'{indent}- Mixed types; convert left to {a} and retry comparison')
            a = [a]
        if isinstance(b, int):
            if debug:
                print(f'{indent}- Mixed types; convert right to {b} and retry comparison')
            b = [b]

        # To compare two lists, compare their elements
        for left, right in zip(a, b):
            result = self.elements_in_order(left, right, depth+1, debug)
            if result is not None:
                return result

        if len(a) > len(b):
            if debug:
                print(f'{indent}- Right side ran out of items, *not* right order')
            return False

        if len(a) < len(b):
            if debug:
                print(f'{indent}- Left side ran out of items - *right order*')
            return True

        return None

    def packet_in_correct_order(self, a, b) -> bool:
        """
        a and b are packets
        packets are lists or ints (may be nested)
        Return -1 if a < b
        Return 1 if a > b
        This can be used as a comparator
        """
        res = self.elements_in_order(a, b, depth=0, debug=False)
        return -1 if res else 1

    def part_one(self) -> int:
        """
        Return the sum of the indices of the pairs that are in order
        """
        sum_of_indices_of_in_order_pairs: int = 0
        for i in range(0, len(self.packets), 2):
            if self.packet_in_correct_order(self.packets[i], self.packets[i+1]) == -1:
                # Because we want the index of the pair, rather than of the packet
                # we need to divide by 2
                sum_of_indices_of_in_order_pairs += (int(i/2)+1)

        return sum_of_indices_of_in_order_pairs

    def part_two(self) -> int:
        """
        Add two decoder packets '[[2]]' and '[[6]]' to the packets
        Sort all of the packets
        Return the product of the indices of the decoder packets
        """
        markers: list = [[[2]], [[6]]]
        self.packets.extend(markers)

        # Sort the packets according to the comprator
        sorted_packets = sorted(self.packets, key=cmp_to_key(self.packet_in_correct_order))

        # Find the indices of the marker packets
        marker_index_product: int = 1
        for i, item in enumerate(sorted_packets):
            if item in markers:
                marker_index_product *= (i+1)
        return marker_index_product

def main() -> None:
    """
    Main
    """
    solver = Day13()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
