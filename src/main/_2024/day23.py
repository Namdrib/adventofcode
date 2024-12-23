#!/usr/bin/python3
import sys

class Day23:
    """
    Solution for https://adventofcode.com/2024/day/23
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.connections: set = None
        self.all_connections: set = None

        self.largest_set: set = set()

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line is of the format "s1-s2" where s1 and s2 are
        names of computers that are connected to each other
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.connections = set()
        for item in self.input:
            connection: tuple = tuple(item.split('-'))
            self.connections.add(connection)

    def compute_computer_sets(self) -> None:
        """
        Create a dict of which computers connect to which other computers
        Since connections are necessarily mutual, this also tracks which
        computers connect to a given computer.
        """
        # {computer_name: [computer_names]}
        self.all_connections: dict = {}
        for c in self.connections:
            if c[0] not in self.all_connections:
                self.all_connections[c[0]] = []
            if c[1] not in self.all_connections:
                self.all_connections[c[1]] = []

            self.all_connections[c[0]].append(c[1])
            self.all_connections[c[1]].append(c[0])

    def get_sets_of_three(self) -> set:
        """
        Look for all sets of 3 computers where each computer is connected to
        each other.
        e.g. A-B + B-C + C-A is one such set

        :return: The set of all 3-connected computers
        :rtype: set
        """
        tri_connections: set = set()

        # We already know a and b are connected
        for a, b in self.connections:
            # Are there any computers that are connected to both A and B?
            for computer, connections in self.all_connections.items():
                if a in connections and b in connections:
                    tri_connections.add(tuple(sorted((a, b, computer))))

        return tri_connections

    def get_largest_interconnected_group(self, current: set, available: set, exclude: set):
        """
        Find the largest interconnected group (in graph theory terms, "clique").
        Uses the Bron-Kerbosch algorithm, with a global largest set

        :param current: The current set of PCs we're looking at
        :type current: set
        :param available: The PCs that could be joined to this network
        :type available: set
        :param exclude: The PCs that won't be joined to this network
        :type exclude: set
        """
        # Recursive base case: Nothing left to add to this set
        if not available and not exclude:
            if len(current) > len(self.largest_set):
                self.largest_set = current

        for pc in available.copy():
            # Otherwise Python will try to generate a set out of the elements of
            # the strings in pc (e.g. {'a', 'b'}, instead of {'ab'})
            pc_in_set: set = set()
            pc_in_set.add(pc)

            self.get_largest_interconnected_group(current.union(pc_in_set), available.intersection(self.all_connections[pc]), exclude.intersection(self.all_connections[pc]))

            # Don't consider pc again on the next iteration
            available.discard(pc)
            exclude = exclude.union(pc)

    def part_one(self) -> int:
        """
        Find all the sets of three inter-connected computers. How many contain
        at least one computer with a name that starts with t?
        """
        self.compute_computer_sets()
        tri_connections: set = self.get_sets_of_three()

        # Count the tri-connections where any of the computers starts with t
        count: int = 0
        for tc in tri_connections:
            if any(x.startswith('t') for x in tc):
                count += 1
        return count

    def part_two(self) -> int:
        """
        Return the password to get into the LAN party, which is:
        "the name of every computer at the LAN party, sorted alphabetically,
        then joined together with commas"
        """
        # Find the largest interconnected set of computers in this network
        all_computers: set = set(x for x in self.all_connections)
        self.get_largest_interconnected_group(set(), all_computers, set())

        # By this point, self.largest_set has been set by the helper method
        # Format the computers, comma-separated, sorted by name
        return ",".join(sorted(map(str, self.largest_set)))

def main() -> None:
    """
    Main
    """
    solver = Day23()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
