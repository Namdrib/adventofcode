#!/usr/bin/python3
import sys

class Day10:
    """
    Solution for https://adventofcode.com/2022/day/10
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self._input: list = None

        # How many execution cycles have passed
        self._cycles: int = 0

        self._instructions: list = []

        # The X register. Also the sprite position
        self._x: int = 1

        # Used for part 1 only
        # Used to calculalte the signal strength at the 20th cycle, and every 40th after that
        self._signal_calculation_start: int = 20
        self._signal_calculation_interval: int = 40
        self._signal_strength_sum: int = 0

        # Used for part 2 only
        # The CRT display is a grid of pixels, either lit (#) or dark (.)
        # It starts off dark
        self._crt: list = [['.' for x in range(40)] for y in range(6)]

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line is basic CPU instruction
        """
        raw_input = sys.stdin.read()

        self._input = raw_input.split('\n')
        self._input = self._input[0:-1]

        self._instructions = self._input

    def draw_crt_pixel(self) -> None:
        """
        The X register is a position marker for a 3-character wide sprite
        It represents the middle position on the CRT
        A # pixel is drawn if the cycle number overlaps with any part of the sprite
        """
        x: int = (self._cycles-1) % len(self._crt[0])
        sprite_bounds: range = range(self._x-1, self._x+2)

        if x in sprite_bounds:
            y: int = int((self._cycles-1) / len(self._crt[0]))
            self._crt[y][x] = '#'

    def calculate_signal_strength(self) -> int:
        """
        The signal strength is the value of the X register multiplied by
        the number of cycles that have passed
        """
        return self._x * self._cycles

    def next_cycle(self) -> None:
        """
        Both the CPU and display are tied to the clock circuit's cycles
        In each cycle, a pixel may be drawn on the CRT
        """
        self._cycles += 1

        # For part 1
        # Calculate the signal strength at 20 and every multiple of 40 after that
        if self._cycles == self._signal_calculation_start \
                or self._cycles >= self._signal_calculation_start \
                and ((self._cycles - self._signal_calculation_start) % self._signal_calculation_interval == 0):
            signal_strength: int = self.calculate_signal_strength()

            self._signal_strength_sum += signal_strength

        # For part 2
        self.draw_crt_pixel()

    def execute_instruction(self, instruction: str) -> None:
        """
        Execute the given instruction
        noop: takes one cycle and does nothing
        addx: takes two cycles and adds a number to the x register
        """
        if instruction == 'noop':
            # Do nothing for one cycle
            self.next_cycle()

        elif instruction.startswith('addx'):
            # Addition takes two cycles to finish
            self.next_cycle()
            self.next_cycle()

            # Finish adding the argument to the x register
            arg: int = int(instruction.split()[1])
            self._x += arg

    def part_one(self) -> int:
        """
        Return the sum of the signal strengths at the 20th cycle and every 40th cycle after that
        """
        for item in self._instructions:
            self.execute_instruction(item)

        return self._signal_strength_sum

    def part_two(self) -> int:
        """
        Return the letters being drawn by the pixels
        This needs to be parsed by a human
        """
        for row in self._crt:
            print(''.join(row))
        return 0

def main() -> None:
    """
    Main
    """
    solver = Day10()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
