import pygame
from config import *
import math


def ray_casting(screen, player_pos, player_angle):
    cur_angle = player_angle - (FOV / 2)
    points = []
    for ray in range(RAYS_AMOUNT):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        for depth in range(MAX_DEPTH):
            x = player_pos[0] + depth * cos_a
            y = player_pos[1] + depth * sin_a
            points.append((x, y))
            if (x // TILE * TILE, y // TILE * TILE) in WORLD_MAP:
                break
        cur_angle += DELTA_ANGLE
        return points
