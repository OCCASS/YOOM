import math

import numpy

"""
Павлов Тимур:
26.12.2021. Созданы константы
28.12.2021. Внесены поправки
01.01.2021. Добавлены настройки проекции
08.01.2022. Добавлены настройки проекции

Вайман Ангелина:
28.12.2021. Внесены поправки
03.01.2022. Добавлены настройки миникарты и новые цвета
04.01.2022. Добавлены настройки текстур
06.01.2022. Добавлены настройки оружия
09.01.2022. Добавлены настройки меню

Батталов Арслан:
03.01.2022. Добавлены константы для коллизии
04.01.2022 Изменены константы коллизии
05.01.2022 Добавлены настройки музыки
07.01.2022 Добавлены настройки звука оружия
08.01.2022 Изменены константы максимальной прорисовки
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
PLAYER_SIZE = 20
PLAYER_HEALTH = 100

# Карта и настройки карты
WALL_CHARS = ('1', '2')
SPRITE_CHARS = ('3', '4', '5')
STATIC_SPRITES = ('3', '4')
MOVABLE_SPRITES = ('5',)
TILE = 125
WORLD_MAP = {}
MAP_SIZE = numpy.array([32, 24])

# Настройки ray casting
FOV = math.pi / 3
HALF_FOV = FOV / 2
RAYS_AMOUNT = 300
MAX_HORIZONTAL_RAY_DISTANCE = TILE * MAP_SIZE[0]
MAX_VERTICAL_RAY_DISTANCE = TILE * MAP_SIZE[1]
DELTA_ANGLE = FOV / RAYS_AMOUNT
CENTER_RAY_INDEX = RAYS_AMOUNT // 2 - 1

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
BLUE = 'Blue'

# Настройки проекции
SCALE = SCREEN_WIDTH // RAYS_AMOUNT
DISTANCE_TO_PROJECTION_PLANE = RAYS_AMOUNT / (2 * math.tan(HALF_FOV))
PROJECTION_COEFFICIENT = TILE * DISTANCE_TO_PROJECTION_PLANE * 3
MIN_DISTANCE = 0.00001

# Настройки миникарты
MINI_MAP = set()
MAP_SCALE = 5
MAP_TILE = SCREEN_HEIGHT / MAP_SIZE[1] // MAP_SCALE
MIINIMAP_OFFSET = 10

# Настройки текстур
TEXTURES_PATH = 'TextureSprite'
SKY_TEXTURE = 'sky.png'
WALL_TEXTURE_1 = 'wall1.jpg'
WALL_TEXTURE_2 = 'wall2.jpg'
FLOOR_TEXTURE = 'floor.png'
TEXTURE_WIDTH, TEXTURE_HEIGHT = 128, 128
TEXTURE_SCALE = TEXTURE_WIDTH // TILE

# Настройки музыки
THEME_MUSIC = 'music/theme.mp3'
FOOTSTEP = 'sound/playerstep.mp3'
SHOTGUN = 'sound/shotgun.mp3'
PISTOL = 'sound/pistol.mp3'
RIFLE = 'sound/rifle.mp3'
EMPTY_SHOT_SOUND = 'sound/null_ammo.mp3'
SPRITE_HIT_SOUND = 'sound/hit.mp3'
WALL_HIT_SOUND = 'sound/wall_hit.mp3'

# Настройки оружия
WEAPON_FILE = 'WeaponSprite/'
WEAPON_BASE = '0.png'
GUN_BASE = '0.png'
WEAPON_SIZE = (400, 260)
ANIMATION_SPEED = 6

# Настройки меню
MENU_BACKGROUND = 'StartWindow.jpg'
MENU_BACKGROUND_POS = (0, 0)
FONT = 'font.ttf'
BUTTON_FONT_SIZE = 75
LOGO_FONT_SIZE = 250
LOGO = 'YOOM'
LEVELS_NAME = 'LEVELS'
ARCADE_NAME = 'ARCADE'
SETTINGS_NAME = 'SETTINGS'
EXIT_NAME = 'EXIT'
LEVEL_1_NAME = 'level 1'
LEVEL_2_NAME = 'level 2'
LEVEL_3_NAME = 'level 3'
LEVEL_4_NAME = 'level 4'
LEVEL_5_NAME = 'level 5'
BACK_NAME = 'back'
LOGO_COLOR = (0, 50)
LOGO_POS = (HALF_SCREEN_WIDTH - 270, 0)
BTN_LEVELS_POS = (HALF_SCREEN_WIDTH - 140, 200)
BTN_ARCADE_POS = (HALF_SCREEN_WIDTH - 140, 320)
BTN_SETTINGS_POS = (HALF_SCREEN_WIDTH - 185, 440)
BTN_EXIT_BACK_POS = (50, 500)
BTN_EXIT_BACK_SIZE = (150, 50)
BTN_LEVEL_1_POS = (HALF_SCREEN_WIDTH - 140, 200)
BTN_LEVEL_2_POS = (HALF_SCREEN_WIDTH - 140, 270)
BTN_LEVEL_3_POS = (HALF_SCREEN_WIDTH - 140, 340)
BTN_LEVEL_4_POS = (HALF_SCREEN_WIDTH - 140, 410)
BTN_LEVEL_5_POS = (HALF_SCREEN_WIDTH - 140, 480)

# Файлы уровней
LEVEL_1 = 'level1.txt'
LEVEL_2 = 'level2.txt'
LEVEL_3 = 'level3.txt'
LEVEL_4 = 'level4.txt'
LEVEL_5 = 'level5.txt'
MENU_BTN_SIZE = (360, 100)
LEVEL_BTN_SIZE = (340, 50)

# Настройки спрайтов
SPRITE_SPEED = 4
SPRITE_HIT_DISTANCE = 150
