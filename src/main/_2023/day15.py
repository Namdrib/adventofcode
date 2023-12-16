#!/usr/bin/python3
import sys

class Day15:
    """
    Solution for https://adventofcode.com/2023/day/15
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.initialisation_sequence: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, the input is single line of comma-separated instructions
        """
        self.input = sys.stdin.read()

        self.initialisation_sequence = self.input.strip().split(',')

    def do_hash(self, string: str) -> int:
        """
        The HASH algorithm is a way to turn any string of characters into a single number in the range 0 to 255.
        To run the HASH algorithm on a string, start with a current value of 0.
        Then, for each character in the string starting from the beginning:
            - Determine the ASCII code for the current character of the string.
            - Increase the current value by the ASCII code you just determined.
            - Set the current value to itself multiplied by 17.
            - Set the current value to the remainder of dividing itself by 256.

        :param string: The string to hash
        :type string: str
        :return: hash value of the string
        :rtype: int
        """
        current_value: int = 0

        for char in string:
            ascii_code = ord(char)
            current_value += ascii_code
            current_value *= 17
            current_value %= 256

        return current_value

    def label_in_box(self, label: str, box: list) -> bool:
        """
        Return whether a given label is in a box

        :param label: The label to look for
        :type label: str
        :param box: The box to search, where each element is (label, focal_length)
        :type box: list
        :return: True if the label is in the box, False otherwise
        :rtype: bool
        """
        return label in [x[0] for x in box if x]

    def apply_step(self, box: list, step: str) -> None:
        if '=' in step:
            # Insert or replace a lens with the given label
            label, focal_length = step.split('=')
            focal_length = int(focal_length)

            if self.label_in_box(label, box):
                # Update the current lens with the new focal length
                for i, lens in enumerate(box):
                    if lens[0] == label:
                        box[i] = (label, focal_length)
            else:
                # Insert the lens at the end of the box
                box.append((label, focal_length))

        else:
            # Remove the lens with the given label
            label = step.strip('-')
            lens_to_remove = [lens for lens in box if lens[0] == label]

            # We can only index lens_to_remove if there was anything there
            if lens_to_remove:
                lens_to_remove = lens_to_remove[0]

            # Remove the lens from the box
            if lens_to_remove in box:
                box.remove(lens_to_remove)

    def calculate_total_focussing_power(self, boxes: list) -> int:
        """
        Find the total focusing power of all lens in all boxes
        The focussing power of a single lens is the result of multiplying together:
        - One plus the box number of the lens in question.
        - The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and so on.
        - The focal length of the lens.

        :param boxes: The boxes containing lenses
        :type boxes: list
        :return: The total focussing power of all lenses in all boxes
        :rtype: int
        """
        total_focussing_power: int = 0

        for i, box in enumerate(boxes):
            for slot_number, lens in enumerate(box):
                fp_individual: int = (i+1) * (slot_number+1) * lens[1]
                # print(f'{lens[0]}: {i+1} (box {i}) * {slot_number+1} * {lens[1]} (focal length) = {fp_individual}')
                total_focussing_power += fp_individual

        return total_focussing_power

    def part_one(self) -> int:
        """
        Find the sum of the hash of every step in the initialisation sequence
        """
        return sum(self.do_hash(x) for x in self.initialisation_sequence)

    def part_two(self) -> int:
        """
        Find the total load on the north support beams after 1000000000 spin cycles
        See: do_spin_cycle(grid)
        """
        # Each element is a list of (label, focal length)
        # It is a list because the order matters
        # All boxes start empty
        boxes: list = [[] for i in range(256)]

        # Execute the step defined in each part of the initialisation sequence
        for step in self.initialisation_sequence:
            # Determine which box is being operated on
            label = step.split('=')[0] if '=' in step else step.strip('-')
            box_num: int = self.do_hash(label)
            box: list = boxes[box_num]

            # Apply the step on the given box
            self.apply_step(box, step)

            # print(f'After "{step}":')
            # for i, box in enumerate(boxes):
            #     if box:
            #         print(f'Box {i}:', [x for x in box])
            # print()

        return self.calculate_total_focussing_power(boxes)

def main() -> None:
    """
    Main
    """
    solver = Day15()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
