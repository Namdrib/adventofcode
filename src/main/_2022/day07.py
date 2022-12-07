#!/usr/bin/python3
import sys

directory_sizes: dict = {}

class Node:
    """
    A node in a file system tree
    """
    # Tree stuff
    # We are a leaf node if there are no children
    children: list = []
    parent = None # Node
    depth: int = 0

    # Data
    name: str = ''
    size: int = 0
    cumulative_size: int = 0

    def __init__(self, name: str = '', size: int = 0, depth: int = 0, parent = None):
        """
        Constructor
        """
        self.name = name
        self.size = size
        self.depth = depth
        self.parent = parent
        self.children = []

    def pretty_print(self):
        """
        Visualise this Node and its children as a tree
        """
        indentation: str = '  '*self.depth
        details: str = ('dir' if self.size == 0 else f'file, size={self.size}')
        # Print self
        print(f'{indentation}- {self.name} ({details})')

        # Print all children
        for child in self.children:
            child.pretty_print()

    def update_cumulative_size(self):
        """
        Calculate this Node's cumulative size, which is the size of all the
        files and directories under this Node
        """
        global directory_sizes
        new_size: int = 0

        for child in self.children:
            if child.size == 0:
                child.update_cumulative_size()
                new_size += child.cumulative_size
            else:
                new_size += child.size

        self.cumulative_size = new_size

        # Store the cumulative size in a global dict so it is accessible from Day07
        # got kinda lazy here
        # when storing in the dictionary, not all dirs/file names are unique.
        # prepend with parent name to reduce the chance of clashes
        name = self.name
        if hasattr(self, 'parent'):
            if hasattr(self.parent, 'name'):
                name = f'{self.parent.name}/{name}'
        directory_sizes[name] = self.cumulative_size

class Day07:
    """
    Solution for https://adventofcode.com/2022/day/7
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self._input: list = None
        self._filesystem_root: Node = None

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()

        self._input = raw_input.split('\n')
        self._input = self._input[0:-1]

        # Construct a filesystem tree of files and directories
        current_depth: int = 0
        is_reading_command: bool = True
        self._filesystem_root = Node(name='/')
        head: Node = self._filesystem_root

        for item in self._input:
            is_reading_command = item.startswith('$')

            if is_reading_command:
                if item == '$ cd ..':
                    # Go up one directory
                    current_depth -= 1
                    head = head.parent

                elif item == '$ cd /':
                    current_depth = 0
                    head = self._filesystem_root

                elif item.startswith('$ cd'):
                    # Go to the specified directory
                    dir_name: str = item.split()[-1]

                    current_depth += 1
                    head = [x for x in head.children if x.name == dir_name][0]

                elif item.startswith('$ ls'):
                    # List items. The following lines won't be commands
                    pass
            else:
                # Build the Node's children for this level
                file_size, file_name = item.split()
                size = 0 if file_size == 'dir' else int(file_size)
                child_node = Node(file_name, size=size, depth=current_depth+1, parent=head)
                head.children.append(child_node)

        # self._filesystem_root.pretty_print()

    def part_one(self) -> int:
        """
        Return the sum of the dirs whose cumulative size is less than 10000
        """
        global directory_sizes
        self._filesystem_root.update_cumulative_size()

        # The sum of all directories smaller than 100000
        return sum(size for _, size in directory_sizes.items() if size <= 100000)

    def part_two(self) -> int:
        """
        Return the smalelst directory we can delete to get the required space
        """
        global directory_sizes
        total_available_space: int = 70000000
        required_space: int = 30000000

        # Calculate how much space we need to delete
        currently_used_space: int = directory_sizes['/']
        currently_unused_space: int = total_available_space - currently_used_space
        minimum_space_to_delete: int = required_space - currently_unused_space

        # The delete smallest directory that gives us enough space
        return min(size for _, size in directory_sizes.items() if size >= minimum_space_to_delete)

def main() -> None:
    """
    Main
    """
    solver = Day07()
    solver.read_input()

    print(f'Part 1: {solver.part_one()}')
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
