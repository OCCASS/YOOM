from config import *
from point import Point
from hit import RayCastHit

"""
Павлов Тимур 01.01.2021. Написаны классы Ray и RayCastHit 

Использованы алгоритмы написанные Ангелиной Вайман 28.12.2021 и Арсланом Батталовым 29.12.2021

Батталов Арслан 2.01.2022 написаны функции vertical_collision, horizontal_collision, ray_cast

Вайман Ангелина 04.01.2022. Доработаны функции vertical_collision, horizontal_collision, ray_cast

Батталов Арслан 04.01.2022. Исправлена ошибка деления на ноль в функции ray_cast

Батталов Арслан 08.01.2022. Исправлена ошибка прорисовки, добавлена поддержка различных текстур стен
"""


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

    @staticmethod
    def _check_map(x, y):
        return x // TILE * TILE, y // TILE * TILE

    def ray_cast(self):
        player_x, player_y = self.origin
        cos_a, sin_a = math.cos(self.direction), math.sin(self.direction)
        square_x, square_y = self._check_map(player_x, player_y)

        cos_a = 10 ** -10 if cos_a == 0 else cos_a
        sin_a = 10 ** -10 if sin_a == 0 else sin_a

        x_ver, y_ver, vert_dist, ver_offset, wall_num = self.vertical_collision(square_x, player_x, player_y, sin_a,
                                                                                cos_a)
        x_hor, y_hor, hor_dist, hor_offset, wall_num = self.horizontal_collision(square_y, player_x, player_y, sin_a,
                                                                                 cos_a)

        if hor_dist > vert_dist:
            return RayCastHit(vert_dist, (x_ver, y_ver), self.direction, ver_offset), wall_num
        return RayCastHit(hor_dist, (x_hor, y_hor), self.direction, hor_offset), wall_num

    def vertical_collision(self, square_x, player_x, player_y, sin_a, cos_a):
        y_ver, vert_dist, wall_num = 0, 0, '2'
        x_ver, sign_x = (square_x + TILE, 1) if cos_a >= 0 else (square_x, -1)
        for i in range(0, MAX_VERTICAL_RAY_DISTANCE, TILE):
            vert_dist = (x_ver - player_x) / cos_a
            y_ver = player_y + vert_dist * sin_a
            tile_pos = self._check_map(x_ver + sign_x, y_ver)
            if tile_pos in WORLD_MAP.keys():
                wall_num = WORLD_MAP[tile_pos]
                break
            x_ver += sign_x * TILE
        offset = y_ver
        return x_ver, y_ver, vert_dist, offset, wall_num

    def horizontal_collision(self, square_y, player_x, player_y, sin_a, cos_a):
        x_hor, hor_dist, wall_num = 0, 0, '2'
        y_hor, sign_y = (square_y + TILE, 1) if sin_a >= 0 else (square_y, -1)
        for i in range(0, MAX_HORIZONTAL_RAY_DISTANCE, TILE):
            hor_dist = (y_hor - player_y) / sin_a
            x_hor = player_x + hor_dist * cos_a
            tile_pos = self._check_map(x_hor, y_hor + sign_y)
            if tile_pos in WORLD_MAP.keys():
                wall_num = WORLD_MAP[tile_pos]
                break
            y_hor += sign_y * TILE
        offset = x_hor
        return x_hor, y_hor, hor_dist, offset, wall_num
