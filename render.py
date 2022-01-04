import pygame

from config import *
from ray_casting import ray_casting
from load_image import load_image

"""
Вайман Ангелина:
02.01.2022. Создан класс Render с использованием алгоритма Павлова Тимура
03.01.2022. Создана функция _draw_minimap, _draw_sky
04.01.2022. Доработано фунукция _draw_walls и добавлены текстуры
"""

sky_texture = load_image(SKY_TEXTURE)
wall_texture = load_image(WALL_TEXTURE)


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

    def _draw_player(self):
        player_pos = self.player.pos
        pygame.draw.circle(self.screen, BLACK, (player_pos.x, player_pos.y), 5)
        hits = ray_casting(player_pos, self.player.direction)

        for hit in hits:
            hit_point = hit.point
            pygame.draw.line(self.screen, WHITE, player_pos, hit_point)

    def _draw_floor(self):
        pygame.draw.rect(self.screen, BRICK, (0, HALF_SCREEN_HEIGHT, SCREEN_WIDTH, HALF_SCREEN_HEIGHT))

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
            wall = wall_texture.convert().subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
            wall = pygame.transform.scale(wall, (SCALE, projection_height))
            self.screen.blit(wall, (hit_index * SCALE, HALF_SCREEN_HEIGHT - projection_height // 2))

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

    def _draw_minimap(self):
        self.screen_map.fill(BLACK)
        map_x, map_y = self.player.x / MAP_TILE, self.player.y / MAP_TILE
        cos_a, sin_a = math.cos(self.player.direction), math.sin(self.player.direction)
        pygame.draw.line(self.screen_map, YELLOW, (map_x, map_y), (map_x + 10 * cos_a, map_y + 10 * sin_a), 2)
        pygame.draw.circle(self.screen_map, RED, (int(map_x), int(map_y)), 3)
        for x, y in MINI_MAP:
            pygame.draw.rect(self.screen_map, SKYBLUE, (x, y, MAP_TILE, MAP_TILE))
        self.screen.blit(self.screen_map, (0, SCREEN_HEIGHT - SCREEN_HEIGHT // MAP_SCALE))
