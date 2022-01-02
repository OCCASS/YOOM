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
"""


def ray_casting(player_pos: Point, player_angle: float) -> list[RayCastHit]:
    current_angle: float = player_angle - HALF_FOV
    ray_cast_hits: list[RayCastHit] = []
    for _ in range(RAYS_AMOUNT):
        ray = Ray(player_pos, current_angle, MAX_RAY_DISTANCE)

        ray_cast_hit = ray.ray_cast()
        ray_cast_hits.append(ray_cast_hit)

        current_angle += DELTA_ANGLE

    return ray_cast_hits
