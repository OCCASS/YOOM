import pygame
import collections
import os

from config import *
from load_image import load_image

"""
Вайман Ангелина:
06.01.2022. Создан класс Weapon
"""


class Weapon:
    def __init__(self, screen, name, size, sprites_amount):
        self._name = name
        self._size = size
        self._sprites_amount = sprites_amount
        self._weapon_animation_list_path = os.path.join(WEAPON_FILE, name)
        self._shot_animation_count = 0
        self._animation_list = self._load_weapon()

        width, height = size
        self._weapon_pos = (HALF_SCREEN_WIDTH - width // 2, SCREEN_HEIGHT - height)
        self._lost_frames_count = 0

        self._screen = screen

    def animation(self):
        shot_sprite = self._animation_list[0]
        self._screen.blit(shot_sprite, self._weapon_pos)
        self._shot_animation_count += 1
        if self._shot_animation_count == ANIMATION_SPEED:
            self._animation_list.rotate(-1)
            self._shot_animation_count = 0
            self._lost_frames_count += 1
            return True

        if self._lost_frames_count == len(self._animation_list):
            self._lost_frames_count = 0
            self.static_animation()
            return False

        return True

    def static_animation(self):
        self._screen.blit(self._animation_list[0], self._weapon_pos)

    def _load_weapon(self):
        animation_list = [pygame.transform.scale(load_image(self._weapon_animation_list_path, f'{i}.gif'), self._size)
                          for i in range(self._sprites_amount)]

        return collections.deque(animation_list)
