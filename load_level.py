import os


def load_level(filename):
    filename = os.path.join('Levels', filename)
    level_map = []
    if os.path.exists(filename):
        with open(filename, 'r') as mapFile:
            for el in mapFile:
                level_map.append(el[:-1])
        return level_map
    else:
        print('Такого уровня не существует!')
        exit()