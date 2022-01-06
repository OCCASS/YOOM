import os
import pygame

"""
Вайман Ангелина. Создана функция load_image для загрузки спрайтов
"""


def load_image(file_name, name, colorkey=-1):
    fullname = os.path.join(file_name, name)
    image = pygame.image.load(fullname)

    if colorkey == -1:
        colorkey = image.get_at((0, 0))
    image.set_colorkey(colorkey)
    return image
