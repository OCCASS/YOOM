import math

import pygame

from config import *
from player import Player
from ray_casting import ray_casting
from map import create_map


# Павлов Тимур 26.12.2021
# Вайман Ангелина 28.12.2021. Внесены поправки
class Game:
    def __init__(self, caption=GAME_NAME):
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()

        self.player = Player(200, 200, self.screen)
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
        pygame.draw.circle(self.screen, BLACK, (int(self.player.pos[0]), int(self.player.pos[1])), 5)

        view_line_x = self.player.x + math.cos(self.player.angel) * MAX_VIEW_DISTANCE
        view_line_y = self.player.y + math.sin(self.player.angel) * MAX_VIEW_DISTANCE
        pygame.draw.line(self.screen, BLACK, self.player.pos, (view_line_x, view_line_y), 2)

    def _draw_map(self):
        create_map(WORLD_MAP, MAP)
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
