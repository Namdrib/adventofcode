#!/usr/bin/python3
import copy
import sys

class Day16:
    """
    Solution for https://adventofcode.com/2022/day/16

    Trying to do a depth-first branch and bound of the problem space.
    From every position, try every possible action, etc.

    Calculate the bounding constraint by how much "wasted" pressure we have at this point
    e.g. if there's no way we can do better than the current best solution, then bound the branch
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        # An adjacency list of all the locations
        self.graph: dict = {}

        # str: int. The flow rate of a valve
        self.flow_rate: dict = {}

        # str: bool. True if open, False if closed
        self.valve_state: dict = {}

        # str: int. The eventual flow rate (how much flow from now to time=0)
        self.eventual_flow: dict = {}

        # each action is either a move or turning a valve on
        self.actions: list = []

        self.best_epr: int = 0
        self.best_actions: list = []
        self.min_wasted_flow: int = 99999999

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()

        self.input = raw_input.split('\n')
        self.input = self.input[0:-1]

        for item in self.input:
            tokens = item.split()
            location = tokens[1]
            rate = tokens[4].split('=')[1].strip(';')

            self.flow_rate[location] = int(rate)
            self.valve_state[location] = False
            self.eventual_flow[location] = 0

            # Read the runnels
            valves_pos = 0
            tunnels = ''
            if 'valve ' in item:
                tunnels = [tokens[-1]]
            else:
                valves = item.split('valves')[1]
                tunnels = list(map(lambda x: x.strip(), valves.split(', ')))

            self.graph[location] = tunnels

        for item in self.graph.items():
            print(f'{item} rate={self.flow_rate[item[0]]}, state={self.valve_state[item[0]]}')

    def total_eventual_pressure_release(self) -> int:
        return sum(self.eveutual_flow.values())

    def calculate_eventual_pressure_release_from_actions(self, actions: list) -> int:
        """
        Simulate how much eventual pressure release we achieve if we take the current actions
        """
        epr: int = 0

        location = 'AA'
        for i, item in enumerate(actions):
            if item == 'turn':
                # calcualte eventual flow rate for that valve
                # i.e. how much that valve will release from now until time=30
                epr += (30-i+1) * self.flow_rate[location]
            else:
                location = item

        print(f'epr from the following actions: {actions} = {epr}')
        return epr

    def calculate_best_amount_of_remaining_flow(self, time) -> int:
        """
        Calculate how much flow we could potentially have lft if we turned on all of the remaining
        valves on one-by-one
        This is unrealistic as it assumes no travel time
        However it provides an upper bound of how well we could possible do
        """
        wasted_flow: int = 0

        unopened_locations: list = [self.flow_rate[x] for x in self.graph.keys() if not self.valve_state[x]]
        unopened_locations.sort(reverse=True)

        current_time = time
        for flow_rate in unopened_locations:
            if current_time >= 30:
                break

            wasted_flow += (30-current_time) * flow_rate
            current_time += 1

        print(f'The amount of wasted flow up till now: {wasted_flow}')
        return wasted_flow

    def calculate_wasted_flow(self, actions, time) -> int:
        """
        How much wasted flow at a given time (how many valves are closed)
        """
        wasted_flow: int = 0

        max_flow: int = sum(self.flow_rate.values()) * 30
        return max_flow - self.calculate_eventual_pressure_release_from_actions(actions)
        for location, rate in self.flow_rate.items():
            if not self.valve_state[location]:
                wasted_flow += (30-time) * rate

        return wasted_flow

    def pathfind_recurse(self, location: str, time: int, current_epr: int, actions: list) -> int:
        """
        Do a branch and bound on every possible action we can do here
        """
        # If we've hit the end, stop
        if time == 30:
            print(f'At the end. Current actions: {actions}')
            # If we've done better than a previous run, record our results
            if current_epr > self.best_epr:
                self.best_epr = current_epr
                self.best_actions = actions

                wasted_flow: int = self.calculate_wasted_flow(actions, time)
                print(f'amount of wasted flow: {wasted_flow}')
                self.min_wasted_flow = wasted_flow
            return

        # If we've already missed more flow than the best solution
        # No point going down this path
        # wasted_flow: int = self.calculate_wasted_flow(actions, time)
        wasted_flow: int = self.calculate_best_amount_of_remaining_flow(time)
        if wasted_flow >= self.min_wasted_flow:
            print(f'wasted flow from {actions} = {wasted_flow}')
            return

        # Explore all the possible options
        # Turn the valve in this location if it hasn't already been turned
        if not self.valve_state[location]:
            actions.append('turn')
            self.valve_state[location] = True
            epr = self.calculate_eventual_pressure_release_from_actions(actions)
            self.pathfind_recurse(location, time+1, epr, actions)
            actions.pop()
            self.valve_state[location] = False

        # Go down each tunnel
        for tunnel in self.graph[location]:
            actions.append(tunnel)
            epr = self.calculate_eventual_pressure_release_from_actions(actions)
            self.pathfind_recurse(tunnel, time+1, epr, actions)
            actions.pop()

    def pathfind(self, start: str = 'AA') -> int:
        """
        Find the best path that allows us to provide as much eventual pressure as possible
        """
        best_eventual_flow: int = 0
        actions: list = []

        self.pathfind_recurse(start, 0, 0, actions)
        return 0

    def part_one(self) -> int:
        """
        Return the ...
        """
        # actions = ['DD', 'turn', 'CC', 'BB', 'turn', 'AA', 'II', 'JJ', 'turn', 'II', 'AA', 'DD', 'EE', 'FF', 'GG', 'HH', 'turn', 'GG', 'FF', 'EE', 'turn', 'DD', 'CC', 'turn']
        # epr = self.calculate_eventual_pressure_release_from_actions(actions)
        # print(epr)
        self.pathfind('AA')
        print(self.best_epr)
        return 0

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
