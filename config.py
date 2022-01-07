import math
from typing import List

"""
Павлов Тимур:
26.12.2021. Созданы константы
28.12.2021. Внесены поправки
01.01.2021. Добавлены настройки проекции

Вайман Ангелина:
28.12.2021. Внесены поправки
03.01.2022. Добавлены настройки миникарты и новые цвета
04.01.2022. Добавлены настройки текстур
06.01.2022. Добавлены настройки оружия

Батталов Арслан:
03.01.2022. Добавлены константы для коллизии
04.01.2022 Изменены константы коллизии
05.01.2022 Добавлены настройки музыки
07.01.2022 Добавлены настройки звука оружия
"""

# Настройки экрана
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (1200, 600)
HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT = SCREEN_WIDTH >> 1, SCREEN_HEIGHT >> 1
WINDOW_NAME = 'Game'

# Настройки игрока и луча
FPS = 120
PLAYER_SPEED = 5
SENSITIVITY = 0.005
MAX_VIEW_DISTANCE = 800
PLAYER_SIZE = 15
MAX_DISTANCE_TO_WALL = PLAYER_SIZE * 4

# Настройки ray casting
FOV = math.pi / 3
HALF_FOV = FOV / 2
RAYS_AMOUNT = 300
MAX_RAY_DISTANCE = 800
DELTA_ANGLE = FOV / RAYS_AMOUNT

# Карта и настройки карты
MAP: List[str] = [
    '11111111111111111111111111111111',
    '1..............................1',
    '1.222......1...1.1...1.....222.1',
    '1.222......11111.11111.....222.1',
    '1.....212..............212.....1',
    '1.222......11111.11111.....222.1',
    '1.222......1...1.1...1.....222.1',
    '1..............................1',
    '1.11111..................11111.1',
    '1.11111..................11111.1',
    '1.11111.......22222......11111.1',
    '1.............22222............1',
    '1.............22222............1',
    '1..11111......22222......11111.1',
    '1..11111.................11111.1',
    '1..11111.................11111.1',
    '1..............................1',
    '1.222......1...1.1...1.....222.1',
    '1.222......11111.11111.....222.1',
    '1.....212..............212.....1',
    '1.222......11111.11111.....222.1',
    '1.222......1...1.1...1.....222.1',
    '1..............................1',
    '11111111111111111111111111111111'
]
WALL_CHARS = ('1', '2')
TILE = 125
WORLD_MAP = set()
MAP_SIZE = (len(MAP[0]), len(MAP))
COLLISION_MAP = list()

# Цвета
ORANGE = 'Orange'
PURPLE = 'Purple'
BLACK = 'Black'
SKYBLUE = 'Skyblue'
DARKGREY = 'Darkgrey'
YELLOW = 'Yellow'
GREEN = 'Green'
RED = 'Red'
WHITE = 'White'
BRICK = (139, 79, 57)
ANTHRACITE = (45, 45, 45)

# Настройки проекции
SCALE = SCREEN_WIDTH // RAYS_AMOUNT
DISTANCE_TO_PROJECTION_PLANE = RAYS_AMOUNT / (2 * math.tan(HALF_FOV))
PROJECTION_COEFFICIENT = TILE * DISTANCE_TO_PROJECTION_PLANE * 3

# Настройки миникарты
MINI_MAP = set()
MAP_SCALE = 5
MAP_TILE = SCREEN_HEIGHT / MAP_SIZE[1] // MAP_SCALE

# Настройки текстур
TEXTURE_FILE = 'TextureSprite'
SKY_TEXTURE = 'sky.png'
WALL_TEXTURE = 'wall2.jpg'
FLOOR_TEXTURE = 'floor.png'
TEXTURE_WIDTH, TEXTURE_HEIGHT = 128, 128
TEXTURE_SCALE = TEXTURE_WIDTH // TILE

# Настройки музыки
THEME_MUSIC = 'music/theme.mp3'
FOOTSTEP = 'sound/playerstep.mp3'
SHOTGUN = 'sound/shotgun.mp3'
PISTOL = 'sound/pistol.mp3'
RIFLE = 'sound/rifle.mp3'

# Настройки оружия
WEAPON_FILE = 'WeaponSprite/'
WEAPON_BASE = '0.png'
GUN_BASE = '0.png'
WEAPON_SIZE = (400, 260)
ANIMATION_SPEED = 6
