#!/usr/bin/python3
import sys

class Day16:
    """
    Solution for https://adventofcode.com/2022/day/16

    Only part 1
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        # An adjacency graph of all the valves
        self.graph: list[list] = []

        # Translate a valve name to its index in the graph
        self.valve_names: list[str] = []

        # The flow rate of a valve
        self.flow_rate: list[int] = []

        # True if open, False if closed
        self.valve_state: list[bool] = []

        # Record the best outcome so far
        self.best_epr: int = 0
        self.best_actions: dict[int: int] = []
        self.best_wasted_flow: int = 99999

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()

        self.input = raw_input.split('\n')
        self.input = self.input[0:-1]

        # Initialise the adjacency graph to infinite
        self.graph = [[99999 for _ in range(len(self.input))] for _ in range(len(self.input))]

        # Get the names of all the valves
        for item in self.input:
            tokens = item.split()
            self.valve_names.append(tokens[1])

        # Initialise sizes
        self.flow_rate = [0 for _ in range(len(self.valve_names))]
        self.valve_state = [False for _ in range(len(self.valve_names))]

        for item in self.input:
            tokens = item.split()

            # Store the valve and turn it into a unique index for the adjacency graph
            valve = tokens[1]
            index = self.valve_names.index(valve)

            rate = tokens[4].split('=')[1].strip(';')
            self.flow_rate[index] = int(rate)

            # All valves start closed
            self.valve_state[index] = False

            # Read the tunnels
            tunnels = ''
            if 'valve ' in item:
                # Only one tunnel
                tunnels = [tokens[-1]]
            else:
                # Multiple tunnels
                valves = item.split('valves')[1]
                tunnels = list(map(str.strip, valves.split(', ')))

            # Index-ify all of the valves that can be reached from here
            destinations = list(map(self.valve_names.index, tunnels))

            for destination in destinations:
                self.graph[index][destination] = 1

        # Finalise the weightings from each valve to each other valve
        self.calculate_shortest_path_to_each_valve()

        # for i, name in enumerate(self.valve_names):
        #     print(f'Tunnel {name}: {self.graph[i]}: rate={self.flow_rate[i]}')

    def calculate_shortest_path_to_each_valve(self):
        """
        Populate self.graph with the shortest distances from each valve to every other
        Floyd-Warshall algorithm
        """
        # Distances to every other place has already been initialised to a large number
        # Distance to self is 0
        for i in range(len(self.graph)):
            self.graph[i][i] = 0

        for k in range(len(self.graph)):
            for i in range(len(self.graph)):
                for j in range(len(self.graph)):
                    if self.graph[i][j] > self.graph[i][k] + self.graph[k][j]:
                        self.graph[i][j] = self.graph[i][k] + self.graph[k][j]

    def calculate_eventual_pressure_release_from_actions(self, actions: dict[int, int]) -> int:
        """
        Simulate how much eventual pressure release we achieve if we take the current actions
        Each action takes into account travel + time to turn the valve
        Each item in action is the {valve, time turned on}
        """
        epr: int = 0

        # Each valve gives off a rate for the entire remaining time
        for valve, time in actions.items():
            epr += (30-time) * self.flow_rate[valve]

        return epr

    def calculate_max_wasted_flow(self) -> int:
        """
        The maximum wasted flow is if we open no valves
        """
        return sum(map(lambda x: x * 30, self.flow_rate))

    def calculate_approximate_wasted_flow_so_far(self, actions) -> int:
        """
        Approximate wasted flow so far is the sum of unopened valves up till now
        """
        current_time: int = max(actions.values())
        wasted_flow_from_closed_valves: int = sum(map(lambda x: x * current_time, self.flow_rate))

        return wasted_flow_from_closed_valves

    def pathfind_recurse(self, valve: int, time: int, current_epr: int, actions: dict) -> int:
        """
        Do a branch and bound on every possible action we can do here
        """
        # If we've hit the end, stop
        if time >= 30:
            # print(f'At the end. Current actions: {actions}')
            return

        # If we've done better than a previous run, record our results
        if current_epr > self.best_epr:
            self.best_epr = current_epr
            self.best_actions = actions
            self.best_wasted_flow = self.calculate_max_wasted_flow() - self.best_epr

        # Calculate the wasted flow so far (the upper bound)
        # If we can't do better than the best, then prune this branch
        if actions:
            wasted_flow: int = self.calculate_approximate_wasted_flow_so_far(actions)
            if wasted_flow >= self.best_wasted_flow:
                return

        # Greedily explore the best path first
        # This lets us get a better wasted flow earlier on
        # This takes into account the amount of flow we lose out on in transit
        neighbours_sorted: list = list(range(len(self.graph)))
        neighbours_sorted.sort(key=lambda x: self.flow_rate[x]-time, reverse=True)

        # Explore all the possible valves from here
        for next_valve in neighbours_sorted:
            weight: int = self.graph[valve][next_valve]

            # We'll have activated valve x in weight time + 1 to open it
            next_time: int = time + weight + 1
            if self.valve_state[next_valve]:
                # What is open may never (be) open(ed again)
                continue
            if self.flow_rate[next_valve] == 0:
                # No point opening something that will give nothing
                continue
            if next_time > 30:
                # Won't have enough time to explore this option
                continue

            actions[next_valve] = next_time
            self.valve_state[next_valve] = True
            epr = self.calculate_eventual_pressure_release_from_actions(actions)
            self.pathfind_recurse(next_valve, next_time, epr, actions)
            self.valve_state[next_valve] = False
            actions.pop(next_valve)

    def find_best_path(self, start: str = 'AA'):
        """
        Find the best path that allows us to provide as much eventual pressure as possible
        Store the best path and cost in self
        """
        actions: dict = {}
        start_index: int = self.valve_names.index(start)
        self.pathfind_recurse(start_index, 0, 0, actions)

    def part_one(self) -> int:
        """
        Return the most pressure we can release in 30 minutes
        """
        self.find_best_path('AA')
        return self.best_epr

    def part_two(self) -> int:
        """
        Return the ...
        """
        return 0

def main() -> None:
    """
    Main
    """
    solver = Day16()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
