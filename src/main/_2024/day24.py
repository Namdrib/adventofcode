#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from util import helpers

class GateConnection:
    """
    A node of a binary tree of wires and an operation, where the connecting
    wires are the two children. The node's value is determined by the operation
    it performs, and the value of its children
    """
    def __init__(self, name: str, in1_name: str, in2_name: str, op: str) -> None:
        self.name: str = name
        self.in1_name: str = in1_name
        self.in2_name: str = in2_name
        self.op: str = op

        self.in1: GateConnection = None
        self.in2: GateConnection = None

        self.value: bool = None

    def evaluate_value(self) -> bool:
        if self.value is None:
            v1 = self.in1.evaluate_value()
            v2 = self.in2.evaluate_value()

            if self.op == "AND":
                self.value = v1 and v2
            if self.op == "OR":
                self.value = v1 or v2
            if self.op == "XOR":
                self.value = v1 ^ v2

        return self.value

    def __repr__(self) -> str:
        return f'GateConnection({self.name}, {self.in1_name}, {self.in2_name}, {self.op})'

    def original_representation(self) -> str:
        return f'{self.in1_name} {self.op} {self.in2_name} --> {self.name}'

    def __str__(self) -> str:
        return f'{self.name}: {self.value}'

class Day24:
    """
    Solution for https://adventofcode.com/2024/day/24
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        # {wire_name: GateConnection}
        self.wires: dict = {}

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        reading_values: bool = True
        for item in self.input:
            if reading_values:
                if item:
                    wire, value = item.split(': ')
                    # The initial set of nodes are leaf nodes of the binary tree
                    # They have their value prescribed, and have no children
                    self.wires[wire] = GateConnection(wire, None, None, None)
                    self.wires[wire].value = 1 if value == '1' else 0
                else:
                    reading_values = False
            else:
                # The next set of nodes are at arbitrary points of the binary
                # tree. Their children aren't guaranteed to exist yet. For now,
                # make a node for each one - the children will be set later
                connections: list = item.split(' ')
                self.wires[connections[4]] = GateConnection(connections[4], connections[0], connections[2], connections[1])

        # Now that all of the nodes in the tree exist, make a second pass to
        # populate the connections in the binary tree
        for name, gc in self.wires.items():
            if gc.in1 is None and gc.in1_name is not None:
                gc.in1 = self.wires[gc.in1_name]
            if gc.in2 is None and gc.in2_name is not None:
                gc.in2 = self.wires[gc.in2_name]

    def part_one(self) -> int:
        """
        Return the decimal representation of the binary number that is obtained
        from all fo the 'z' wires. zn,zn-1,...,z1,z0
        """
        # The z-wires are at the root of the tree, so all their descendants can
        # be populated from them
        # Reverse them so the most significant bit (highest z value) is first
        z_wires: list = reversed(sorted([wire for wire in self.wires if wire.startswith('z')]))

        # The binary representation of the values in the z-wires
        binary_str: str = ""

        for z_wire in z_wires:
            val: bool = self.wires[z_wire].evaluate_value()
            binary_str += ('1' if val else '0')

        return int(binary_str, 2)

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
    solver = Day24()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
