from config import TILE, SPRITE_CHARS, MAP, TEXTURE_FILE
from load_image import load_image
from utils import world_pos2cell

"""
Павлов Тимур 08.01.2022. Создан класс Sprite и функция create_sprites
"""

sprite_textures = {
    '3': load_image(TEXTURE_FILE, 'plant.png'),
    '4': load_image(TEXTURE_FILE, 'barrel.png')
}


class Sprite:
    def __init__(self, texture, pos):
        self.texture = texture
        self.pos = self.x, self.y = pos


def create_sprites() -> list[Sprite]:
    sprites = []

    for row_index, row in enumerate(MAP):
        for col_index, el in enumerate(row):
            if el in SPRITE_CHARS:
                x, y = col_index * TILE + TILE // 2, row_index * TILE + TILE // 2
                cell_x, cell_y = world_pos2cell(x, y)
                char = MAP[cell_y][cell_x]
                texture = sprite_textures[char]
                sprite = Sprite(texture, (x, y))
                sprites.append(sprite)

    return sprites
