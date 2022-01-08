import pygame

from config import *
from load_image import load_image

"""
Вайман Ангелина 08.01.2022. Добавлен класс Menu и Button
"""


class Menu:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.background = pygame.transform.scale(load_image(TEXTURE_FILE, MENU_BACKGROUND, color_key=None), SCREEN_SIZE)
        self.screen.blit(self.background, MENU_BACKGROUND_POS)
        self.button = Button(self.screen, BTN_SIZE[0], BTN_SIZE[1])

    def run(self):
        self.start_menu()
        while True:
            self.button.draw(BTN_LEVELS_POS[0], BTN_LEVELS_POS[1], BTN_LEVELS)
            self.button.draw(BTN_ARCADE_POS[0], BTN_ARCADE_POS[1], BTN_ARCADE)
            self.button.draw(BTN_SETTINGS_POS[0], BTN_SETTINGS_POS[1], BTN_SETTINGS)
            self.button.draw(BTN_EXIT_POS[0], BTN_EXIT_POS[1], BTN_EXIT)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return False
            pygame.display.flip()
            self.clock.tick(FPS)

    def start_menu(self):
        self.screen.blit(self.background, MENU_BACKGROUND_POS)
        self.button.show_text(LOGO, LOGO_POS[0], LOGO_POS[1], font_size=100, font_color=ACTIVE_COLOR)


class Button:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height

    def draw(self, x, y, message):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            self.show_text(message, x, y, font_color=ACTIVE_COLOR)
        else:
            self.show_text(message, x, y)

    def show_text(self, message, x, y, font_size=50, font_color=INACTIVE_COLOR,
                  font_type=FONT):
        font_type = pygame.font.Font(font_type, font_size)
        text = font_type.render(message, True, font_color)
        self.screen.blit(text, (x, y))


