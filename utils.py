def get_color_depend_distance(distance):
    return 255 / (1 + distance * distance * 0.00001), 186 / (1 + distance * distance * 0.00001), 0
