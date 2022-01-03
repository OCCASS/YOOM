import pygame

from config import *
from point import Point

"""
Павлов Тимур 26.12.2021. Создан класс Player

Батталов Арслан 03.01.2022. Изменена функция _process_keyboard, добавлены функции find_collison, change_cors
(пока не отлажено)
"""


class Player:
    def __init__(self, x, y):
        self._x, self._y = x, y
        self.direction = 0
        self.player_collision = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SPEED)
        self.collision_map = COLLISION_MAP

    def update(self):
        self._process_mouse()
        self._process_keyboard()
        self.player_collision.center = self._x, self._y

    @property
    def pos(self) -> Point:
        return Point(self._x, self._y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def _process_keyboard(self):
        pressed_keys = pygame.key.get_pressed()

        cos_a, sin_a = math.cos(self.direction), math.sin(self.direction)

        if pressed_keys[pygame.K_w]:
            step_x = cos_a * PLAYER_SPEED
            step_y = sin_a * PLAYER_SPEED
            self.change_cors(*self.find_collison(step_x, step_y))
        if pressed_keys[pygame.K_s]:
            step_x = -cos_a * PLAYER_SPEED
            step_y = -sin_a * PLAYER_SPEED
            self.change_cors(*self.find_collison(step_x, step_y))
        if pressed_keys[pygame.K_a]:
            step_x = sin_a * PLAYER_SPEED
            step_y = -cos_a * PLAYER_SPEED
            self.change_cors(*self.find_collison(step_x, step_y))
        if pressed_keys[pygame.K_d]:
            step_x = -sin_a * PLAYER_SPEED
            step_y = cos_a * PLAYER_SPEED
            self.change_cors(*self.find_collison(step_x, step_y))
        if pressed_keys[pygame.K_LEFT]:
            self.direction -= SENSITIVITY
        if pressed_keys[pygame.K_RIGHT]:
            self.direction += SENSITIVITY

    def _process_mouse(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_SCREEN_WIDTH
            pygame.mouse.set_pos((HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT))
            self.direction += difference * SENSITIVITY
            self.direction %= math.radians(360)

    def find_collison(self, x, y):
        return x, y

    def change_cors(self, delta_x, delta_y):
        self._x += delta_x
        self._y += delta_y
