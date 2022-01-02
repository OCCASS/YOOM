import pygame

from ray_casting import ray_casting
from utils import get_color_depend_distance
from config import *

"""
Вайман Ангелина 02.01.2022. Создан класс Render с использованием алгоритма Павлова Тимура
"""


class Render:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        # self.texture = pygame.load('texture/wall_texture1.png').convert()

    def _draw_player(self):
        player_pos = self.player.pos
        pygame.draw.circle(self.screen, BLACK, (player_pos.x, player_pos.y), 5)
        hits = ray_casting(player_pos, self.player.direction)

        for hit in hits:
            hit_point = hit.point
            pygame.draw.line(self.screen, 'white', player_pos, hit_point)

    def _draw_floor(self):
        pygame.draw.rect(self.screen, DARKGREY, (0, HALF_SCREEN_HEIGHT, SCREEN_WIDTH, HALF_SCREEN_HEIGHT))

    # Отрисовка 2.5D
    def _draw_walls(self):
        hits = ray_casting(self.player.pos, self.player.direction)

        for hit_index, hit in enumerate(hits):
            distance = hit.distance * math.cos(self.player.direction - hit.angel)
            projection_height = min(PROJECTION_COEFFICIENT / (distance + 10 ** -10), SCREEN_HEIGHT * 2)

            color = get_color_depend_distance(distance)
            pygame.draw.rect(self.screen, color,
                             (hit_index * SCALE, HALF_SCREEN_HEIGHT - projection_height // 2, SCALE, projection_height))

    def _draw_map(self):
        for row_index, row in enumerate(MAP):
            for char_index, char in enumerate(row):
                if char in WALL_CHARS:
                    if char == WALL_CHARS[0]:
                        color = ORANGE
                    elif char == WALL_CHARS[1]:
                        color = PURPLE
                    else:
                        color = BLACK

                    x, y = char_index * TILE, row_index * TILE
                    pygame.draw.rect(self.screen, color, (x, y, TILE, TILE))
