from config import TILE


def get_color_depend_distance(distance):
    return [255 / (1 + distance * distance * 0.00001)] * 3


def check_map(x, y):
    return x // TILE * TILE, y // TILE * TILE
