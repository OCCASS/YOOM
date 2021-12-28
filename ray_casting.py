from config import HALF_FOV, RAYS_AMOUNT, DELTA_ANGLE, WORLD_MAP, TILE, MAX_RAY_DISTANCE
import math

"""
Вайман Ангелина 28.12.2021. Создана функция ray_casting.

Павлов Тимур 28.12.2021. Доработка функции ray_casting
"""


def ray_casting(player_pos, player_angle):
    cur_angle = player_angle - HALF_FOV

    points = []
    for ray in range(RAYS_AMOUNT):
        collision_pos = collide_nearest_wall(player_pos, cur_angle)
        points.append(collision_pos)

        cur_angle += DELTA_ANGLE

    return points


def collide_nearest_wall(start_pos: tuple, angel: float) -> tuple[float, float]:
    start_x, start_y = start_pos
    cos_a, sin_a = math.cos(angel), math.sin(angel)

    for distance in range(MAX_RAY_DISTANCE):
        x = start_x + distance * cos_a
        y = start_y + distance * sin_a

        if (x // TILE * TILE, y // TILE * TILE) in WORLD_MAP:
            return x, y
