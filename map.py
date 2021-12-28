from config import *

def create_map(world_map, map):
    for i, row in enumerate(map):
        for j, el in enumerate(row):
            if el == WALL_CHARS[0] or el == WALL_CHARS[1]:
                WORLD_MAP.add((j * TILE, i * TILE))
    return WORLD_MAP