import os
import random

from config import *
from utils import world_pos2cell


class Arcade:
    def __init__(self, arcade_map_file_name):
        self.level_path = os.path.join(LEVELS_PATH, arcade_map_file_name)
        self.map = self.load_map()
        self.spawns = self.get_spawns()

    def load_map(self):
        with open(self.level_path, 'r') as file:
            lines = list(map(str.strip, file.readlines()))
            file.close()

        return lines

    def get_spawns(self):
        spawns = list()

        for row_index, row in enumerate(self.map):
            for el_index, el in enumerate(row):
                if el == ARCADE_SPAWN_CHAR:
                    x, y = el_index * TILE, row_index * TILE
                    spawns.append((x, y))

        return spawns

    @staticmethod
    def get_random_sprite():
        return random.choice(MOVABLE_SPRITES)

    def spawn(self, count):
        self.map = self.load_map()

        spawns = random.choices(self.spawns, k=count)

        for spawn in spawns:
            cell_x, cell_y = world_pos2cell(*spawn)
            self.map[cell_y][cell_x] = self.get_random_sprite()

    def get_map(self):
        return self.map