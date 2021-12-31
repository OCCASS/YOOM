import math
from point import Point
from config import MAX_RAY_DISTANCE, TILE, WORLD_MAP

"""
Павлов Тимур 01.01.2021. Написаны классы Ray и RayCastHit 

Использованы алгоритмы написанные Ангелиной Вайман 28.12.2021 и Арсланом Батталовым 29.12.2021
"""


class RayCastHit:
    def __init__(self, distance: float, point: Point):
        self.distance = distance
        self.point = point


class Ray:
    def __init__(self, origin: Point, direction: float, length: float = None, end: Point = None):
        """
        Ray class used for convenient use
        :param origin: start point of ray
        :param direction: direction of ray
        :param length: a parameter that determines the length of the beam
        :param end: end point of ray
        """
        self.origin = origin
        self.direction = direction

        if length is None and end is None:
            raise TypeError('Ray.__init__ method has only 3 required arguments '
                            'start: Point, angel: float and (length: float or end: Point)')
        elif length is not None and end is not None:
            raise TypeError(
                'Ray.__init__ method has only 3 required arguments, '
                'you can`t use length and end parameters at the same time')

    @property
    def length(self) -> float:
        return math.sqrt((self.origin.x - self.end.x) ** 2 + (self.origin.y - self.end.y) ** 2)

    @property
    def end(self) -> Point:
        return Point(self.origin.x + math.cos(self.direction) * self.length,
                     self.origin.y + math.sin(self.direction) * self.length)

    def get_point(self, distance: float) -> Point:
        """
        Get a point at distance units along the ray
        :param distance: distance along ray
        """
        return Point(self.origin.x + math.cos(self.direction) * distance,
                     self.origin.y + math.sin(self.direction) * distance)

    def ray_cast(self) -> RayCastHit:
        for distance in range(MAX_RAY_DISTANCE):
            point = self.get_point(distance)
            if (point.x // TILE * TILE, point.y // TILE * TILE) in WORLD_MAP:
                return RayCastHit(distance, point)
