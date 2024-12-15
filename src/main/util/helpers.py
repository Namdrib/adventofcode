direction_to_coords_map: dict = {
    'N' : {'x':  0, 'y': -1 },
    'NE': {'x':  1, 'y': -1 },
    'E' : {'x':  1, 'y':  0 },
    'SE': {'x':  1, 'y':  1 },
    'S' : {'x':  0, 'y':  1 },
    'SW': {'x': -1, 'y':  1 },
    'W' : {'x': -1, 'y':  0 },
    'NW': {'x': -1, 'y': -1 },
    # Arrows :)
    '^' : {'x':  0, 'y': -1 },
    '>' : {'x':  1, 'y':  0 },
    'v' : {'x':  0, 'y':  1 },
    '<' : {'x': -1, 'y':  0 },
}

cardinal_directions: list = [
    'N', 'E', 'S', 'W'
]

ordinal_directions: list = [
    'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'
]

def get_directions(directions: list = None):
    """
    Turn a list of directions into a list of delta-points

    :param directions: The directions to get co-ordinates for, defaults to cardinal_directions
    :type directions: list
    :yield: The next direction
    :rtype: Iterator[dict]
    """
    # Default to using cardinal directions
    # Get around having a mutable value as the default
    if directions is None:
        directions = cardinal_directions

    for d in directions:
        yield direction_to_coords_map[d]

def get_neighbours(x: int, y: int, grid: list, directions: list = None, include_oob: bool = False):
    """
    Get the neighbours of a given point and directions

    :param x: The x position of the point to get neighbours
    :type x: int
    :param y: The y position of the point to get neighbours
    :type y: int
    :param grid: The grid where the (x, y) co-ordinates are located
    :type grid: list
    :param directions: The directions to look for neighbours in, defaults to cardinal_directions
    :type directions: list, optional
    :param include_oob: Whether to include neighbours outside of the grid, defaults to False
    :type include_oob: bool, optional
    :yield: The next neighbour
    :rtype: Iterator[Point]
    """
    # Default to using cardinal directions
    # Get around having a mutable value as the default
    if directions is None:
        directions = cardinal_directions

    # Look around the current point
    for direction in directions:
        next_x: int = x + direction_to_coords_map[direction]['x']
        next_y: int = y + direction_to_coords_map[direction]['y']

        # Skip OOB neighbours if include_oob isn't set
        out_of_bounds: bool = not in_range(grid, next_y) or not in_range(grid[0], next_x)
        if out_of_bounds and not include_oob:
            continue

        yield Point(next_x, next_y)

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

def rotate_clockwise(p: Point) -> Point:
    """
    Rotate a Point clockwise by 90 degrees

    :param p: The original point
    :type p: Point
    :return: A new point, rotated 90 degrees clockwise
    :rtype: Point
    """
    return Point(-p.y if p.y else p.y, p.x)

def rotate_anticlockwise(p: Point) -> Point:
    """
    Rotate a Point anti-clockwise by 90 degrees

    :param p: The original point
    :type p: Point
    :return: A new point, rotated 90 degrees anti-clockwise
    :rtype: Point
    """
    return Point(p.y, -p.x if p.x else p.x)

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
