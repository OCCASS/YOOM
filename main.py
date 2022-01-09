import pygame

from config import *
from map import create_map, create_minimap
from menu import MainMenu, show_info
from player import Player
from render import Render
from sound import Music
from sprite import create_sprites, sprites_update, is_win
from stats import Stats
from utils import is_game_over
from weapon import Weapon
from result_window import Win, Losing

"""
Павлов Тимур 26.12.2021. Создан класс Game
Вайман Ангелина 28.12.2021. Внесены поправки
Вайман Ангелина 03.01.2022. Создана новая поверхность screen_map для миникарты
Батталов Арслан 05.01.2022. Добавлены функция play_theme
Батталов Арслан 08.01.2022 Добавлена поддержка звуков выстрела
Павлов Тимур 08.01.2022. Исправлена ошибка анимации оружия
Батталов Арслан 08.01.2022 Исправлена проблема двойного проигрывания звуков
Павлов Тимур 09.01.2022. Добавлена проверка окончания игры
"""


class Game:
    def __init__(self):
        self._screen = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
        self._minimap_screen = pygame.Surface((MAP_SIZE[0] * MAP_TILE, MAP_SIZE[1] * MAP_TILE))
        self._clock = pygame.time.Clock()
        self._caption = WINDOW_NAME
        self._is_game_end = False

        self._weapons = [
            Weapon(self._screen, 'Gun1', (500, 450), 12, SHOTGUN, 5),
            Weapon(self._screen, 'Gun2', (400, 400), 2, PISTOL, 25),
            Weapon(self._screen, 'Gun3', (350, 300), 10, RIFLE, 10)
        ]

        self._menu = MainMenu(self._screen, self._clock)
        self._losing = Losing(self._screen, self._clock)
        self._win = Win(self._screen, self._clock)

    def run(self):
        self._menu.run()
        self._init()
        self.play_theme()
        self._config()
        self._update()
        self._finish()

    def _init(self):
        self._sprites = create_sprites(self._menu.chosen_level)
        self._stats = Stats()
        self._player = Player(TILE * 2 - TILE // 2, TILE * 2 - TILE // 2, self._weapons, self._sprites, self._stats)
        self._render = Render(self._screen, self._player, self._minimap_screen, self._sprites)

        create_map(self._menu.chosen_level)
        create_minimap(self._menu.chosen_level)
        pygame.init()

    def _config(self):
        pygame.display.set_caption(self._caption)
        pygame.mouse.set_visible(False)

    def _update(self):
        running = True
        while running:
            self._screen.fill(SKYBLUE)
            self._clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self._is_game_end:
                    if event.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._player.on_mouse_down(event)

            self._is_game_end = is_game_over(self._player) or is_win(self._sprites)
            if self._is_game_end:
                if is_game_over(self._player):
                    self._losing.run()
                elif is_win(self._sprites):
                    self._win.run()

                print(self._stats.total_time())
                print(self._stats.get_kills())
            else:
                self._player.update()
                self._render.render()
                sprites_update(self._sprites, self._player)
                show_info(self._screen, self._player)

            pygame.display.set_caption('FPS: ' + str(int(self._clock.get_fps())))
            pygame.display.flip()

    @staticmethod
    def _finish():
        pygame.quit()

    @staticmethod
    def play_theme():
        theme = Music()
        theme.play_music()


if __name__ == '__main__':
    game = Game()
    game.run()
