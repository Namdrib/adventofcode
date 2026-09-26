#!/usr/bin/python3
from dataclasses import dataclass

# order and unsafe_hash allow this to be inserted into sets and dicts
@dataclass(order=True, unsafe_hash=True)
class Coord2D:
    """
    A class representing co-ordinates in a 2D plane
    """
    x: int
    y: int
