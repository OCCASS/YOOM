import pygame

from config import *
from map import create_map, create_minimap
from player import Player
from render import Render
from sound import Music

"""
Павлов Тимур 26.12.2021. Создан класс Game
Вайман Ангелина 28.12.2021. Внесены поправки
Вайман Ангелина 03.01.2022. Создана новая поверхность screen_map для миникарты
Батталов Арслан 05.01.2022. Добавлены функция play_theme
"""


class Game:
    def __init__(self, caption=WINDOW_NAME):
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
        self.screen_map = pygame.Surface((MAP_SIZE[0] * MAP_TILE, MAP_SIZE[1] * MAP_TILE))
        self.clock = pygame.time.Clock()

        self.player = Player(200, 200)
        self.render = Render(self.screen, self.player, self.screen_map)
        self.caption = caption

    def run(self):
        self._init()
        self.play_theme(THEME_MUSIC)
        self._config()
        self._update()
        self._finish()

    @staticmethod
    def _init():
        create_map(MAP)
        create_minimap(MAP)
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
            self.render.render()

            pygame.display.set_caption('FPS: ' + str(int(self.clock.get_fps())))
            pygame.display.flip()

    @staticmethod
    def _finish():
        pygame.quit()

    @staticmethod
    def play_theme(path):
        theme = Music(path)
        theme.play_music()


if __name__ == '__main__':
    game = Game()
    game.run()
