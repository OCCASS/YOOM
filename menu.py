import random
import sys

import pygame

from config import *
from load_image import load_image
from load_level import load_level

"""
Вайман Ангелина:
07.01.2022. Добавлен класс Menu и Button
08.01.2022. Доработан класс Menu. Создан класс Levels

Батталов Арслан:
08.01.2022. Добавлена наследование классов, добавлен класс Menu
08.01.2022. Добавлен класс Settings, убран баг музыки 
"""

pygame.init()

background = load_image(TEXTURES_PATH, MENU_BACKGROUND, color_key=None)
button_font = pygame.font.Font(FONT, BUTTON_FONT_SIZE)
logo_font = pygame.font.Font(FONT, LOGO_FONT_SIZE)


def button(screen, name, color, rect_pos, width, height):
    text = button_font.render(name, True, color)
    btn = pygame.Rect(rect_pos[0], rect_pos[1], width, height)
    screen.blit(text, (rect_pos[0], rect_pos[1]))
    return btn, text


def show_info(screen, player):
    health = 'Health   ' + str(player.health)
    ammo = 'Ammo   ' + str(player.weapons[player.current_gun_index].ammo)
    button(screen, health, RED, (10, SCREEN_HEIGHT - 160), 140, 70)
    button(screen, ammo, BLUE, (10, SCREEN_HEIGHT - 90), 140, 70)


def show_game_over(screen):
    width, height = 100, 30
    button(screen, 'GAME OVER', 'yellow', (HALF_SCREEN_WIDTH - width // 2, HALF_SCREEN_HEIGHT - height // 2), width,
           height)


def show_win(screen):
    width, height = 100, 30
    button(screen, 'YOU WIN!', 'yellow', (HALF_SCREEN_WIDTH - width // 2, HALF_SCREEN_HEIGHT - height // 2), width,
           height)


class Menu:
    def __init__(self, screen, clock):
        self.x = 0
        self.screen = screen
        self.clock = clock
        self.delay = 0
        self.running = True
        self.chosen_level = None
        self.delta_x = 0

    def run(self, delta_x=0):
        self.delta_x = delta_x
        pygame.time.delay(self.delay)
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self._draw_background()
            self._logo()
            self._create_buttons()
            self._mouse_operations()
            if self.chosen_level is not None:
                return self.chosen_level
            pygame.display.flip()
            self.clock.tick(20)

    def _draw_background(self):
        self.screen.blit(background, MENU_BACKGROUND_POS,
                         (self.delta_x % SCREEN_WIDTH, HALF_SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.delta_x += 1

    def _logo(self):
        color = random.randint(LOGO_COLOR[0], LOGO_COLOR[1])
        logo = logo_font.render(LOGO, True, (color, color, color))
        self.screen.blit(logo, LOGO_POS)

    def _create_buttons(self):
        pass

    def _mouse_operations(self):
        pass

    def check_chosen_level(self):
        pass


class MainMenu(Menu):
    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.levels_class = Levels(self.screen, self.clock)
        self.settings_class = Settings(self.screen, self.clock)

    def _create_buttons(self):
        self.btn_levels, self.levels = button(self.screen, LEVELS_NAME, BLACK, BTN_LEVELS_POS,
                                              MENU_BTN_SIZE[0], MENU_BTN_SIZE[1])
        self.btn_arcade, self.arcade = button(self.screen, ARCADE_NAME, BLACK, BTN_ARCADE_POS,
                                              MENU_BTN_SIZE[0], MENU_BTN_SIZE[1])
        self.btn_settings, self.settings = button(self.screen, SETTINGS_NAME, BLACK, BTN_SETTINGS_POS,
                                                  MENU_BTN_SIZE[0], MENU_BTN_SIZE[1])
        self.btn_exit, self.exit = button(self.screen, EXIT_NAME, BLACK, BTN_EXIT_BACK_POS, BTN_EXIT_BACK_SIZE[0],
                                          BTN_EXIT_BACK_SIZE[1])

    def _mouse_operations(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        self._btn_levels_check(mouse_pos, mouse_click)
        self._btn_arcade_check(mouse_pos, mouse_click)
        self._btn_settings_check(mouse_pos, mouse_click)
        self._btn_exit_check(mouse_pos, mouse_click)

    def _btn_levels_check(self, mouse_pos, mouse_click):
        if self.btn_levels.collidepoint(mouse_pos):
            button(self.screen, LEVELS_NAME, WHITE, BTN_LEVELS_POS, MENU_BTN_SIZE[0], MENU_BTN_SIZE[1])
            if mouse_click[0]:
                self.chosen_level = self.levels_class.run(delta_x=self.delta_x)
                if self.chosen_level:
                    self.menu_run = False

    def _btn_arcade_check(self, mouse_pos, mouse_click):
        if self.btn_arcade.collidepoint(mouse_pos):
            button(self.screen, ARCADE_NAME, WHITE, BTN_ARCADE_POS, MENU_BTN_SIZE[0], MENU_BTN_SIZE[1])

    def _btn_settings_check(self, mouse_pos, mouse_click):
        if self.btn_settings.collidepoint(mouse_pos):
            button(self.screen, SETTINGS_NAME, WHITE, BTN_SETTINGS_POS, MENU_BTN_SIZE[0],
                   MENU_BTN_SIZE[1])
            if mouse_click[0]:
                self.settings_class.run(delta_x=self.delta_x)

    def _btn_exit_check(self, mouse_pos, mouse_click):
        if self.btn_exit.collidepoint(mouse_pos):
            button(self.screen, EXIT_NAME, WHITE, BTN_EXIT_BACK_POS, BTN_EXIT_BACK_SIZE[0], BTN_EXIT_BACK_SIZE[1])
            if mouse_click[0]:
                pygame.quit()
                sys.exit()


class Settings(Menu):
    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.music_off = False
        self.sound_effect_off = False
        self.delay = 100

    def _create_buttons(self):
        self.btn_music, self.music = button(self.screen, MUSIC_NAME, BLACK, BTN_MUSIC_POS, MENU_BTN_SIZE[0],
                                            MENU_BTN_SIZE[1])
        if not self.music_off:
            self.btn_music_on, self.music = button(self.screen, MUSIC_ON_NAME, WHITE, BTN_MUSIC_ON_POS,
                                                   MENU_BTN_SIZE[0], MENU_BTN_SIZE[1])
        else:
            self.btn_music_on, self.music = button(self.screen, MUSIC_OFF_NAME, WHITE, BTN_MUSIC_ON_POS,
                                                   MENU_BTN_SIZE[0], MENU_BTN_SIZE[1])
        self.btn_sound_effects, self.sound_effects = button(self.screen, SOUND_EFFECTS_NAME, BLACK,
                                                            BTN_SOUND_EFFECTS_POS, MENU_BTN_SIZE[0], MENU_BTN_SIZE[1])
        if not self.sound_effect_off:
            self.btn_sound_effects_on, self.sound_effects_on = button(self.screen, MUSIC_ON_NAME, WHITE,
                                                                      BTN_SOUND_EFFECTS_ON_POS, MENU_BTN_SIZE[0],
                                                                      MENU_BTN_SIZE[1])
        else:
            self.btn_sound_effects_on, self.sound_effects_on = button(self.screen, MUSIC_OFF_NAME, WHITE,
                                                                      BTN_SOUND_EFFECTS_ON_POS, MENU_BTN_SIZE[0],
                                                                      MENU_BTN_SIZE[1])
        self.btn_back, self.back = button(self.screen, BACK_NAME, BLACK, BTN_EXIT_BACK_POS, BTN_EXIT_BACK_SIZE[0],
                                          BTN_EXIT_BACK_SIZE[1])

    def _mouse_operations(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        self._check_music(mouse_pos, mouse_click)
        self._check_sound_effects(mouse_pos, mouse_click)
        self._btn_back_check(mouse_pos, mouse_click)

    def _check_music(self, mouse_pos, mouse_click):
        if self.btn_music_on.collidepoint(mouse_pos):
            if not self.music_off:
                button(self.screen, MUSIC_ON_NAME, BLACK, BTN_MUSIC_ON_POS, MENU_BTN_SIZE[0], MENU_BTN_SIZE[1])
            else:
                button(self.screen, MUSIC_OFF_NAME, BLACK, BTN_MUSIC_ON_POS, MENU_BTN_SIZE[0], MENU_BTN_SIZE[1])
            if mouse_click[0] and not self.music_off:
                pygame.time.delay(self.delay)
                self.music_off = True
            elif mouse_click[0] and self.music_off:
                pygame.time.delay(self.delay)
                self.music_off = False

    def _check_sound_effects(self, mouse_pos, mouse_click):
        if self.btn_sound_effects_on.collidepoint(mouse_pos):
            if not self.sound_effect_off:
                button(self.screen, MUSIC_ON_NAME, BLACK, BTN_SOUND_EFFECTS_ON_POS, MENU_BTN_SIZE[0], MENU_BTN_SIZE[1])
            else:
                button(self.screen, MUSIC_OFF_NAME, BLACK, BTN_SOUND_EFFECTS_ON_POS, MENU_BTN_SIZE[0], MENU_BTN_SIZE[1])
            if mouse_click[0] and not self.sound_effect_off:
                pygame.time.delay(self.delay)
                self.sound_effect_off = True
            elif mouse_click[0] and self.sound_effect_off:
                pygame.time.delay(self.delay)
                self.sound_effect_off = False

    def _btn_back_check(self, mouse_pos, mouse_click):
        if self.btn_back.collidepoint(mouse_pos):
            button(self.screen, BACK_NAME, WHITE, BTN_EXIT_BACK_POS, BTN_EXIT_BACK_SIZE[0],
                   BTN_EXIT_BACK_SIZE[1])
            if mouse_click[0]:
                self.running = False


class Levels(Menu):
    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.delay = 250

    def check_chosen_level(self):
        if self.chosen_level is not None:
            return self.chosen_level

    def _create_buttons(self):
        self.btn_level_1, self.level_1 = button(self.screen, LEVEL_1_NAME, BLACK, BTN_LEVEL_1_POS,
                                                LEVEL_BTN_SIZE[0], LEVEL_BTN_SIZE[1])
        self.btn_level_2, self.level_2 = button(self.screen, LEVEL_2_NAME, BLACK, BTN_LEVEL_2_POS,
                                                LEVEL_BTN_SIZE[0], LEVEL_BTN_SIZE[1])
        self.btn_level_3, self.level_3 = button(self.screen, LEVEL_3_NAME, BLACK, BTN_LEVEL_3_POS,
                                                LEVEL_BTN_SIZE[0], LEVEL_BTN_SIZE[1])
        self.btn_level_4, self.level_4 = button(self.screen, LEVEL_4_NAME, BLACK, BTN_LEVEL_4_POS,
                                                LEVEL_BTN_SIZE[0], LEVEL_BTN_SIZE[1])
        self.btn_level_5, self.level_5 = button(self.screen, LEVEL_5_NAME, BLACK, BTN_LEVEL_5_POS,
                                                LEVEL_BTN_SIZE[0], LEVEL_BTN_SIZE[1])
        self.btn_menu_back, self.menu_back = button(self.screen, BACK_NAME, BLACK, BTN_EXIT_BACK_POS,
                                                    BTN_EXIT_BACK_SIZE[0], BTN_EXIT_BACK_SIZE[1])

    def _mouse_operations(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        chosen_levels = [self._btn_level_1_check(mouse_pos, mouse_click),
                         self._btn_level_2_check(mouse_pos, mouse_click),
                         self._btn_level_3_check(mouse_pos, mouse_click),
                         self._btn_level_4_check(mouse_pos, mouse_click),
                         self._btn_level_5_check(mouse_pos, mouse_click)]
        for el in chosen_levels:
            if el is not None:
                self.chosen_level = el
        self._btn_back_check(mouse_pos, mouse_click)

    def _btn_level_1_check(self, mouse_pos, mouse_click):
        if self.btn_level_1.collidepoint(mouse_pos):
            button(self.screen, LEVEL_1_NAME, WHITE, BTN_LEVEL_1_POS, LEVEL_BTN_SIZE[0],
                   LEVEL_BTN_SIZE[1])
            if mouse_click[0]:
                return load_level(LEVEL_1)

    def _btn_level_2_check(self, mouse_pos, mouse_click):
        if self.btn_level_2.collidepoint(mouse_pos):
            button(self.screen, LEVEL_2_NAME, WHITE, BTN_LEVEL_2_POS, LEVEL_BTN_SIZE[0],
                   LEVEL_BTN_SIZE[1])
            if mouse_click[0]:
                return load_level(LEVEL_2)

    def _btn_level_3_check(self, mouse_pos, mouse_click):
        if self.btn_level_3.collidepoint(mouse_pos):
            button(self.screen, LEVEL_3_NAME, WHITE, BTN_LEVEL_3_POS, LEVEL_BTN_SIZE[0],
                   LEVEL_BTN_SIZE[1])
            if mouse_click[0]:
                return load_level(LEVEL_3)

    def _btn_level_4_check(self, mouse_pos, mouse_click):
        if self.btn_level_4.collidepoint(mouse_pos):
            button(self.screen, LEVEL_4_NAME, WHITE, BTN_LEVEL_4_POS, LEVEL_BTN_SIZE[0],
                   LEVEL_BTN_SIZE[1])
            if mouse_click[0]:
                return load_level(LEVEL_4)

    def _btn_level_5_check(self, mouse_pos, mouse_click):
        if self.btn_level_5.collidepoint(mouse_pos):
            button(self.screen, LEVEL_5_NAME, WHITE, BTN_LEVEL_5_POS, LEVEL_BTN_SIZE[0],
                   LEVEL_BTN_SIZE[1])
            if mouse_click[0]:
                return load_level(LEVEL_5)

    def _btn_back_check(self, mouse_pos, mouse_click):
        if self.btn_menu_back.collidepoint(mouse_pos):
            button(self.screen, BACK_NAME, WHITE, BTN_EXIT_BACK_POS, BTN_EXIT_BACK_SIZE[0], BTN_EXIT_BACK_SIZE[1])
            if mouse_click[0]:
                self.running = False
