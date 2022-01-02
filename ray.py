from config import *
from point import Point
from utils import check_map

"""
Павлов Тимур 01.01.2021. Написаны классы Ray и RayCastHit 

Использованы алгоритмы написанные Ангелиной Вайман 28.12.2021 и Арсланом Батталовым 29.12.2021

Батталов Арслан 2.01.2022 написаны функции vertical_collision, horizontal_collision, ray_cast
"""


class RayCastHit:
    def __init__(self, distance: float, point: Point, angel: float):
        """
        Structure used to get information back from a raycast
        :param distance: the distance from the ray's origin to the impact point
        :param point: the impact point in world space where the ray hit the collider
        :param angel:
        """
        self.distance = distance
        self.point = point
        self.angel = angel


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

    def ray_cast(self) -> RayCastHit:
        player_x, player_y = self.origin
        cos_a, sin_a = math.cos(self.direction), math.sin(self.direction)
        square_x, square_y = check_map(player_x, player_y)

        x_ver, y_ver, vert_dist = self.vertical_collision(square_x, player_x, player_y, sin_a, cos_a)
        x_hor, y_hor, hor_dist = self.horizontal_collision(square_y, player_x, player_y, sin_a, cos_a)

        if hor_dist > vert_dist:
            return RayCastHit(vert_dist, (x_ver, y_ver), self.direction)

        return RayCastHit(hor_dist, (x_hor, y_hor), self.direction)

    @staticmethod
    def vertical_collision(square_x, player_x, player_y, sin_a, cos_a):
        y_ver, vert_dist = 0, 0
        x_ver, sign_x = (square_x + TILE, 1) if cos_a >= 0 else (square_x, -1)

        for i in range(0, SCREEN_WIDTH, TILE):
            vert_dist = (x_ver - player_x) / cos_a
            y_ver = player_y + vert_dist * sin_a

            if check_map(x_ver + sign_x, y_ver) in WORLD_MAP:
                break

            x_ver += sign_x * TILE

        return x_ver, y_ver, vert_dist

    @staticmethod
    def horizontal_collision(square_y, player_x, player_y, sin_a, cos_a):
        x_hor, hor_dist = 0, 0
        y_hor, sign_y = (square_y + TILE, 1) if sin_a >= 0 else (square_y, -1)

        for i in range(0, SCREEN_HEIGHT, TILE):
            hor_dist = (y_hor - player_y) / sin_a
            x_hor = player_x + hor_dist * cos_a

            if check_map(x_hor, y_hor + sign_y) in WORLD_MAP:
                break

            y_hor += sign_y * TILE

        return x_hor, y_hor, hor_dist
