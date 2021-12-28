import pygame
from config import *
import math


def ray_casting(screen, player_pos, player_angle):
    cur_angle = player_angle - FOV / 2
    x0, y0 = player_pos
    for ray in range(RAYS_AMOUNT):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        for depth in range(MAX_DEPTH):
            x = x0 + depth * cos_a
            y = y0 + depth * sin_a
            if (x // TILE * TILE, y // TILE * TILE) in WORLD_MAP:
                break
        cur_angle += DELTA_ANGLE
