import pygame
import collections
import os

from config import *
from load_image import load_image
from sound import GunSound

"""
Вайман Ангелина:
06.01.2022. Создан класс Weapon
07.01.2022 Батталов Арслан добавлен звук выстрела
"""


class Weapon:
    def __init__(self, screen, name, size, sprites_amount, sound_path):
        self._name = name
        self._size = size
        self._sprites_amount = sprites_amount
        self._weapon_animation_list_path = os.path.join(WEAPON_FILE, name)
        self._shot_animation_count = 0
        self._animation_list = self._load_weapon()

        self.sound = GunSound(sound_path)
        self.sound.init_track(sound_path)

        width, height = size
        self._weapon_pos = (HALF_SCREEN_WIDTH - width // 2, SCREEN_HEIGHT - height)
        self._lost_frames_count = 0

        self._screen = screen

    def animation(self):
        self.fire_sound()
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

    def fire_sound(self):
        self.sound.play_sound()

    def _load_weapon(self):
        animation_list = [pygame.transform.scale(load_image(self._weapon_animation_list_path, f'{i}.gif'), self._size)
                          for i in range(self._sprites_amount)]

        return collections.deque(animation_list)
