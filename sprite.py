import math
from copy import deepcopy

from config import TILE, SPRITE_CHARS, MAP, TEXTURES_PATH, STATIC_SPRITES, MOVABLE_SPRITES
from load_image import load_image
from point import Point
from utils import world_pos2cell, get_distance
from wave_algorithm import *
from ray import Ray
import numpy

"""
Павлов Тимур 08.01.2022. Создан класс Sprite и функция create_sprites
Павлов Тимур 09.01.2022. Создан класс MovableSprite
"""

sprite_textures = {
    '3': load_image(TEXTURES_PATH, 'plant.png'),
    '4': load_image(TEXTURES_PATH, 'barrel.png'),
    '5': load_image(TEXTURES_PATH, 'enemy.png')
}
sprite_speed = 5


class Sprite:
    def __init__(self, texture, pos):
        self.texture = texture
        self.pos = self.x, self.y = list(pos)
        self.is_dead = False
        self.hit_distance = 70

    def check_damage(self, player):
        distance_to_player = get_distance(*self.pos, player.x, player.y)

        if distance_to_player <= self.hit_distance:
            return True

        return False


class MovableSprite(Sprite):
    def __init__(self, texture, pos, speed):
        super(MovableSprite, self).__init__(texture, pos)
        self.speed = speed

        self._route = []
        self._previous_to_x, self._previous_to_y = -1, -1
        self._move_x_coefficient, self._move_y_coefficient = 0, 0

    @staticmethod
    def _get_clean_board():
        return [[0 for _ in range(MAP_SIZE[0])] for _ in range(MAP_SIZE[1])]

    def move_to(self, to_x, to_y):
        to_x, to_y = world_pos2cell(to_x, to_y)
        from_x, from_y = world_pos2cell(*self.pos)

        if self._previous_to_x != to_x or self._previous_to_y != to_y:
            self._route = numpy.array([])

        # If not route, create new route
        if self._route is None or numpy.array_equal(self._route, numpy.array([])):
            wave_map = self._get_wave_map(from_x, from_y, to_x, to_y)
            self._previous_to_x, self._previous_to_y = to_x, to_y

            if wave_map is not None:
                self._route = deepcopy(get_route_to_point(wave_map, to_x, to_y))
                self._set_move_coefficient()
            else:
                return

        # If route calculated update sprite pos
        if self._route is not None and not numpy.array_equal(self._route, numpy.array([])):
            to_cell_x, to_cell_y = self._route[0]
            to_tile_x, to_tile_y = to_cell_x * TILE, to_cell_y * TILE

            if from_x == to_tile_x and from_y == to_tile_y:
                self._set_move_coefficient()
                self._route = self._route[1:]
            else:
                self.pos[0] += self._move_x_coefficient * self.speed
                self.pos[1] += self._move_y_coefficient * self.speed

    def _get_wave_map(self, x0, y0, x1, y1):
        wave_map = self._get_clean_board()
        wave_map[y0][x0] = 1

        current_step = 1
        while wave_map[y1][x1] == 0:
            if wave_map is not None:
                previous_wave_map = wave_map.copy()
                wave_map = next_step(numpy.array(wave_map), current_step)

                if numpy.array_equal(previous_wave_map, wave_map):
                    return

                current_step += 1
            else:
                break

        return wave_map

    def _set_move_coefficient(self):
        if len(self._route) > 1:
            self._move_x_coefficient = self._route[1][0] - self._route[0][0]
            self._move_y_coefficient = self._route[1][1] - self._route[0][1]
        else:
            self._move_x_coefficient, self._move_y_coefficient = 0, 0


def create_sprites() -> list[Sprite]:
    sprites = []

    for row_index, row in enumerate(MAP):
        for col_index, el in enumerate(row):
            if el in SPRITE_CHARS:
                x, y = col_index * TILE + TILE // 2, row_index * TILE + TILE // 2
                texture = sprite_textures[el]

                if el in STATIC_SPRITES:
                    sprite = Sprite(texture, (x, y))
                    sprites.append(sprite)
                elif el in MOVABLE_SPRITES:
                    sprite = MovableSprite(texture, (x, y), sprite_speed)
                    sprites.append(sprite)

    return sprites
