from config import *
from point import Point
from ray import Ray, RayCastHit

"""
Вайман Ангелина 28.12.2021. Создана функция ray_casting.

Павлов Тимур 28.12.2021. Доработка функции ray_casting

Батталов Арслан 29.12.2021 Добавлена функция collide_nearest_wall
(пока функционирует некорректно)

Батталов Арслан 29.12.2021 Изменена функция collide_nearest_wall
Доработка эффективного алгоритма

Батталов Арслан 08.01.2022 Добавлена поддержа разных текстур стен
"""


def ray_casting(player_pos: Point, player_angle: float) -> (list[RayCastHit], str):
    current_angle: float = player_angle - HALF_FOV
    ray_cast_hits: list[RayCastHit] = []
    wall_char_list = []
    for _ in range(RAYS_AMOUNT):
        ray = Ray(player_pos, current_angle, MAX_VIEW_DISTANCE)

        ray_cast_hit, wall_char = ray.ray_cast()
        ray_cast_hits.append(ray_cast_hit)
        wall_char_list.append(wall_char)

        current_angle += DELTA_ANGLE

    return ray_cast_hits, wall_char_list
