from config import *

"""
Вайман Ангелина 28.12.2021. Создана функция ray_casting.

Павлов Тимур 28.12.2021. Доработка функции ray_casting

Батталов Арслан 29.12.2021 Добавлена функция collide_nearest_wall
(пока функционирует некорректно)

Батталов Арслан 29.12.2021 Измененена функция collide_nearest_wall
Доработка эффективного алгоритма
"""


def ray_casting(player_pos, player_angle):
    cur_angle = player_angle - HALF_FOV
    points = []
    # distance_to_edges = edges_distance(player_pos)
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


