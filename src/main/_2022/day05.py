#!/usr/bin/python3
import copy
import math
import sys

class Day05:
    """
    Solution for https://adventofcode.com/2022/day/5
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self._input: list = None

        # list of lists where the inner lists will be treated as stacks
        self._stacks: list = []

        self._instructions: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()

        self._input = raw_input.split('\n')
        self._input = self._input[0:-1]

        # Find out how many stacks there are, initialise that many stacks
        for item in self._input:
            if '1' in item:
                stack_ids: str = item
                num_stacks: int = int(stack_ids.split()[-1])
                self._stacks = [[] for x in range(num_stacks)]
                break

        # Read the actual input now
        reading_stack: bool = True
        for item in self._input:
            if reading_stack:
                # Reading the containers
                if '[' in item:
                    for i, char in enumerate(item):
                        if char.isupper():
                            stack_pos = int(math.floor(i/4))
                            # Insert at the bottom since we're reading top-down
                            self._stacks[stack_pos].insert(0, char)

                else:
                    reading_stack = False
            else:
                # Reading the instructions
                if item.startswith('move'):
                    self._instructions.append(item)

    def _run_instruction(self, stacks: list, instruction: str, new_cratemover: bool=False) -> None:
        """
        Run the given instruction
        """
        # Parse the instruction
        tokens: list = instruction.split()
        num_crates_to_move: int = int(tokens[1])
        source: int = int(tokens[3])-1
        dest: int = int(tokens[5])-1

        # Move the crates
        if new_cratemover:
            # New cratemover can move multiple crates at a time
            crates_to_move: list = stacks[source][-num_crates_to_move:]
            stacks[source] = stacks[source][:-num_crates_to_move]
            stacks[dest].extend(crates_to_move)
        else:
            # Old cratemover moves crates one at a time
            for _ in range(num_crates_to_move):
                crate_id: str = stacks[source].pop()
                stacks[dest].append(crate_id)

    def get_top_of_crates(self, stacks: list) -> str:
        """
        Return a string of the top item of each stack in the list
        """
        return ''.join(map(lambda x: x[-1], stacks))

    def part_one(self) -> int:
        """
        Return the top crate of each stack after performing all instructions with the old cratemover
        """
        stack_copy: list = copy.deepcopy(self._stacks)
        for item in self._instructions:
            self._run_instruction(stack_copy, item, False)

        return self.get_top_of_crates(stack_copy)

    def part_two(self) -> str:
        """
        Return the top crate of each stack after performign all instructions with the new cratemover
        """
        stack_copy: list = copy.deepcopy(self._stacks)
        for item in self._instructions:
            self._run_instruction(stack_copy, item, True)

        return self.get_top_of_crates(stack_copy)

def main() -> None:
    """
    Main
    """
    solver = Day05()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
