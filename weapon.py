import collections
import os

import pygame

from config import *
from load_image import load_image
from sound import GunSound

"""
Вайман Ангелина:
06.01.2022. Создан класс Weapon

Павлов Тимур:
08.01.2022. Исправлена ошибка анимации
09.01.2022. Добавлена способность стрелять

Батталов Арслан:
08.01.2022 Добавлена поддержка звуков выстрела, функция fire_sound
"""


class Weapon:
    def __init__(self, screen, name, size, animation_frame_counts, sound, ammo, damage, depth):
        self.ammo = ammo
        self.damage = damage
        self.depth = depth
        self._name = name
        self._size = size
        self._animation_frame_counts = animation_frame_counts
        self._weapon_animation_list_path = os.path.join(WEAPON_FILE, name)
        self._shot_animation_count = 0
        self._animation_list = self._load_weapon()
        self._default_animation_list = self._animation_list.copy()
        self._sound = GunSound(sound)
        self._weapon_pos = (HALF_SCREEN_WIDTH - size[0] // 2, SCREEN_HEIGHT - size[1])
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

    def reset(self):
        self._animation_list = self._default_animation_list.copy()
        self._shot_animation_count = 0
        self._lost_frames_count = 0

    def static_animation(self):
        self._screen.blit(self._animation_list[0], self._weapon_pos)

    def fire_sound(self):
        self._sound.play_sound()

    def shot(self):
        self.ammo -= 1

    def _load_weapon(self):
        animation_list = [pygame.transform.scale(load_image(self._weapon_animation_list_path, f'{i}.gif'), self._size)
                          for i in range(self._animation_frame_counts)]

        return collections.deque(animation_list)
