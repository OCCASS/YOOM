import pygame

from config import *
from hit import RayCastHit, SpriteHit
from load_image import load_image
from ray_casting import ray_casting, sprites_ray_casting
from sprite import MovableSprite

"""
Вайман Ангелина:
02.01.2022. Создан класс Render с использованием алгоритма Павлова Тимура
03.01.2022. Создана функция _draw_minimap, _draw_sky
04.01.2022. Доработана фунукция _draw_walls и добавлены текстуры
05.01.2022. Добавлена функция weapon_animation

Батталов Арслан:
06.01.2022 Изменена обработка текстур стены

Палов Тимур:
08.01.2022. Создана поддержка отрисовки спрайтов
"""

sky_texture = load_image(TEXTURES_PATH, SKY_TEXTURE)
wall_texture = load_image(TEXTURES_PATH, WALL_TEXTURE_1, color_key=None)


class Render:
    def __init__(self, screen, player, screen_map, sprites):
        self.screen = screen
        self.player = player
        self.screen_map = screen_map
        self.sprites = sprites

    def render(self):
        self._draw_sky()
        self._draw_floor()
        self._draw_world()
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
    def _draw_world(self):
        sprite_hits = sprites_ray_casting(self.sprites, self.player.pos, self.player.direction)
        wall_hits = ray_casting(self.player.pos, self.player.direction)
        hits = [*enumerate(sprite_hits), *enumerate(wall_hits)]
        hits = list(sorted(hits, key=lambda i: i[1].distance, reverse=True))

        for hit_index, hit in hits:
            if isinstance(hit, RayCastHit):
                offset = int(hit.offset) % TILE
                distance = hit.distance * math.cos(self.player.direction - hit.angel)
                distance = max(distance, MIN_DISTANCE)
                self._draw_wall(distance, offset, hit_index)
            elif isinstance(hit, SpriteHit):
                sprite = self.sprites[hit.sprite_index]

                if sprite.is_dead:
                    continue
                if isinstance(sprite, MovableSprite):
                    self.sprites[hit.sprite_index].update(self.player)
                if sprite.check_damage(self.player):
                    self.player.damage()

                self.draw_sprite(hit.texture, hit.distance, hit.casted_ray_index)

    def draw_sprite(self, texture, distance, current_ray):
        projection_height = min(PROJECTION_COEFFICIENT / (distance + 10 ** -10), SCREEN_HEIGHT)
        projection_width = projection_height
        sprite_x = current_ray * SCALE - projection_width // 2
        sprite_y = HALF_SCREEN_HEIGHT - projection_height // 2

        texture = pygame.transform.scale(texture, (projection_width, projection_height))
        self.screen.blit(texture, (sprite_x, sprite_y))

    def _draw_wall(self, distance, offset, hit_index):
        projection_height = min(PROJECTION_COEFFICIENT / (distance + 10 ** -10), SCREEN_HEIGHT * 2)
        wall = wall_texture.subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE,
                                       TEXTURE_HEIGHT)
        wall = pygame.transform.scale(wall, (SCALE, projection_height))
        self.screen.blit(wall, (hit_index * SCALE, HALF_SCREEN_HEIGHT - projection_height // 2))

    def _draw_minimap(self):
        self.screen_map.fill(BLACK)
        x, y = self.player.x / MAP_TILE, self.player.y / MAP_TILE
        cos_a, sin_a = math.cos(self.player.direction), math.sin(self.player.direction)
        pygame.draw.line(self.screen_map, YELLOW, (int(x) // MAP_TILE, int(y) // MAP_TILE),
                         (int(x) // MAP_TILE + MIINIMAP_OFFSET * cos_a, int(y) // MAP_TILE + MIINIMAP_OFFSET * sin_a),
                         2)
        pygame.draw.circle(self.screen_map, GREEN, (int(x) // MAP_TILE, int(y) // MAP_TILE), 3)
        for x, y in MINI_MAP:
            pygame.draw.rect(self.screen_map, RED, (x, y, MAP_TILE, MAP_TILE))
        self.screen.blit(self.screen_map,
                         (SCREEN_WIDTH - SCREEN_WIDTH // MAP_TILE + 80, SCREEN_HEIGHT - SCREEN_HEIGHT // MAP_TILE))
