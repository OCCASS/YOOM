import pygame.time

from config import *
from load_image import load_image
from point import Point
from ray import Ray
from utils import get_distance, world_pos2cell, angle_between_vectors

"""
Павлов Тимур 08.01.2022. Создан класс Sprite и функция create_sprites
Павлов Тимур 09.01.2022. Создан класс MovableSprite
"""

sprite_textures = {
    '3': load_image(TEXTURES_PATH, 'plant.png'),
    '4': load_image(TEXTURES_PATH, 'barrel.png'),
    '5': load_image(TEXTURES_PATH, 'enemy.png'),
    '6': load_image(TEXTURES_PATH, 'devil.png')
}


def sprites_update(sprites, player):
    for i in range(len(sprites)):
        sprite = sprites[i]
        if isinstance(sprite, MovableSprite):
            sprites[i].move_to(player.x, player.y)

            if sprite.check_damage(player):
                player.damage(sprite.damage)

    return sprites


class Sprite:
    def __init__(self, texture, pos):
        self.texture = texture
        self.pos = pos
        self.is_dead = False


class MovableSprite(Sprite):
    def __init__(self, texture, pos, speed, damage, hit_distance):
        super(MovableSprite, self).__init__(texture, pos)
        self.speed = speed
        self.damage = damage
        self.hit_distance = hit_distance
        self._delay = 0

    def update(self, player):
        self.move_to(player.x, player.y)

    def _get_angel_to_player(self, player):
        dx, dy = player.x - self.pos[0], player.y - self.pos[1]
        direction = angle_between_vectors(RIGHT_VECTOR, (dx, dy, 0))

        if player.y < self.pos[1]:
            direction = 2 * math.pi - direction

        return -direction

    def move_to(self, to_x, to_y):
        distance = get_distance(to_x, to_y, *self.pos)

        if abs(distance) > TILE * 2:
            dx, dy = self.pos[0] - to_x, self.pos[1] - to_y
            move_coefficient_x, move_coefficient_y = 1 if dx < 0 else -1, 1 if dy < 0 else -1
            next_x = self.pos[0] + move_coefficient_x * self.speed
            next_y = self.pos[1] + move_coefficient_y * self.speed

            cell_x, cell_y = world_pos2cell(next_x, next_y)
            # if (cell_x * TILE, cell_y * TILE) not in WORLD_MAP:
            self.pos = [next_x, next_y]

    def check_damage(self, player):
        self._delay += pygame.time.get_ticks() / 1000
        distance_to_player = get_distance(*self.pos, player.x, player.y)

        ray = Ray(Point(*self.pos), self._get_angel_to_player(player), MAX_VIEW_DISTANCE)
        ray_cast = ray.ray_cast()
        ray_cast_distance = ray_cast.distance

        if distance_to_player <= self.hit_distance \
                and distance_to_player <= ray_cast_distance \
                and self._delay >= SPRITE_DAMAGE_DELAY:
            self._delay = 0
            return True

        return False


sprites_dict = {
    '5': MovableSprite(sprite_textures['5'], None, 2, 2, SPRITE_HIT_DISTANCE * 3),
    '6': MovableSprite(sprite_textures['6'], None, 1, 3, SPRITE_HIT_DISTANCE // 2)
}


def create_sprites(world_map) -> list[Sprite]:
    sprites = []

    for row_index, row in enumerate(world_map):
        for col_index, el in enumerate(row):
            if el in SPRITE_CHARS:
                x, y = col_index * TILE + TILE // 2, row_index * TILE + TILE // 2
                texture = sprite_textures[el]

                if el in STATIC_SPRITES:
                    sprite = Sprite(texture, (x, y))
                    sprites.append(sprite)
                elif el in MOVABLE_SPRITES:
                    sprite = sprites_dict[el]
                    sprite.pos = (x, y)
                    sprites.append(sprite)

    return sprites


def is_win(sprites):
    for sprite in sprites:
        if isinstance(sprite, MovableSprite):
            if not sprite.is_dead:
                return False

    return True
