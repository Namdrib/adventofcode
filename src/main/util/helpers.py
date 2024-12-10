# All of the cardinal directions + diagonals
# If you don't want diagonals, skip every second one
directions: list = [
    { 'name': 'N ', 'x':  0, 'y': -1 },
    { 'name': 'NE', 'x':  1, 'y': -1 },
    { 'name': 'E' , 'x':  1, 'y':  0 },
    { 'name': 'SE', 'x':  1, 'y':  1 },
    { 'name': 'S' , 'x':  0, 'y':  1 },
    { 'name': 'SW', 'x': -1, 'y':  1 },
    { 'name': 'W' , 'x': -1, 'y':  0 },
    { 'name': 'NW', 'x': -1, 'y': -1 },
]

cardinal_directions: list = [
    { 'name': 'N ', 'x':  0, 'y': -1 },
    { 'name': 'E' , 'x':  1, 'y':  0 },
    { 'name': 'S' , 'x':  0, 'y':  1 },
    { 'name': 'W' , 'x': -1, 'y':  0 },
]

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def add(self, p) -> None:
        self.x += p.x
        self.y += p.y

    def subtract(self, p) -> None:
        self.x -= p.x
        self.y -= p.y

    def clone(self):
        return Point(self.x, self.y)

    def __eq__(self, p) -> bool:
        return self.x == p.x and self.y == p.y

    def __hash__(self) -> int:
        return self.x + 2 * self.x * self.y + self.y

    def __repr__(self) -> str:
        return f'Point({self.x}, {self.y})'

def in_range(thing, index: int) -> bool:
    """
    Return whether the index is in range fo the thing. i.e., is it safe to do thing[index]?

    :param thing: A container (e.g., string, list, etc.)
    :type thing: Any
    :param index: The index to test bounds
    :type index: int
    :return: True if the index is in bounds of the thing
    :rtype: bool
    """
    return 0 <= index < len(thing)
