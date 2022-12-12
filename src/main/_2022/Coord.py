#!/usr/bin/python3

class Coord2D:
    """
    A class representing co-ordinates in a 2D plane
    """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __lt__(self, obj) -> bool:
        if self.x == obj.x:
            return self.y < self.y
        return self.x < obj.x

    def __eq__(self, obj) -> bool:
        return isinstance(obj, Coord2D) and self.x == obj.x and self.y == obj.y

    def __hash__(self) -> int:
        return int(0.5 * (self.x + self.y) * (self.x + self.y + 1) + self.y)
