import pygame

from config import *
from point import Point
from ray import Ray
from ray_casting import sprites_ray_casting
from sound import SoundEffect, GunSound
from sprite import MovableSprite
from weapon import Weapon

"""
Павлов Тимур 26.12.2021. Создан класс Player

Батталов Арслан 03.01.2022. Изменена функция _process_keyboard, добавлены функции find_collision, change_cors
(пока не отлажено)

Батталов Арслан 04.01.2022. Добавлена функция can_move
Батталов Арслан 05.01.2022. Добавлены функции sound_effect_init, sound

Вайман Ангелина 06.01.2022. Добавлены функции _shot

Павлов Тимур 09.01.2022. Добавлена функция do_shot
"""


class Player:
    def __init__(self, x, y, weapons, sprites, stats):
        self._x, self._y = x, y
        self.shot = False
        self.current_gun_index = 0
        self.weapons: list[Weapon] = weapons
        self.health = PLAYER_HEALTH
        self.direction = 0
        self.footstep_sound = SoundEffect(FOOTSTEP)
        self._sprites = sprites
        self._stats = stats

    def update(self):
        self._process_mouse()
        self._process_keyboard()
        self._play_sound()

    def damage(self, val=1):
        self.health -= val

    def dead(self):
        self.health = 0
        SoundEffect(DEAD_SOUND).play_sound()

    def draw(self):
        self._shot()

    def set_weapon(self, delta):
        self.set_shot(False)
        self.weapons[self.current_gun_index].reset()
        GunSound.stop_sound()
        if delta == -1:
            if self.current_gun_index < 0:
                self.current_gun_index = 2
        self.current_gun_index -= delta
        self.current_gun_index %= len(self.weapons)

    def on_mouse_down(self, event):
        if event.button == pygame.BUTTON_LEFT:
            self.do_shot()
        if event.button == pygame.BUTTON_WHEELDOWN:
            self.set_weapon(-1)
        if event.button == pygame.BUTTON_WHEELUP:
            self.set_weapon(1)

    def do_shot(self):
        if self._can_shot():
            Weapon.fire_sound(self.weapons[self.current_gun_index])
            self.set_shot(True)
            self.weapons[self.current_gun_index].shot()
            all_casted_sprites = sprites_ray_casting(self._sprites, self.pos, self.direction)
            ray = Ray(self.pos, self.direction, MAX_VIEW_DISTANCE)
            ray_cast_distance = ray.ray_cast().distance
            for sprite_hit in all_casted_sprites:
                if -1 <= int(math.degrees(sprite_hit.angel)) <= 1 and sprite_hit.distance < ray_cast_distance:
                    self._sprites[sprite_hit.sprite_index].kill()
                    SoundEffect(SPRITE_HIT_SOUND).play_sound()
                    if isinstance(self._sprites[sprite_hit.sprite_index], MovableSprite):
                        self._stats.update_kills()
                    break
        current_weapon = self.weapons[self.current_gun_index]
        if current_weapon.ammo <= 0:
            Weapon.empty_fire_sound()

    def set_shot(self, val):
        if (not val) == self.shot:
            self.shot = val

    def _can_shot(self):
        current_weapon = self.weapons[self.current_gun_index]
        return not self.shot and current_weapon.ammo > 0

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
                delta_angel = math.pi / 6
                if self._can_move(self.direction - delta_angel, PLAYER_SIZE * 4) and self._can_move(
                        self.direction + delta_angel, PLAYER_SIZE * 4):
                    self._x += cos_a * PLAYER_SPEED
                    self._y += sin_a * PLAYER_SPEED
        if pressed_keys[pygame.K_s]:
            if self._can_move(self.direction - math.pi, PLAYER_SIZE * 4):
                delta_angel = math.pi / 6 - math.pi
                if self._can_move(self.direction - delta_angel, PLAYER_SIZE * 4) and self._can_move(
                        self.direction + delta_angel, PLAYER_SIZE * 4):
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
        current_weapon = self.weapons[self.current_gun_index]
        if self.shot:
            self.shot = current_weapon.animation()
        else:
            current_weapon.static_animation()

    def _can_move(self, direction, collision_distance):
        ray = Ray(self.pos, direction, MAX_VIEW_DISTANCE)

        if ray.ray_cast().distance <= collision_distance:
            return False

        return True

    def _play_sound(self):
        pressed_keys = pygame.key.get_pressed()

        if (pressed_keys[pygame.K_w] or pressed_keys[pygame.K_s]
                or pressed_keys[pygame.K_a] or pressed_keys[pygame.K_d]):
            self.footstep_sound.play_sound()
