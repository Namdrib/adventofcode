#!/usr/bin/python3
import copy
import functools
import math
import sys

class Monkey:
    """
    A monkey has items with worry levels, and throws them to other monkeys based on the worry level
    The worry level changes (operator, operand)
    """
    def __init__(self, id_: int, starting_items: list, operator: str, operand: str, division_test: int, true_monkey: int, false_monkey: int, debug_: bool=False) -> None:
        """
        Constructor
        """
        self.id = id_
        self.items = starting_items
        self.operator = operator
        self.operand = operand
        self.division_test = division_test
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey

        self.debug: bool = debug_

        # This is used for the puzzle output
        self.num_items_inspected: int = 0

    def get_num_items(self) -> int:
        return len(self.items)

    def show_items(self) -> None:
        """
        Pretty print the items this monkey has
        """
        print(f'Monkey {self.id}: {self.items}.')

    def inspect(self, reset_worry: bool=True, lowest_common_factor: int=0) -> tuple:
        """
        Inspect the first item in the monkey's items
        Change the worry level associated with that item by the operator and operand
        If reset_worry is true, reset the worry level for that item
        Then, based on the division_test, pass that item to another monkey

        The lowest_common_factor is used to keep the worry levels in check for part two

        Return the new worry level assiciated with that item and the monkey we're passing it to
        Whoever calls this method has to deal with giving that item to the other monkey
        """
        # Inspect the item
        if self.debug:
            print(f'  Monkey inspects an item with a worry level of {self.items[0]}')
        self.num_items_inspected += 1

        # Apply the worry level change
        old_worry_level: int = self.items[0]
        new_worry_level: int = self.apply_worry_operation(old_worry_level)

        # Reset the worry if applicable
        new_worry_level = self.reset_worry_level(new_worry_level, reset_worry, lowest_common_factor)

        # Remove the first item from the bag
        self.items = self.items[1:]

        # Pass the item on to the next monkey based on the worry test
        pass_worry_test: bool = self.test(new_worry_level)
        target_monkey: int = 0
        if pass_worry_test:
            target_monkey = self.true_monkey
            if self.debug:
                print(f'    Current worry level is divisible by {self.division_test}')
        else:
            target_monkey = self.false_monkey
            if self.debug:
                print(f'    Current worry level is not divisible by {self.division_test}')

        if self.debug:
            print(f'    Item with worry level {new_worry_level} is thrown to monkey {self.false_monkey}')
        return new_worry_level, target_monkey

    def reset_worry_level(self, current_worry_level: int, reset_worry: bool, lowest_common_factor: int) -> int:
        """
        Reset the worry level after seeing the item has not been damaged
        """
        if reset_worry:
            # For part 1, always divide by 3
            current_worry_level = int(math.floor(current_worry_level / 3))
            if self.debug:
                print(f'    Monkey gets bored with item. Worry level is divided by 3 to {current_worry_level}')
        else:
            # For part two, we don't divide by a fixed number.
            # However, the current worry level is always disible by the lowest factor
            # This trick is used to prevent the numbers from getting too large
            current_worry_level %= lowest_common_factor

        return current_worry_level

    def resolve_operand(self, current_worry_level: int) -> int:
        """
        Resolve what the operand should be as an int
        (e.g. transforming old to whatever the current worry level is
        """
        if self.operand == 'old':
            return current_worry_level
        return int(self.operand)

    def apply_worry_operation(self, current_worry_level: int) -> int:
        """
        Modify the worry level by whatever the operator and operand says
        """
        operand: int = self.resolve_operand(current_worry_level)
        new_worry_level: int = 0
        if self.operator == '+':
            new_worry_level = current_worry_level + self.resolve_operand(current_worry_level)
            if self.debug:
                print(f'    Worry level increases by {operand} to {new_worry_level}.')
        elif self.operator == '*':
            new_worry_level = current_worry_level * self.resolve_operand(current_worry_level)
            if self.debug:
                print(f'    Worry level is multiplied by {operand} to {new_worry_level}.')

        return new_worry_level

    def test(self, number: int) -> bool:
        """
        Return True if the worry is divisble by division_test, False otherwise
        """
        return number % self.division_test == 0

    def receive_item(self, item: int) -> None:
        """
        Receive an item with a given worry level. Add that to the current items
        """
        self.items.append(item)

class Day11:
    """
    Solution for https://adventofcode.com/2022/day/11
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.monkeys: Monkey = []
        self.original_monkeys = []

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each block of lines corresponds to a Monkey
        """
        raw_input = sys.stdin.read()

        self.input = raw_input.split('\n')
        self.input = self.input[0:-1]

        id_: int = 0
        starting_items: list = []
        operator: str = ''
        operand: str = ''
        division_test: int = 1
        true_monkey: int = 0
        false_monkey: int = 0

        for item in self.input:
            item = item.strip()
            if item.startswith('Monkey'):
                id_ = int(item.split()[1].strip(':'))

            elif item.startswith('Starting items'):
                numbers = item.split(': ')[1].strip()
                starting_items = [int(x) for x in numbers.split(', ')]

            elif item.startswith('Operation'):
                item = item.split('= ')[1]
                operation = item.split()
                operator = operation[1]
                operand = operation[2]

            elif item.startswith('Test'):
                division_test = int(item.split()[-1])

            elif item.startswith('If true'):
                true_monkey = int(item.split()[-1])

            elif item.startswith('If false'):
                false_monkey = int(item.split()[-1])

            elif item == '':
                new_monkey: Monkey = Monkey(id_, starting_items, operator, operand, division_test, true_monkey, false_monkey, debug_=False)
                self.original_monkeys.append(new_monkey)

        # Handle the last one
        new_monkey: Monkey = Monkey(id_, starting_items, operator, operand, division_test, true_monkey, false_monkey, debug_=False)
        self.original_monkeys.append(new_monkey)

    def do_round(self, reset_worry: bool=True, lowest_common_factor: int=0) -> None:
        """
        In one round, each monkey inspects all of the items in their bag
        and passes them on to the next monkey
        """
        for monkey in self.monkeys:
            # print(f'Monkey {monkey.id}:')
            for _ in range(monkey.get_num_items()):
                item, target = monkey.inspect(reset_worry, lowest_common_factor)
                self.monkeys[target].receive_item(item)

    def calculate_product_of_two_most_active_monkeys(self) -> int:
        """
        This is what we return in each part
        """
        num_items_inspected: list = [x.num_items_inspected for x in self.monkeys]
        num_items_inspected.sort()
        return num_items_inspected[-1] * num_items_inspected[-2]

    def part_one(self) -> int:
        """
        Return the product of the two most active monkeys after 20 rounds
        """
        self.monkeys = copy.deepcopy(self.original_monkeys)
        for i in range(20):
            self.do_round()
            # print(f'After round {i+1}, the monkeys are holding items with these worry levels:')
            if (i+1) == 1 or (i+1) == 20 or (i+1) % 1000 == 0:
                print(f'== After round {i+1} ==')
                for monkey in self.monkeys:
                    print(f'Monkey {monkey.id} inspected items {monkey.num_items_inspected} times.')

        return self.calculate_product_of_two_most_active_monkeys()

    def part_two(self) -> int:
        """
        Return the product of the two most active monkeys after 10000 rounds
        """
        self.monkeys = copy.deepcopy(self.original_monkeys)

        # All of the divisors in the puzzle input are prime.
        # Calculate the product of all of the divisors and pass sthat to the inspect() method
        # The worry must be able to be divided by this
        # This keeps the numbers from getting too large
        all_divisors: list = [monkey.division_test for monkey in self.monkeys]
        product_of_divisors = functools.reduce(lambda a, b: a * b, all_divisors)

        for _ in range(10000):
            self.do_round(reset_worry=False, lowest_common_factor=product_of_divisors)

        return self.calculate_product_of_two_most_active_monkeys()

def main() -> None:
    """
    Main
    """
    solver = Day11()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
