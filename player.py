import pygame

from config import *
from point import Point
from ray import Ray
from sound import SoundEffect
from weapon import Weapon

"""
Павлов Тимур 26.12.2021. Создан класс Player

Батталов Арслан 03.01.2022. Изменена функция _process_keyboard, добавлены функции find_collison, change_cors
(пока не отлажено)

Батталов Арслан 04.01.2022. Добавлена функция can_move
Батталов Арслан 05.01.2022. Добавлены функции sound_effect_init, sound

Вайман Ангелина 06.01.2022. Добавлены функции _shot
"""


class Player:
    def __init__(self, x, y, weapons):
        self._x, self._y = x, y
        self.direction = 0
        self.footstep_sound = SoundEffect(FOOTSTEP)
        self.shot = False
        self.current_gun_index = 0
        self.weapons: list[Weapon] = weapons

    def update(self):
        self._process_mouse()
        self._process_keyboard()
        self._play_sound()

    def draw(self):
        self._shot()

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
            if self._can_move(self.direction, PLAYER_SIZE * 4):
                self._x += cos_a * PLAYER_SPEED
                self._y += sin_a * PLAYER_SPEED
        if pressed_keys[pygame.K_s]:
            if self._can_move(self.direction - math.pi, PLAYER_SIZE * 4):
                self._x += -cos_a * PLAYER_SPEED
                self._y += -sin_a * PLAYER_SPEED
        if pressed_keys[pygame.K_a]:
            if self._can_move(self.direction - math.pi / 2, PLAYER_SIZE * 3):
                self._x += sin_a * PLAYER_SPEED
                self._y += -cos_a * PLAYER_SPEED
        if pressed_keys[pygame.K_d]:
            if self._can_move(self.direction + math.pi / 2, PLAYER_SIZE * 3):
                self._x += -sin_a * PLAYER_SPEED
                self._y += cos_a * PLAYER_SPEED
        if pressed_keys[pygame.K_LEFT]:
            self.direction -= SENSITIVITY
        if pressed_keys[pygame.K_RIGHT]:
            self.direction += SENSITIVITY

    def _process_mouse(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_SCREEN_WIDTH
            pygame.mouse.set_pos((HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT))
            self.direction += difference * SENSITIVITY
            self.direction %= math.pi * 2

    def _shot(self):
        curren_weapon = self.weapons[self.current_gun_index]
        if self.shot:
            self.shot = curren_weapon.animation()
        else:
            curren_weapon.static_animation()

    def _can_move(self, direction, collision_distance):
        ray = Ray(self.pos, direction, MAX_VIEW_DISTANCE)

        if ray.ray_cast()[0].distance <= collision_distance:
            return False

        return True

    def _play_sound(self):
        pressed_keys = pygame.key.get_pressed()

        if (pressed_keys[pygame.K_w] or pressed_keys[pygame.K_s]
                or pressed_keys[pygame.K_a] or pressed_keys[pygame.K_d]):
            self.footstep_sound.play_sound()
