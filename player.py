import pygame
import math
from ray_casting import ray_casting

from config import *


# Павлов Тимур 26.12.2021
class Player:
    def __init__(self, x, y):
        self._x, self._y = x, y
        self.angel = 0

    def update(self):
        self._process_mouse()
        self._process_keyboard()

    @property
    def pos(self):
        return self._x, self._y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def _process_keyboard(self):
        pressed_keys = pygame.key.get_pressed()

        cos_a, sin_a = math.cos(self.angel), math.sin(self.angel)

        if pressed_keys[pygame.K_w]:
            self._x += cos_a * PLAYER_SPEED
            self._y += sin_a * PLAYER_SPEED
        if pressed_keys[pygame.K_s]:
            self._x -= cos_a * PLAYER_SPEED
            self._y -= sin_a * PLAYER_SPEED
        if pressed_keys[pygame.K_a]:
            self._x += sin_a * PLAYER_SPEED
            self._y -= cos_a * PLAYER_SPEED
        if pressed_keys[pygame.K_d]:
            self._x -= sin_a * PLAYER_SPEED
            self._y += cos_a * PLAYER_SPEED
        if pressed_keys[pygame.K_LEFT]:
            self.angel -= 0.02
        if pressed_keys[pygame.K_RIGHT]:
            self.angel += 0.02


    def _process_mouse(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_SCREEN_WIDTH
            pygame.mouse.set_pos((HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT))
            self.angel += difference * SENSITIVITY
            self.angel %= math.radians(360)
