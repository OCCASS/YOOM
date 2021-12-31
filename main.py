import pygame

from config import *
from player import Player
from ray_casting import ray_casting
from map import create_map
from point import Point

"""
Павлов Тимур 26.12.2021. Создан класс Game
Вайман Ангелина 28.12.2021. Внесены поправки
"""


class Game:
    def __init__(self, caption=WINDOW_NAME):
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()

        self.player = Player(200, 200)
        self.caption = caption

    def run(self):
        self._init()
        self._config()
        self._update()
        self._finish()

    @staticmethod
    def _init():
        pygame.init()

    def _config(self):
        pygame.display.set_caption(self.caption)
        pygame.mouse.set_visible(False)

    def _update(self):
        running = True

        while running:
            self.screen.fill(SKYBLUE)
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False

            self.player.update()
            self._draw_player()
            self._draw_map()

            pygame.display.set_caption(str(self.clock.get_fps()))
            pygame.display.flip()

    def _draw_player(self):
        create_map(MAP)
        x, y = self.player.pos
        pygame.draw.circle(self.screen, BLACK, (int(x), int(y)), 5)
        hits = ray_casting(Point(x, y), self.player.direction)

        for hit in hits:
            pygame.draw.line(self.screen, 'white', self.player.pos, hit.point)

    def _draw_map(self):
        for row_index, row in enumerate(MAP):
            for char_index, char in enumerate(row):
                if char in WALL_CHARS:
                    if char == WALL_CHARS[0]:
                        color = ORANGE
                    elif char == WALL_CHARS[1]:
                        color = PURPLE
                    else:
                        color = BLACK

                    x, y = char_index * TILE, row_index * TILE
                    pygame.draw.rect(self.screen, color, (x, y, TILE, TILE))

    @staticmethod
    def _finish():
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
