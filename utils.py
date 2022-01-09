import numba
import math
from config import TILE, MAP_SIZE, WALLS_MAP

"""
Павлов Тимур 08.01.2022. Создана функция get_distance, world_pos2cell
"""


@numba.njit(fastmath=True, cache=True)
def get_distance(x0, y0, x1, y1):
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)


@numba.njit(fastmath=True, cache=True)
def world_pos2cell(x, y):
    return int(x // TILE), int(y // TILE)


@numba.njit(fastmath=True, cache=True)
def is_cell_a_wall(x, y):
    if 0 <= x < MAP_SIZE[0] and 0 <= y < MAP_SIZE[1]:
        return bool(WALLS_MAP[y][x])


def is_game_over(player, sprites):
    if player.health == 0:
        return True

    for sprite in sprites:
        if not sprite.is_dead:
            return False

    return True
