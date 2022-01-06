import pygame

from config import *
from ray_casting import ray_casting
from load_image import load_image


"""
Вайман Ангелина:
02.01.2022. Создан класс Render с использованием алгоритма Павлова Тимура
03.01.2022. Создана функция _draw_minimap, _draw_sky
04.01.2022. Доработана фунукция _draw_walls и добавлены текстуры
05.01.2022. Добавлена функция weapon_animation
06.01.2022 Изменена обработка текстур стены
"""

sky_texture = load_image(TEXTURE_FILE, SKY_TEXTURE)
wall_texture = load_image(TEXTURE_FILE, WALL_TEXTURE, color_key=None)


class Render:
    def __init__(self, screen, player, screen_map):
        self.screen = screen
        self.player = player
        self.screen_map = screen_map

    def render(self):
        self._draw_sky()
        self._draw_floor()
        self._draw_walls()
        self._draw_minimap()
        self.player.draw()

    def _draw_floor(self):
        pygame.draw.rect(self.screen, ANTHRACITE, (0, HALF_SCREEN_HEIGHT, SCREEN_WIDTH, HALF_SCREEN_HEIGHT))

    def _draw_sky(self):
        sky_image = pygame.transform.scale(sky_texture, (SCREEN_WIDTH, SCREEN_HEIGHT))
        sky_offset = -10 * math.degrees(self.player.direction) % SCREEN_WIDTH
        self.screen.blit(sky_image, (sky_offset, 0))
        self.screen.blit(sky_image, (sky_offset + SCREEN_WIDTH, 0))
        self.screen.blit(sky_image, (sky_offset - SCREEN_WIDTH, 0))

    # Отрисовка 2.5D
    def _draw_walls(self):
        hits = ray_casting(self.player.pos, self.player.direction)

        for hit_index, hit in enumerate(hits):
            offset = int(hit.offset) % TILE
            distance = hit.distance * math.cos(self.player.direction - hit.angel)
            distance = max(distance, 0.00001)
            projection_height = min(PROJECTION_COEFFICIENT / (distance + 10 ** -10), SCREEN_HEIGHT * 2)
            wall = wall_texture.subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
            wall = pygame.transform.scale(wall, (SCALE, projection_height))
            self.screen.blit(wall, (hit_index * SCALE, HALF_SCREEN_HEIGHT - projection_height // 2))

    def _draw_minimap(self):
        self.screen_map.fill(BLACK)
        x, y = self.player.x / MAP_TILE, self.player.y / MAP_TILE
        cos_a, sin_a = math.cos(self.player.direction), math.sin(self.player.direction)
        pygame.draw.line(self.screen_map, YELLOW, (int(x) // MAP_TILE, int(y) // MAP_TILE),
                         (int(x) // MAP_TILE + 10 * cos_a, int(y) // MAP_TILE + 10 * sin_a), 2)
        pygame.draw.circle(self.screen_map, GREEN, (int(x) // MAP_TILE, int(y) // MAP_TILE), 3)
        for x, y in MINI_MAP:
            pygame.draw.rect(self.screen_map, RED, (x, y, MAP_TILE, MAP_TILE))
        self.screen.blit(self.screen_map,
                         (SCREEN_WIDTH - SCREEN_WIDTH // MAP_TILE + 80, SCREEN_HEIGHT - SCREEN_HEIGHT // MAP_TILE))

