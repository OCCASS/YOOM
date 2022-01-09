import collections

import pygame.time

from config import *
from load_image import load_image
from point import Point
from ray import Ray
from sound import Sounds
from utils import get_distance, world_pos2cell, angle_between_vectors, compare_deque

"""
Павлов Тимур 08.01.2022. Создан класс Sprite и функция create_sprites
Павлов Тимур 09.01.2022. Создан класс MovableSprite, создана функция sprites_update, is_win, улучшен алгоритм поиска 
    пути и дамага игрока
Павлов Тимур 09.01.2022. Добавлена анимация спрайтов
Павлов Тимур 09.01.2022. Добавлена анимация статичным спрайтам
"""

sprite_textures = {
    '3': {
        'default': collections.deque(
            [load_image(TEXTURES_PATH, f'devil/{i}.png') for i in range(DEVIL_ANIMATION_FRAMES_COUNT)]),
        'dead': load_image(TEXTURES_PATH, 'devil/dead.png')
    },
    '4': {
        'default': collections.deque(
            [load_image(TEXTURES_PATH, f'pin/{i}.png') for i in range(PIN_ANIMATION_FRAMES_COUNT)]),
        'dead': load_image(TEXTURES_PATH, 'pin/dead.png')
    },
    '5': {
        'default': collections.deque(
            [load_image(TEXTURES_PATH, f'flame/{i}.png') for i in range(FLAME_ANIMATION_FRAMES_COUNT)]),
        'dead': load_image(TEXTURES_PATH, 'flame/dead.png')
    },
    '6': {
        'default': collections.deque(
            [load_image(TEXTURES_PATH, f'devil_yellow/{i}.png') for i in range(DEVIL_YELLOW_ANIMATION_FRAMES_COUNT)]),
        'dead': load_image(TEXTURES_PATH, 'devil_yellow/dead.png')
    },
    '7': {
        'default': collections.deque(
            [load_image(TEXTURES_PATH, f'aerial/{i}.png') for i in range(AERIAL_ANIMATION_FRAMES_COUNT)]
        ),
        'dead': load_image(TEXTURES_PATH, 'aerial/dead.png')
    },
    '8': {
        'default': collections.deque(
            [load_image(TEXTURES_PATH, f'skull/{i}.png') for i in range(SKULL_ANIMATION_FRAMES_COUNT)]
        ),
        'dead': load_image(TEXTURES_PATH, 'skull/dead.png')
    },
    '9': {
        'default': collections.deque(
            [load_image(TEXTURES_PATH, f'imp/{i}.png') for i in range(IMP_ANIMATION_FRAMES_COUNT)]),
        'dead': load_image(TEXTURES_PATH, 'imp/dead.png'),
        'attack': collections.deque(
            [load_image(TEXTURES_PATH, f'imp/attack/{i}.png') for i in range(IMP_ATTACK_ANIMATION_FRAMES_COUNT)])
    }
}


def sprites_update(sprites, player):
    for sprite_index in range(len(sprites)):
        sprite = sprites[sprite_index]
        sprite.update()
        if isinstance(sprite, MovableSprite):
            sprites[sprite_index].move_to(player.x, player.y)

            if sprite.check_damage(player):
                Sounds.damage()
                Sounds.get_damage(3)

                sprites[sprite_index].attack()
                player.damage(sprite.damage)
            else:
                sprites[sprite_index].stop_attack()

    return sprites


class StaticSprite:
    def __init__(self, animation_list, dead_texture, pos, vertical_scale=1.0, vertical_shift=0.0, destroyed=False,
                 animation_speed=SPRITE_ANIMATION_SPEED):
        self.dead_texture = dead_texture
        self.pos = pos
        self.is_dead = False
        self.vertical_scale = vertical_scale
        self.vertical_shift = vertical_shift
        self.destroyed = destroyed

        self.default_animation_list = animation_list.copy()
        self.animation_list = animation_list
        self.animation_count = 0

        self.texture = self.animation_list[0].copy()
        self.default_texture = self.texture.copy()

        self.animation_speed = animation_speed

    def kill(self):
        self.is_dead = True

    def reset(self):
        self.is_dead = False

    def get_texture(self):
        if not self.destroyed:
            return self.animation_list[0]
        else:
            if self.is_dead:
                return self.dead_texture
            else:
                return self.animation_list[0]

    def update(self):
        self.animation_count += 1
        if self.animation_count == self.animation_speed:
            self.animation_list.rotate(-1)
            self.animation_count = 0

    def copy(self):
        return StaticSprite(self.animation_list, self.dead_texture, self.pos, self.vertical_scale, self.vertical_shift,
                            self.destroyed, self.animation_speed)


class MovableSprite(StaticSprite):
    def __init__(self, animation_list, dead_texture, pos, speed, damage, hit_distance, vertical_scale=1.0,
                 vertical_shift=0.0, attack_animation_list=None, animation_speed=SPRITE_ANIMATION_SPEED):
        super(MovableSprite, self).__init__(animation_list, dead_texture, pos, vertical_scale, vertical_shift,
                                            animation_speed)
        self.damage = damage

        self._speed = speed
        self._hit_distance = hit_distance
        self._delay = 0
        self._attack = False
        self._attack_animation_list = None if attack_animation_list is None else attack_animation_list.copy()

    def attack(self):
        if self._attack_animation_list and not self._attack:
            self.animation_list = self._attack_animation_list.copy()
            self.animation_list.rotate(-1)
            self.animation_count = 0

        self._attack = True

    def stop_attack(self):
        if self._attack_animation_list and self._attack:
            if compare_deque(self.animation_list, self._attack_animation_list):
                self.animation_list = self.default_animation_list.copy()
                self.animation_count = 0
                self._attack = False
            else:
                return
        else:
            self._attack = False

    def full_update(self, player):
        self.move_to(player.x, player.y)
        super(MovableSprite, self).update()

    def get_texture(self):
        if self.is_dead:
            return self.dead_texture
        else:
            return self.animation_list[0]

    def copy(self):
        return MovableSprite(self.animation_list, self.dead_texture, self.pos, self._speed, self.damage,
                             self._hit_distance, self.vertical_scale, self.vertical_shift, self._attack_animation_list,
                             self.animation_speed)

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
            next_x = self.pos[0] + move_coefficient_x * self._speed
            next_y = self.pos[1] + move_coefficient_y * self._speed
            cell_x, cell_y = world_pos2cell(next_x, next_y)
            if (cell_x * TILE, cell_y * TILE) not in WORLD_MAP:
                self.pos = [next_x, next_y]

    def check_damage(self, player):
        self._delay += pygame.time.get_ticks() / 1000
        distance_to_player = get_distance(*self.pos, player.x, player.y)
        ray = Ray(Point(*self.pos), self._get_angel_to_player(player), MAX_VIEW_DISTANCE)
        ray_cast = ray.ray_cast()
        ray_cast_distance = ray_cast.distance
        if distance_to_player <= self._hit_distance \
                and distance_to_player <= ray_cast_distance \
                and self._delay >= SPRITE_DAMAGE_DELAY and not self.is_dead:
            self._delay = 0
            return True
        return False


movable_sprites_dict = {
    '3': MovableSprite(sprite_textures['3']['default'], sprite_textures['3']['dead'], None, speed=2, damage=5,
                       hit_distance=SPRITE_HIT_DISTANCE * 2),
    '4': MovableSprite(sprite_textures['4']['default'], sprite_textures['4']['dead'], None, speed=1, damage=3,
                       hit_distance=SPRITE_HIT_DISTANCE * 4, vertical_scale=.5),
    '6': MovableSprite(sprite_textures['6']['default'], sprite_textures['6']['dead'], None, speed=1, damage=5,
                       hit_distance=SPRITE_HIT_DISTANCE * 4),
    '7': MovableSprite(sprite_textures['7']['default'], sprite_textures['7']['dead'], None, speed=1, damage=0.5,
                       hit_distance=SPRITE_HIT_DISTANCE * 6),
    '8': MovableSprite(sprite_textures['8']['default'], sprite_textures['8']['dead'], None, speed=2, damage=5,
                       hit_distance=SPRITE_HIT_DISTANCE * 1.5, vertical_scale=2),
    '9': MovableSprite(sprite_textures['9']['default'], sprite_textures['9']['dead'], None, speed=2, damage=5,
                       hit_distance=SPRITE_HIT_DISTANCE * 1.5, attack_animation_list=sprite_textures['9']['attack'])
}

static_sprites_dict = {
    '5': StaticSprite(sprite_textures['5']['default'], sprite_textures['5']['dead'], None, 0.7, 20),
}


def create_sprites(world_map) -> list[StaticSprite]:
    sprites = []
    for row_index, row in enumerate(world_map):
        for col_index, el in enumerate(row):
            if el in SPRITE_CHARS:
                x, y = col_index * TILE + TILE // 2, row_index * TILE + TILE // 2
                if el in STATIC_SPRITES:
                    sprite = static_sprites_dict[el].copy()
                elif el in MOVABLE_SPRITES:
                    sprite = movable_sprites_dict[el].copy()

                if el in SPRITE_CHARS:
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
