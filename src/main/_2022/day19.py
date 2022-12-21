#!/usr/bin/python3
import sys

ore_to_index: dict = {
    'ore': 0,
    'clay': 1,
    'obsidian': 2,
    'geode': 3
}

class Blueprint:
    def __init__(self, id_: int, cost_matrix: dict) -> None:
        self.id = id_
        self.cost_matrix: dict = cost_matrix

    def cost_to_build_bot(self, robot: str) -> list:
        """
        Return the cost to build a given bot
        """
        return self.cost_matrix[robot]

    def can_build_bot_with_resources(self, robot: str, resources: list) -> bool:
        """
        Return True if we can build the specified robot with the given resources, False otherwise
        """
        res: bool = all(x >= y for x, y in zip(resources, self.cost_to_build_bot(robot)))
        # print(f'{"can" if res else "cant"} build {robot} with {resources}')
        return res

class Day19:
    """
    Solution for https://adventofcode.com/2022/day/19
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None
        self.blueprints: list = []
        self.temp_max_geodes: int = -1
        self.max_geodes: int = -1
        self.best_geodes_at_time: list = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line describes a blueprint. The blueprint describes how much it costs to build a bot of each type
        """
        raw_input = sys.stdin.read()

        self.input = raw_input.split('\n')
        self.input = self.input[0:-1]

        for item in self.input:
            # 'ore': [amount of resource]
            cost_matrix: dict = {}

            tokens = item.split()
            blueprint_id = int(tokens[1].strip(':'))
            cost_matrix['ore'] = [int(tokens[6]), 0, 0, 0]
            cost_matrix['clay'] = [int(tokens[12]), 0, 0, 0]
            cost_matrix['obsidian'] = [int(tokens[18]), int(tokens[21]), 0, 0]
            cost_matrix['geode'] = [int(tokens[27]), 0, int(tokens[30]), 0]

            print(f'Cost matrix for blueprint {blueprint_id}:')
            for key, value in cost_matrix.items():
                print(f'{key}: {value}')
            print()

            self.blueprints.append(Blueprint(blueprint_id, cost_matrix))

    def build_bot(self, bot: str, blueprint: Blueprint, resources: list, robots: list) -> tuple:
        """
        Build a bot, adding it to the bot inventory
        Subtract the resources according to the blueprint's specs
        Return the new resources and robots
        """
        # print(f'  Building {bot} bot with {resources}, currently have {robots}')
        bot_cost: list = blueprint.cost_to_build_bot(bot)
        for i, item in enumerate(bot_cost):
            resources[i] -= item

        robots[ore_to_index[bot]] += 1
        return resources, robots

    def mine_geodes_with_blueprint(self, blueprint: Blueprint, time: int) -> int:
        """
        Mine as many geodes as we can with the given blueprint and time limit
        Assuming we start with 1 ore robot, calculate how many geodes we can mine in max_time
        """
        resources = [0 for _ in range(4)]
        robots = [1, 0, 0, 0]

        current_time = 0
        while current_time < time:
            print(f'== Minute {current_time} ==')
            print(f'  Robots: {robots}, resources: {resources}')

            built_something: bool = False

            # We can build a geode bot - do it
            if blueprint.can_build_bot_with_resources('geode', resources):
                resources, robots = self.build_bot('geode', blueprint, resources, robots)
                built_something = True

            # If we don't have enough obsidian production, try to build an obsidian bot
            if not built_something:
                if robots[2] < blueprint.cost_to_build_bot('geode')[2] - robots[2]:
                    if blueprint.can_build_bot_with_resources('obsidian', resources):
                        resources, robots = self.build_bot('obsidian', blueprint, resources, robots)
                        built_something = True

            if not built_something:
                # If we don't have enough clay production, try to build a clay bot
                if robots[1] < blueprint.cost_to_build_bot('obsidian')[1] - robots[1]:
                    if blueprint.can_build_bot_with_resources('clay', resources):
                        resources, robots = self.build_bot('clay', blueprint, resources, robots)
                        built_something = True

            if not built_something:
                if robots[0] < blueprint.cost_to_build_bot('clay')[0]:
                    if blueprint.can_build_bot_with_resources('ore', resources):
                        resources, robots = self.build_bot('ore', blueprint, resources, robots)
                        built_something = True

            # increase resources
            for i, item in enumerate(robots):
                resources[i] += item

            current_time += 1
            print()

        print(f'{robots} gave us resources: {resources}')

        return resources[-1]

    def calculate_geode_yield_from_blueprint_recurse(self, blueprint, time, time_limit, resources, robots, incoming_robot):
        """
        This is the current working method
        Not working - slow af and reporting inaccurate results
        """
        resources = list(resources)
        robots = list(robots)

        # Get the resources from our bot
        for i, item in enumerate(robots):
            resources[i] += item

        # We don't get the ore that came with the most recent robot
        if incoming_robot:
            resources[ore_to_index[incoming_robot]] -= 1

        # We've hit the time limit, record max geodes and leave
        if time >= time_limit:
            # print('Hit time limit')
            if resources[3] > self.temp_max_geodes:
                print(f'New max: {resources} with {robots} bots')
                self.temp_max_geodes = resources[3]
            return

        # TODO: bounding constraint to prune the search here?
        # If we built a geode bot every minute and can't beat the max so far, we shouldn't bother exploring
        my_max_geode = resources[3] + sum(robots[3] + i for i in range(time+1, time_limit))
        if my_max_geode < self.temp_max_geodes:
            return

        # If our geodes right now is fewer than the geodes at another time, stop
        if resources[3] < self.best_geodes_at_time[time]-2:
            return

        # Build a geode bot if we can
        if blueprint.can_build_bot_with_resources('geode', resources):
            new_resources, new_robots = self.build_bot('geode', blueprint, resources, robots)
            self.calculate_geode_yield_from_blueprint_recurse(blueprint, time+1, time_limit, new_resources, new_robots, 'geode')

        # We don't have enough obsidian - see if we can make an obsidian bot
        if robots[2] < blueprint.cost_to_build_bot('geode')[2]:
            if blueprint.can_build_bot_with_resources('obsidian', resources):
                new_resources, new_robots = self.build_bot('obsidian', blueprint, resources, robots)
                self.calculate_geode_yield_from_blueprint_recurse(blueprint, time+1, time_limit, new_resources, new_robots, 'obsidian')

        # Don't build anything
        # new_resources = list(resources)
        # for i, item in enumerate(robots):
        #     new_resources[i] += item
        self.calculate_geode_yield_from_blueprint_recurse(blueprint, time+1, time_limit, resources, robots, '')

        # We don't have enough clay - see if we can make an clay bot
        if robots[1] < blueprint.cost_to_build_bot('obsidian')[1]:
            if blueprint.can_build_bot_with_resources('clay', resources):
                new_resources, new_robots = self.build_bot('clay', blueprint, resources, robots)
                self.calculate_geode_yield_from_blueprint_recurse(blueprint, time+1, time_limit, new_resources, new_robots, 'clay')

        # We don't have enough ore - see if we can make an ore bot
        if robots[0] < max(blueprint.cost_to_build_bot(x)[0] for x in ['geode', 'obsidian', 'clay']):
            if blueprint.can_build_bot_with_resources('ore', resources):
                new_resources, new_robots = self.build_bot('ore', blueprint, resources, robots)
                self.calculate_geode_yield_from_blueprint_recurse(blueprint, time+1, time_limit, new_resources, new_robots, 'ore')

    def calculate_geode_yield_from_blueprint(self, blueprint, time_limit) -> int:
        self.temp_max_geodes = 0
        self.best_geodes_at_time = [0 for _ in range(time_limit)]
        self.calculate_geode_yield_from_blueprint_recurse(blueprint, 0, time_limit, [0, 0, 0, 0], [1, 0, 0, 0], '')

        return self.temp_max_geodes

    def calculate_best_blueprint(self) -> int:
        max_geodes: int = 0
        max_geodes_index: int = 0
        for i, blueprint in enumerate(self.blueprints):
            geodes = self.mine_geodes_with_blueprint(blueprint, 0, 24, [0, 0, 0, 0], [1, 0, 0, 0], '')

            if geodes > max_geodes:
                max_geodes = geodes
                max_geodes_index = i

        return max_geodes * self.blueprints[max_geodes_index].id

    def part_one(self) -> int:
        """
        Return the ...
        """
        max_geodes_from_blueprint: int = self.calculate_geode_yield_from_blueprint(self.blueprints[0], 24)
        return max_geodes_from_blueprint
        # return self.mine_geodes_with_blueprint(self.blueprints[0], 24)
        # return self.calculate_best_blueprint()

    def part_two(self) -> int:
        """
        Return the ...
        """
        return 0

def main() -> None:
    """
    Main
    """
    solver = Day19()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
