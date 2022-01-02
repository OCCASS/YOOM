import pygame

from config import *
from render import Render
from player import Player
from map import create_map

"""
Павлов Тимур 26.12.2021. Создан класс Game
Вайман Ангелина 28.12.2021. Внесены поправки
Вайман Ангелина 02.01.2022. Доработка файла main
"""


class Game:
    def __init__(self, caption=WINDOW_NAME):
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()

        self.player = Player(200, 200)
        self.render = Render(self.screen, self.player)
        self.caption = caption

    def run(self):
        self._init()
        self._config()
        self._update()
        self._finish()

    @staticmethod
    def _init():
        create_map(MAP)
        pygame.init()

    def _config(self):
        pygame.display.set_caption(self.caption)
        pygame.mouse.set_visible(False)

    def _update(self):
        running = True

        while running:
            self.screen.fill(SKYBLUE)
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False

            self.player.update()
            self.render._draw_floor()
            self.render._draw_walls()

            pygame.display.set_caption(str(self.clock.get_fps()))
            pygame.display.flip()

    @staticmethod
    def _finish():
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
