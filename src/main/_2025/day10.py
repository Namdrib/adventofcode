#!/usr/bin/python3
import os
from queue import PriorityQueue
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class Machine:
    def __init__(self, target: str, buttons: list, joltage_reqs: list) -> None:
        """
        As an example:
        [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
        ^-----^ ^-------------------------------------^ ^----------^
        target                   buttons                joltage_reqs

        The target is a set of 5 lights, where the 3rd (0-indexed) is turned on,
        and all others are off.
        There are 5 buttons. The first button toggles lights 0, 2, 3, and 4. The
        second button toggles lights 2 and 3.
        The joltage requirements of each button is described by the numbers in
        the braces. The 0th button costs 7, the first costs 5, ...

        :param target: The target state
        :type target: str
        :param buttons: A list of strings describing what each button press does
        :type buttons: list
        :param joltage_reqs: A string representing the joltage requirements.
        :type joltage_reqs: list
        """
        # Strip the brackets
        # A '#' represents a light that is on
        self.target = [x == '#' for x in target[1:-1]]
        self.lights: bool = [False for _ in self.target]

        # Each button toggles some set of lights
        self.buttons: list = []
        for button in buttons:
            # Strip the parens
            nums: list = button[1:-1]
            self.buttons.append([int(light) for light in nums.split(',')])

        self.joltage_reqs: list = [int(j) for j in joltage_reqs[1:-1].split(',')]

    def __repr__(self) -> str:
        return f"{__class__.__name__}({self.target}, {self.buttons}, {self.joltage_reqs})"

    def __str__(self) -> str:
        lights_str: str = "".join('#' if x else '.' for x in self.lights)
        return lights_str

class MachineState:
    def __init__(self, lights: str, cost: int = 0, path: list = []) -> None:
        self.lights: str = lights
        self.cumulative_cost: int = cost
        self.path: list = [x for x in path]

    # For use with set/dict and queue.PriorityQueue
    def __hash__(self) -> int:
        return hash((
            ''.join('#' if x else '.' for x in self.lights),
            self.cumulative_cost,
            ','.join(str(x) for x in self.path)
        ))

    def __lt__(self, other: any) -> bool:
        return self.cumulative_cost < other.cumulative_cost

class Day10:
    """
    Solution for https://adventofcode.com/2025/day/10
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.machines: list = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.machines: list = []
        for item in self.input:
            target_state, *buttons, joltage = item.split()

            m = Machine(target_state, buttons, joltage)
            print(m)
            self.machines.append(m)

    def configure(self, machine: Machine) -> list:
        """
        Configure the machine by pressing buttons until its light state matches
        its target state

        Use the fewest presses as possible

        The search space is all the possible states of the machine, and their
        cumulative cost
        Use a graph search to see what will solve the machine first
        Breadth first search is good enough for part 1

        :param machine: The machine to configure
        :type machine: Machine
        :return: The buttons that were pressed to configure the machine
        :rtype: int
        """

        seen: set = set()
        pq: PriorityQueue = PriorityQueue()

        start: MachineState = MachineState(machine.lights, 0, [])
        pq.put(start)

        while not pq.empty():
            # The current light configuration, and cost so far
            current: MachineState = pq.get()

            # Reached the target state - current holds the path taken to get to
            # this point
            if current.lights == machine.target:
                return current.path

            # Try each potential button press
            for i, button in enumerate(machine.buttons):
                # There's no point in pressing the same button twice, as it will
                # cancel itself out. This cuts the runtime from ~10 mins to ~1 min
                if i in current.path:
                    continue

                # Toggle each light that is activated by the button
                new_state = [x for x in current.lights]
                for light_index in button:
                    new_state[light_index] = not new_state[light_index]

                new_path = [x for x in current.path]
                new_path.append(i)
                new_state = MachineState(new_state, current.cumulative_cost + 1, new_path)
                pq.put(new_state)

            seen.add(current)

        return None

    def part_one(self) -> int:
        """
        Return the fewest button presses required to configure each machine to
        its target state
        """
        count: int = 0

        for m in self.machines:
            presses: list = self.configure(m)
            count += len(presses)

        return count

    def part_two(self) -> int:
        """
        Return the ...
        """
        count: int = 0

        return count

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
