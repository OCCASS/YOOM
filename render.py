import pygame
import collections

from config import *
from ray_casting import ray_casting
from load_image import load_image

"""
Вайман Ангелина:
02.01.2022. Создан класс Render с использованием алгоритма Павлова Тимура
03.01.2022. Создана функция _draw_minimap, _draw_sky
04.01.2022. Доработана фунукция _draw_walls и добавлены текстуры
05.01.2022. Добавлена функция weapon_animation
"""

sky_texture = load_image(SKY_TEXTURE)
wall_texture = load_image(WALL_TEXTURE)
sprite_gun_base = load_image(GUN_BASE)
sprite_gun_base = pygame.transform.scale(sprite_gun_base, WEAPON_SIZE)
animations_sprites_list = collections.deque([load_image(f'gun_{i}.png') for i in range(20)])


class Render:
    def __init__(self, screen, player, screen_map):
        self.screen = screen
        self.player = player
        self.screen_map = screen_map
        self.shot_animation_count, self.length_count = 0, 0
        self.weapon_pos = (HALF_SCREEN_WIDTH - WEAPON_SIZE[0] // 2, SCREEN_HEIGHT - WEAPON_SIZE[1])

    def render(self):
        self._draw_sky()
        self._draw_floor()
        self._draw_walls()
        self.weapon_animation()
        self._draw_minimap()

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
            wall = wall_texture.subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
            wall = pygame.transform.scale(wall, (SCALE, projection_height))
            self.screen.blit(wall, (hit_index * SCALE, HALF_SCREEN_HEIGHT - projection_height // 2))

    def _draw_minimap(self):
        self.screen_map.fill(BLACK)
        x, y = self.player.x / MAP_TILE, self.player.y / MAP_TILE
        cos_a, sin_a = math.cos(self.player.direction), math.sin(self.player.direction)
        pygame.draw.line(self.screen_map, YELLOW, (int(x) // MAP_TILE, int(y) // MAP_TILE),
                         (int(x) // MAP_TILE + 10 * cos_a, int(y) // MAP_TILE + 10 * sin_a), 2)
        pygame.draw.circle(self.screen_map, RED, (int(x) // MAP_TILE, int(y) // MAP_TILE), 3)
        for x, y in MINI_MAP:
            pygame.draw.rect(self.screen_map, SKYBLUE, (x, y, MAP_TILE, MAP_TILE))
        self.screen.blit(self.screen_map,
                         (SCREEN_WIDTH - SCREEN_WIDTH // MAP_TILE + 80, SCREEN_HEIGHT - SCREEN_HEIGHT // MAP_SCALE))

    def weapon_animation(self):
        if self.player.shot:
            shot_sprite = animations_sprites_list[0]
            shot_sprite = pygame.transform.scale(shot_sprite, WEAPON_SIZE)
            self.screen.blit(shot_sprite, self.weapon_pos)
            self.shot_animation_count += 1
            if self.shot_animation_count == ANIMATION_SPEED:
                animations_sprites_list.rotate(-1)
                self.shot_animation_count = 0
                self.length_count += 1
            if self.length_count == len(animations_sprites_list):
                self.player.shot = False
                self.length_count = 0
        else:
            self.screen.blit(sprite_gun_base, self.weapon_pos)
