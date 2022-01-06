import pygame
import collections

from config import *
from load_image import load_image


"""
Вайман Ангелина:
06.01.2022. Создан класс Weapon
"""


class Weapon:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.shot_animation_count, self.length_count = 0, 0
        self.weapon_pos = (HALF_SCREEN_WIDTH - WEAPON_FILES[self.player.gun][2][0] // 2,
                           SCREEN_HEIGHT - WEAPON_FILES[self.player.gun][2][1])

    def run(self):
        self._weapon_animation()

    def _load_weapon(self):
        animations_sprites_list = collections.deque(
            [pygame.transform.scale(load_image(WEAPON_FILE + WEAPON_FILES[self.player.gun][0], f'{i}.png'),
                                    WEAPON_FILES[self.player.gun][2])
             for i in
             range(WEAPON_FILES[self.player.gun][1])])
        return animations_sprites_list

    def _weapon_animation(self):
        animations_sprites_list = self._load_weapon()
        if self.player.shot:
            shot_sprite = animations_sprites_list[0]
            self.screen.blit(shot_sprite, self.weapon_pos)
            self.shot_animation_count += 1
            if self.shot_animation_count == ANIMATION_SPEED:
                animations_sprites_list.rotate(-1)
                self.shot_animation_count = 0
                self.length_count += 1
            if self.length_count == len(animations_sprites_list):
                self.player.shot = False
                self.length_count = 0
        else:
            self.screen.blit(animations_sprites_list[0], self.weapon_pos)
