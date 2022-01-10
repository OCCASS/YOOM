import pygame
from config import VIDEO_PATH
from moviepy.editor import VideoFileClip

"""
Батталов Арслан 09.01.2022:
Добавлен класс Video
"""


class Video:
    def __init__(self, menu):
        pygame.display.set_caption('YOOM')
        self.menu = menu

    def play_video(self):
        clip = VideoFileClip(VIDEO_PATH)
        clip.preview()
        self.back_to_menu()

    def back_to_menu(self):
        self.menu.run()

