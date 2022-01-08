import numba
import math
from config import TILE

"""
Павлов Тимур 08.01.2022. Создана функция get_distance, world_pos2cell
"""


@numba.njit(fastmath=True, cache=True)
def get_distance(x0, y0, x1, y1):
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)


@numba.njit(fastmath=True, cache=True)
def world_pos2cell(x, y):
    return int(x // TILE), int(y // TILE)
