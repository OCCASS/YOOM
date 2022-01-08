from config import *

"""
Вайман Ангелина 28.12.2021. Создана функция create_map"

Павлов Тимур 29.12.2021. Немного переработал функцию create_map

Вайман Ангелина 03.01.2022. Создана функция create_minimap

Батталов Арслан 03.01.2022. Добавлена карта коллизии

Батталов Арслан 08.01.2022. Добавлена поддержка разных текстур стен

Павлов Тимур 08.01.2021. Создан метод create_sprites_map
"""


def create_map(map_):
    for row_index, row in enumerate(map_):
        for col_index, el in enumerate(row):
            if el in WALL_CHARS:
                x, y = col_index * TILE, row_index * TILE
                if el == '1':
                    WORLD_MAP[(x, y)] = '1'
                elif el == '2':
                    WORLD_MAP[(x, y)] = '1'


def create_minimap(map_):
    for row_index, row in enumerate(map_):
        for col_index, el in enumerate(row):
            if el in WALL_CHARS:
                x, y = col_index * MAP_TILE, row_index * MAP_TILE
                MINI_MAP.add((x, y))
