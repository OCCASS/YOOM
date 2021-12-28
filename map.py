from config import *


# Вайман Ангелина 28.12.2021. Создана функция create_map
def create_map(map):
    for i, row in enumerate(map):
        for j, el in enumerate(row):
            if el == WALL_CHARS[0] or el == WALL_CHARS[1]:
                WORLD_MAP.add((j * TILE, i * TILE))
    return WORLD_MAP
