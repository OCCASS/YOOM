import numpy
from numba import njit

from config import MAP_SIZE
from utils import is_cell_a_wall


# @njit(fastmath=True, cache=True)
def get_route_to_point(wave_map, to_x, to_y):
    step_index = wave_map[to_y][to_x]
    route = numpy.array([(to_x, to_y)])
    while step_index > 1:
        point = None
        if to_y > 0 and wave_map[to_y - 1][to_x] == step_index - 1:
            to_y, to_x = to_y - 1, to_x
            point = to_x, to_y
            step_index -= 1
        elif to_x > 0 and wave_map[to_y][to_x - 1] == step_index - 1:
            to_y, to_x = to_y, to_x - 1
            point = to_x, to_y
            step_index -= 1
        elif to_x < MAP_SIZE[0] - 1 and wave_map[to_y][to_x + 1] == step_index - 1:
            to_y, to_x = to_y, to_x + 1
            point = to_x, to_y
            step_index -= 1
        elif to_y < MAP_SIZE[1] - 1 and wave_map[to_y + 1][to_x] == step_index - 1:
            to_y, to_x = to_y + 1, to_x
            point = to_x, to_y
            step_index -= 1

        if point is not None:
            route = numpy.append(route, [point], axis=0)

    return route[::-1]


@njit(fastmath=True, cache=True)
def next_step(m, k):
    for i in range(MAP_SIZE[1]):
        for j in range(MAP_SIZE[0]):
            if m[i][j] == k:
                if i > 0 and m[i - 1][j] == 0 and not is_cell_a_wall(i - 1, j):
                    m[i - 1][j] = k + 1
                if j > 0 and m[i][j - 1] == 0 and not is_cell_a_wall(i, j - 1):
                    m[i][j - 1] = k + 1
                if i < MAP_SIZE[1] - 1 and m[i + 1][j] == 0 and not is_cell_a_wall(i + 1, j):
                    m[i + 1][j] = k + 1
                if j < MAP_SIZE[0] - 1 and m[i][j + 1] == 0 and not is_cell_a_wall(i, j + 1):
                    m[i][j + 1] = k + 1

    return m
