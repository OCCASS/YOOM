import pygame

from config import *
from load_image import load_image

scull = pygame.transform.scale(load_image(TEXTURE_FILE, SCULL), SCULL_SIZE)

"""
Вайман Ангелина 08.01.2022. Добавлен класс Menu и Button
"""


class Menu:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.background = pygame.transform.scale(load_image(TEXTURE_FILE, MENU_BACKGROUND, color_key=None), SCREEN_SIZE)
        self.screen.blit(self.background, MENU_BACKGROUND_POS)
        self.button = Button(self.screen, 150, 50)

    def run(self):
        self.start_menu()
        while True:
            self.button.draw(110, 200, "Levels")
            self.button.draw(110, 250, "Arcade")
            self.button.draw(110, 300, "Settings")
            self.button.draw(110, 500, "Exit")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return False
            pygame.display.flip()
            self.clock.tick(FPS)

    def start_menu(self):
        self.screen.blit(self.background, MENU_BACKGROUND_POS)
        self.button.show_text('YOOM', 100, 50, font_size=100, font_color=(255, 255, 255))


class Button:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height

    def draw(self, x, y, message):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            self.show_text(message, x, y, font_color=(255, 255, 255))
        else:
            self.show_text(message, x, y)

    def show_text(self, message, x, y, font_size=50, font_color=(177, 193, 206),
                  font_type='ARCADECLASSIC.TTF'):
        font_type = pygame.font.Font(font_type, font_size)
        text = font_type.render(message, True, font_color)
        self.screen.blit(text, (x, y))


