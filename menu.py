import pygame
import sys
import random

from config import *
from load_image import load_image
from load_level import load_level

"""
Вайман Ангелина:
07.01.2022. Добавлен класс Menu и Button
08.01.2022. Доработан класс Menu. Создан класс Levels
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
    button(screen, health, 'red', (10, SCREEN_HEIGHT - 160), 140, 70)
    button(screen, ammo, 'blue', (10, SCREEN_HEIGHT - 90), 140, 70)


class Menu:
    def __init__(self, screen, clock):
        self.x = 0
        self.screen = screen
        self.clock = clock
        self.menu_run = True
        self.levels_class = Levels(self.screen, self.clock)
        self.chosen_level = None

    def run(self):
        while self.menu_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.blit(background, (0, 0),
                             (self.x % SCREEN_WIDTH, HALF_SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT))
            self.x += 1
            self._logo()
            self._create_buttons()
            self._mouse_operations()
            pygame.display.flip()
            self.clock.tick(20)

    def _logo(self):
        color = random.randint(0, 50)
        logo = logo_font.render(LOGO, True, (color, color, color))
        self.screen.blit(logo, (HALF_SCREEN_WIDTH - 270, 0))

    def _create_buttons(self):
        self.btn_levels, self.levels = button(self.screen, LEVELS_NAME, BLACK, (HALF_SCREEN_WIDTH - 140, 200),
                                              MENU_BTN_SIZE[0], MENU_BTN_SIZE[1])
        self.btn_arcade, self.arcade = button(self.screen, ARCADE_NAME, BLACK, (HALF_SCREEN_WIDTH - 140, 320),
                                              MENU_BTN_SIZE[0], MENU_BTN_SIZE[1])
        self.btn_settings, self.settings = button(self.screen, SETTINGS_NAME, BLACK, (HALF_SCREEN_WIDTH - 185, 440),
                                                  MENU_BTN_SIZE[0], MENU_BTN_SIZE[1])
        self.btn_exit, self.exit = button(self.screen, EXIT_NAME, BLACK, (50, 500), 150, 50)

    def _mouse_operations(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        self._btn_levels_check(mouse_pos, mouse_click)
        self._btn_arcade_check(mouse_pos, mouse_click)
        self._btn_settings_check(mouse_pos, mouse_click)
        self._btn_exit_check(mouse_pos, mouse_click)

    def _btn_levels_check(self, mouse_pos, mouse_click):
        if self.btn_levels.collidepoint(mouse_pos):
            button(self.screen, LEVELS_NAME, WHITE, (HALF_SCREEN_WIDTH - 140, 200), MENU_BTN_SIZE[0], MENU_BTN_SIZE[1])
            if mouse_click[0]:
                self.chosen_level = self.levels_class.run()
                if self.chosen_level:
                    self.menu_run = False

    def _btn_arcade_check(self, mouse_pos, mouse_click):
        if self.btn_arcade.collidepoint(mouse_pos):
            button(self.screen, ARCADE_NAME, WHITE, (HALF_SCREEN_WIDTH - 140, 320), MENU_BTN_SIZE[0], MENU_BTN_SIZE[1])

    def _btn_settings_check(self, mouse_pos, mouse_click):
        if self.btn_settings.collidepoint(mouse_pos):
            button(self.screen, SETTINGS_NAME, WHITE, (HALF_SCREEN_WIDTH - 185, 440), MENU_BTN_SIZE[0],
                   MENU_BTN_SIZE[1])

    def _btn_exit_check(self, mouse_pos, mouse_click):
        if self.btn_exit.collidepoint(mouse_pos):
            button(self.screen, EXIT_NAME, WHITE, (50, 500), 150, 50)
            if mouse_click[0]:
                pygame.quit()
                sys.exit()


class Levels:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.levels_run = True
        self.x = 0
        self.chosen_level = None

    def run(self):
        pygame.time.delay(250)
        self.levels_run = True
        while self.levels_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.blit(background, (0, 0),
                             (self.x % SCREEN_WIDTH, HALF_SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT))
            self.x += 1
            self._logo()
            self._create_buttons()
            self.mouse_operations()
            if self.chosen_level is not None:
                return self.chosen_level
            self.x += 1
            pygame.display.flip()
            self.clock.tick(20)

    def _logo(self):
        color = random.randint(0, 50)
        logo = logo_font.render(LOGO, True, (color, color, color))
        self.screen.blit(logo, (HALF_SCREEN_WIDTH - 270, 0))

    def _create_buttons(self):
        self.btn_level_1, self.level_1 = button(self.screen, LEVEL_1_NAME, BLACK, (HALF_SCREEN_WIDTH - 140, 200),
                                                LEVEL_BTN_SIZE[0],
                                                LEVEL_BTN_SIZE[1])
        self.btn_level_2, self.level_2 = button(self.screen, LEVEL_2_NAME, BLACK, (HALF_SCREEN_WIDTH - 140, 270),
                                                LEVEL_BTN_SIZE[0],
                                                LEVEL_BTN_SIZE[1])
        self.btn_level_3, self.level_3 = button(self.screen, LEVEL_3_NAME, BLACK, (HALF_SCREEN_WIDTH - 140, 340),
                                                LEVEL_BTN_SIZE[0],
                                                LEVEL_BTN_SIZE[1])
        self.btn_level_4, self.level_4 = button(self.screen, LEVEL_4_NAME, BLACK, (HALF_SCREEN_WIDTH - 140, 410),
                                                LEVEL_BTN_SIZE[0],
                                                LEVEL_BTN_SIZE[1])
        self.btn_level_5, self.level_5 = button(self.screen, LEVEL_5_NAME, BLACK, (HALF_SCREEN_WIDTH - 140, 480),
                                                LEVEL_BTN_SIZE[0],
                                                LEVEL_BTN_SIZE[1])
        self.btn_menu_back, self.menu_back = button(self.screen, BACK_NAME, BLACK, (50, 500), 150, 50)

    def mouse_operations(self):
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
            button(self.screen, LEVEL_1_NAME, WHITE, (HALF_SCREEN_WIDTH - 140, 200), LEVEL_BTN_SIZE[0],
                   LEVEL_BTN_SIZE[1])
            if mouse_click[0]:
                return load_level(LEVEL_1)

    def _btn_level_2_check(self, mouse_pos, mouse_click):
        if self.btn_level_2.collidepoint(mouse_pos):
            button(self.screen, LEVEL_2_NAME, WHITE, (HALF_SCREEN_WIDTH - 140, 270), LEVEL_BTN_SIZE[0],
                   LEVEL_BTN_SIZE[1])
            if mouse_click[0]:
                return load_level(LEVEL_2)

    def _btn_level_3_check(self, mouse_pos, mouse_click):
        if self.btn_level_3.collidepoint(mouse_pos):
            button(self.screen, LEVEL_3_NAME, WHITE, (HALF_SCREEN_WIDTH - 140, 340), LEVEL_BTN_SIZE[0],
                   LEVEL_BTN_SIZE[1])
            if mouse_click[0]:
                return load_level(LEVEL_3)

    def _btn_level_4_check(self, mouse_pos, mouse_click):
        if self.btn_level_4.collidepoint(mouse_pos):
            button(self.screen, LEVEL_4_NAME, WHITE, (HALF_SCREEN_WIDTH - 140, 410), LEVEL_BTN_SIZE[0],
                   LEVEL_BTN_SIZE[1])
            if mouse_click[0]:
                return load_level(LEVEL_4)

    def _btn_level_5_check(self, mouse_pos, mouse_click):
        if self.btn_level_5.collidepoint(mouse_pos):
            button(self.screen, LEVEL_5_NAME, WHITE, (HALF_SCREEN_WIDTH - 140, 480), LEVEL_BTN_SIZE[0],
                   LEVEL_BTN_SIZE[1])
            if mouse_click[0]:
                return load_level(LEVEL_5)

    def _btn_back_check(self, mouse_pos, mouse_click):
        if self.btn_menu_back.collidepoint(mouse_pos):
            button(self.screen, BACK_NAME, WHITE, (50, 500), 150, 50)
            if mouse_click[0]:
                self.levels_run = False
