import pygame.time

from config import *
from load_image import load_image
from point import Point
from ray import Ray
from sound import SoundEffect
from utils import get_distance, world_pos2cell, angle_between_vectors

"""
Павлов Тимур 08.01.2022. Создан класс Sprite и функция create_sprites
Павлов Тимур 09.01.2022. Создан класс MovableSprite, создана функция sprites_update, is_win, улучшен алгоритм поиска 
    пути и дамага игрока
"""

sprite_textures = {
    '3': {
        'default': load_image(TEXTURES_PATH, 'devil/default.png'),
        'dead': load_image(TEXTURES_PATH, 'devil/dead.png')
    },
    '4': {
        'default': load_image(TEXTURES_PATH, 'solider/default.png'),
        'dead': load_image(TEXTURES_PATH, 'solider/dead.png')
    },
}


def sprites_update(sprites, player):
    for i in range(len(sprites)):
        sprite = sprites[i]
        if isinstance(sprite, MovableSprite):
            sprites[i].move_to(player.x, player.y)

            if sprite.check_damage(player):
                SoundEffect(DAMAGE_SOUND).play_sound()
                player.damage(sprite.damage)

    return sprites


class Sprite:
    def __init__(self, texture, dead_texture, pos, scale=1.0):
        self.texture = texture
        self.default_texture = self.texture.copy()
        self.dead_texture = dead_texture
        self.pos = pos
        self.is_dead = False
        self.scale = scale

    def kill(self):
        self.is_dead = True
        self.texture = self.dead_texture.copy()

    def reset(self):
        self.is_dead = False
        self.texture = self.default_texture.copy()


class MovableSprite(Sprite):
    def __init__(self, texture, dead_texture, pos, speed, damage, hit_distance, scale=1.0):
        super(MovableSprite, self).__init__(texture, dead_texture, pos, scale)
        self.speed = speed
        self.damage = damage
        self.hit_distance = hit_distance
        self._delay = 0

    def update(self, player):
        self.move_to(player.x, player.y)

    def copy(self):
        return MovableSprite(self.default_texture, self.dead_texture, self.pos, self.speed, self.damage,
                             self.hit_distance)

    def _get_angel_to_player(self, player):
        dx, dy = player.x - self.pos[0], player.y - self.pos[1]
        direction = angle_between_vectors(RIGHT_VECTOR, (dx, dy, 0))
        if player.y < self.pos[1]:
            direction = 2 * math.pi - direction
        return -direction

    def move_to(self, to_x, to_y):
        if not self.is_dead:
            dx, dy = self.pos[0] - to_x, self.pos[1] - to_y
            move_coefficient_x, move_coefficient_y = 1 if dx < 0 else -1, 1 if dy < 0 else -1
            next_x = self.pos[0] + move_coefficient_x * self.speed
            next_y = self.pos[1] + move_coefficient_y * self.speed
            cell_x, cell_y = world_pos2cell(next_x, next_y)
            if (cell_x * TILE, cell_y * TILE) not in WORLD_MAP:
                self.pos = [next_x, next_y]

    def check_damage(self, player):
        self._delay += pygame.time.get_ticks() / 1000
        distance_to_player = get_distance(*self.pos, player.x, player.y)
        ray = Ray(Point(*self.pos), self._get_angel_to_player(player), MAX_VIEW_DISTANCE)
        ray_cast = ray.ray_cast()
        ray_cast_distance = ray_cast.distance
        if distance_to_player <= self.hit_distance \
                and distance_to_player <= ray_cast_distance \
                and self._delay >= SPRITE_DAMAGE_DELAY and not self.is_dead:
            self._delay = 0
            return True
        return False


sprites_dict = {
    '3': MovableSprite(sprite_textures['3']['default'], sprite_textures['3']['dead'], None, speed=2, damage=5,
                       hit_distance=SPRITE_HIT_DISTANCE * 2),
    '4': MovableSprite(sprite_textures['4']['default'], sprite_textures['4']['dead'], None, speed=1, damage=3,
                       hit_distance=SPRITE_HIT_DISTANCE * 5, scale=.5)
}


def create_sprites(world_map) -> list[Sprite]:
    sprites = []
    for row_index, row in enumerate(world_map):
        for col_index, el in enumerate(row):
            if el in SPRITE_CHARS:
                x, y = col_index * TILE + TILE // 2, row_index * TILE + TILE // 2
                texture = sprite_textures[el]
                if el in STATIC_SPRITES:
                    sprite = Sprite(texture['default'], texture['dead'], (x, y))
                    sprite.reset()
                    sprites.append(sprite)
                elif el in MOVABLE_SPRITES:
                    sprite = sprites_dict[el].copy()
                    sprite.pos = (x, y)
                    sprite.reset()
                    sprites.append(sprite)
    return sprites


def is_win(sprites):
    sprites = list(filter(lambda i: isinstance(i, MovableSprite), sprites))
    for sprite in sprites:
        if not sprite.is_dead:
            return False

    return True
