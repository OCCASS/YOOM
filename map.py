from config import *

"""
Вайман Ангелина 28.12.2021. Создана функция create_map"

Павлов Тимур 29.12.2021. Немного переработал функцию create_map

Вайман Ангелина 03.01.2022. Создана функция create_minimap
"""


def create_map(map_):
    for row_index, row in enumerate(map_):
        for col_index, el in enumerate(row):
            if el in WALL_CHARS:
                x, y = col_index * TILE, row_index * TILE
                WORLD_MAP.add((x, y))


def create_minimap(map_):
    for row_index, row in enumerate(map_):
        for col_index, el in enumerate(row):
            if el in WALL_CHARS:
                x, y = col_index * MAP_TILE, row_index * MAP_TILE
                MINI_MAP.add((x, y))