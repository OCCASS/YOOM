import math

import numba
import numpy

from config import TILE

"""
Павлов Тимур 08.01.2022. Создана функция get_distance, world_pos2cell
Павлов Тимур 09.01.2022. Создана функция is_game_over, unit_vector, angel_between_vectors, world_pos2tile
"""


@numba.njit(fastmath=True, cache=True)
def get_distance(x0, y0, x1, y1):
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)


@numba.njit(fastmath=True, cache=True)
def world_pos2cell(x, y):
    return int(x // TILE), int(y // TILE)


@numba.njit(fastmath=True, cache=True)
def world_pos2tile(x, y):
    cx, cy = world_pos2cell(x, y)
    return cx * TILE, cy * TILE


def compare_deque(d1, d2):
    if len(d1) != len(d2):
        return False

    for i, j in zip(d1, d2):
        if i != j:
            return False

    return True


def is_game_over(player):
    if player.health <= 0:
        return True


def unit_vector(vector):
    return vector / numpy.linalg.norm(vector)


def angle_between_vectors(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return numpy.arccos(numpy.clip(numpy.dot(v1_u, v2_u), -1.0, 1.0))
