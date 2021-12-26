import math

import pygame

from config import *
from player import Player


# Павлов Тимур 26.12.2021
class Game:
    def __init__(self, caption='Game'):
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
            self.screen.fill('skyblue')
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.player.update()
            self._draw_map()
            self._draw_player()
            pygame.display.set_caption(str(self.clock.get_fps()))
            pygame.display.flip()

    def _draw_player(self):
        pygame.draw.circle(self.screen, 'black', self.player.pos, 5)

        view_line_x = self.player.x + math.cos(self.player.angel) * MAX_VIEW_DISTANCE
        view_line_y = self.player.y + math.sin(self.player.angel) * MAX_VIEW_DISTANCE
        pygame.draw.line(self.screen, 'black', self.player.pos, (view_line_x, view_line_y), 2)

    def _draw_map(self):
        for row_index, row in enumerate(MAP):
            for char_index, char in enumerate(row):
                if char in WALL_CHARS:
                    if char == '1':
                        color = 'orange'
                    elif char == '2':
                        color = 'purple'
                    else:
                        color = 'black'

                    x, y = char_index * TILE, row_index * TILE
                    pygame.draw.rect(self.screen, color, (x, y, TILE, TILE))

    @staticmethod
    def _finish():
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
