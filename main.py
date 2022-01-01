import pygame

from config import *
from player import Player
from ray_casting import ray_casting
from map import create_map
from utils import get_color_depend_distance

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
            self._draw_floor()
            self._draw_walls()

            pygame.display.set_caption(str(self.clock.get_fps()))
            pygame.display.flip()

    def _draw_player(self):
        player_pos = self.player.pos
        pygame.draw.circle(self.screen, BLACK, (player_pos.x, player_pos.y), 5)
        hits = ray_casting(player_pos, self.player.direction)

        for hit in hits:
            hit_point = hit.point
            pygame.draw.line(self.screen, 'white', player_pos, hit_point)

    def _draw_floor(self):
        pygame.draw.rect(self.screen, DARKGREY, (0, HALF_SCREEN_HEIGHT, SCREEN_WIDTH, HALF_SCREEN_HEIGHT))

    def _draw_walls(self):
        hits = ray_casting(self.player.pos, self.player.direction)

        for hit_index, hit in enumerate(hits):
            distance = hit.distance * math.cos(self.player.direction - hit.angel)
            projection_height = min(PROJECTION_COEFFICIENT / (distance + 10 ** -10), SCREEN_HEIGHT * 2)

            color = get_color_depend_distance(distance)
            pygame.draw.rect(self.screen, color,
                             (hit_index * SCALE, HALF_SCREEN_HEIGHT - projection_height // 2, SCALE, projection_height))

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
