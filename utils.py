import numba
import math

"""
Павлов Тимур 08.01.2022. Создана функция get_distance
"""


@numba.njit(fastmath=True, cache=True)
def get_distance(x0, y0, x1, y1):
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)
