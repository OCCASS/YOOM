from config import *
from ray import Ray, RayCastHit
from point import Point

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

# def collide_nearest_wall(start_pos: tuple, angle: float, distance_to_edges: tuple) -> tuple[float, float]:
#     start_x, start_y = start_pos
#     cos_a, sin_a = math.cos(angle), math.sin(angle)
#     vert_dist, hor_dist = 0, 0
#
#     for vertical in range(0, SCREEN_WIDTH, TILE):
#         if cos_a > 0:
#             vert_dist = distance_to_edges[RIGHT] / cos_a
#         elif cos_a < 0:
#             vert_dist = distance_to_edges[LEFT] / -cos_a
#
#         x_ver, y_ver = start_x + vert_dist * cos_a, start_y + vert_dist * sin_a
#         if (x_ver // TILE * TILE, y_ver // TILE * TILE) in WORLD_MAP:
#             break
#
#     for point in range(0, SCREEN_HEIGHT, TILE):
#         if sin_a > 0:
#             hor_dist = distance_to_edges[BOTTOM] / sin_a
#         elif sin_a < 0:
#             hor_dist = distance_to_edges[TOP] / -sin_a
#
#         x_hor, y_hor = start_x + hor_dist * cos_a, start_y + hor_dist * sin_a
#         if (x_hor // TILE * TILE, y_hor // TILE * TILE) in WORLD_MAP:
#             break
#
#     if hor_dist > vert_dist:
#         return x_ver, y_ver
#     return x_hor, y_hor
#
#
# def edges_distance(pos):
#     x, y = pos
#     right = TILE - (x - x // TILE * TILE)
#     left = x - x // TILE * TILE
#     bottom = TILE - (y - y // TILE * TILE)
#     top = y - y // TILE * TILE
#     return right, left, bottom, top
