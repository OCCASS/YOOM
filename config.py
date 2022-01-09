import math
import os.path
from os import listdir
from os.path import isfile, join

import numpy

"""
Павлов Тимур:
26.12.2021. Созданы константы
28.12.2021. Внесены поправки
01.01.2021. Добавлены настройки проекции
08.01.2022. Добавлены настройки проекции
09.01.2022. Добавлены настройки спрайтов и игрока
09.01.2022. Добавлены новые звуки
09.01.2022. Добавлены настройки анимации спрайтов
09.01.2022. Добавлены новые звуки

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
08.01.2022 Добавлены константы настроек музыки
08.01.2022 Настройки музыки уровней
08.01.2022 Добавлены новые текстуры
"""

# Настройки экрана
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (1200, 600)
HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT = SCREEN_WIDTH >> 1, SCREEN_HEIGHT >> 1
WINDOW_NAME = 'Game'

# Настройки игрока и луча
FPS = 60
PLAYER_SPEED = 8
SENSITIVITY = 0.005
MAX_VIEW_DISTANCE = 800
PLAYER_SIZE = 20
PLAYER_HEALTH = 100
SHOOTING_SPREAD = 2

# Карта и настройки карты
WALL_CHARS = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q')
STATIC_SPRITES = ('5', 'b', 'd')
MOVABLE_SPRITES = ('3', '4', '6', '7', '8', '9', 'a')
ARCADE_SPAWN_CHAR = '@'
SPRITE_CHARS = (*STATIC_SPRITES, *MOVABLE_SPRITES)
TILE = 125
WORLD_MAP = dict()
MAP_SIZE = numpy.array([32, 24])

# Настройки ray casting
FOV = math.pi / 3
HALF_FOV = FOV / 2
RAYS_AMOUNT = 300
MAX_HORIZONTAL_RAY_DISTANCE = TILE * MAP_SIZE[0] * 2
MAX_VERTICAL_RAY_DISTANCE = TILE * MAP_SIZE[1] * 2
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
STONE_WALL = 'STONE2.png'
BASIC_WALL = 'wall1.jpg'
COMPUTER_1 = 'computer1.png'
COMPUTER_2 = 'computer2.png'
FACE_WALL_1 = 'face1.png'
FACE_WALL_2 = 'face2.png'
FACE_WALL_3 = 'face3.png'
MARBLE_WALL_1 = 'marble_wall1.png'
MARBLE_WALL_2 = 'marble_wall2.png'
MARBLE_WALL_BLOOD = 'marble_wall_blood.png'
METAL_WALL = 'metal_wall_2.png'
DUDE_WALL_1 = 'SP_DUDE1.png'
DUDE_WALL_2 = 'SP_DUDE2.png'
BASIC_WALL_2 = 'STARBR2.png'
BASIC_WALL_3 = 'STARG2.png'
BASIC_WALL_4 = 'STARG3.png'
BASIC_WALL_5 = 'STARTAN2.png'
FLOOR_TEXTURE = 'floor.png'
TEXTURE_WIDTH, TEXTURE_HEIGHT = 128, 128
TEXTURE_SCALE = TEXTURE_WIDTH // TILE

# Настройки музыки
THEME_MUSIC = 'music/theme.mp3'
FOOTSTEP_SOUND = 'sound/playerstep.mp3'
SHOTGUN = 'sound/shotgun.mp3'
PISTOL = 'sound/pistol.mp3'
RIFLE = 'sound/rifle.mp3'
NO_AMMO_SOUND = 'sound/null_ammo.mp3'
SPRITE_HIT_SOUND = 'sound/hit.mp3'
WALL_HIT_SOUND = 'sound/wall_hit.mp3'
MENU_THEME = 'music/menu.mp3'
DAMAGE_SOUND = 'sound/damage.wav'
DEAD_SOUND = 'sound/dead.wav'
DO_DAMAGE_SOUND = 'sound/do_damage.mp3'
MUSIC_FOLDER = 'Levels_music'
MUSIC_FILES = [os.path.join(MUSIC_FOLDER, file) for file in listdir(MUSIC_FOLDER) if isfile(join(MUSIC_FOLDER, file))]

# Настройки оружия
WEAPON_FILE = 'WeaponSprite/'
WEAPON_BASE = '0.png'
GUN_BASE = '0.png'
WEAPON_SIZE = (400, 260)
ANIMATION_SPEED = 6

# Настройки меню
MENU_BTN_SIZE = (360, 75)
LEVEL_BTN_SIZE = (340, 50)
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
BTN_MUSIC_POS = (HALF_SCREEN_WIDTH - 140, 250)
MUSIC_NAME = 'music'
MUSIC_ON_NAME = 'on'
BTN_MUSIC_ON_POS = (HALF_SCREEN_WIDTH + 100, 250)
SOUND_EFFECTS_NAME = 'sound effects'
BTN_SOUND_EFFECTS_POS = (HALF_SCREEN_WIDTH - 320, 350)
BTN_SOUND_EFFECTS_ON_POS = (HALF_SCREEN_WIDTH + 210, 350)
MUSIC_OFF_NAME = 'off'

# Файлы уровней
LEVELS_PATH = 'Levels'
LEVEL_1 = 'level1.txt'
LEVEL_2 = 'level2.txt'
LEVEL_3 = 'level3.txt'
LEVEL_4 = 'level4.txt'
LEVEL_5 = 'level5.txt'

# Настройки спрайтов
SPRITE_SPEED = 4
SPRITE_HIT_DISTANCE = 120
SPRITE_DAMAGE_DELAY = 300
DEVIL_ANIMATION_FRAMES_COUNT = 4
PIN_ANIMATION_FRAMES_COUNT = 7
FLAME_ANIMATION_FRAMES_COUNT = 16
BARREL_ANIMATION_FRAME_COUNT = 13
DEVIL_YELLOW_ANIMATION_FRAMES_COUNT = 4
AERIAL_ANIMATION_FRAMES_COUNT = 6
SKULL_ANIMATION_FRAMES_COUNT = 6
IMP_ANIMATION_FRAMES_COUNT = 4
IMP_ATTACK_ANIMATION_FRAMES_COUNT = 3
SOLDIER_ANIMATION_FRAMES_COUNT = 4
SOLDIER_ATTACK_ANIMATION_FRAMES_COUNT = 7
DEATH_SOLDIER_ANIMATION_FRAMES_COUNT = 2
GUITAR_DOOM_GUY_ANIMATION_FRAMES_COUNT = 3
SPRITE_ANIMATION_SPEED = 50

# Настройки векторов
RIGHT_VECTOR = (1, 0, 0)

# Настройки окна победа и проигрыш
WON = "YOU WON"
LOSE = "YOU LOSE"
FONT_SIZE = 200
PICTURE_SIZE = (400, 400)
PICTURE_POS = (800, 100)
SENT_POS = (10, 165)
SENT_SIZE = (250, 100)
SKULL_AMOUNT = 3
SKELETON_AMOUNT = 11
TIME_NAME = "TIME    "
TIME_POS = (10, 400)
TIME_SIZE = (250, 70)
KILLS_NAME = "KILLS   "
KILLS_POS = (10, 500)
SEC = 'S'
BACK_TO_MENU = 'back to menu'
BACK_TO_MENU_POS = (10, 1)
BACK_TO_MENU_SIZE = (190, 50)
