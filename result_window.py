import pygame
import sys
import collections
import random

from config import *
from menu import button
from load_image import load_image

"""
Вайман Ангелина 08.01.2022. Добавлено окно выигрыша и проигрыша
"""

font = pygame.font.Font(FONT, 200)
font_res = pygame.font.Font(FONT, 75)


def show_res(screen, time, kills):
    button(screen, TIME_NAME + str(int(time)) + '  ' + SEC, RED, TIME_POS, TIME_SIZE[0], TIME_SIZE[1], font_res)
    button(screen, KILLS_NAME + str(kills), BLUE, KILLS_POS, TIME_SIZE[0], TIME_SIZE[1], font_res)


class Win:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.animation_count = 0
        self.lost_frames_count = 0
        self.animation_list = self._load_picture()
        self.running = True

    def run(self, total_time, kills_count):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.running = False
            self.screen.fill(BLACK)
            self._draw(total_time, kills_count)

            pygame.display.flip()
            self.clock.tick(20)

    @staticmethod
    def _load_picture():
        animation_list = [pygame.transform.scale(load_image(TEXTURES_PATH, f'win/{i}.gif'), PICTURE_SIZE) for i in
                          range(SKELETON_AMOUNT)]
        return collections.deque(animation_list)

    def _draw(self, total_time, kills_count):
        shot_sprite = self.animation_list[0]
        self.screen.blit(shot_sprite, PICTURE_POS)
        self.animation_count += 1
        if self.animation_count == ANIMATION_SPEED:
            self.animation_list.rotate(-1)
            self.animation_count = 0
            self.lost_frames_count += 1
        color = random.randrange(0, 255)
        button(self.screen, WON, (color, color, color), SENT_POS, SENT_SIZE[0], SENT_SIZE[1], font)
        show_res(self.screen, total_time, kills_count)


class Losing:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.animation_count = 0
        self.lost_frames_count = 0
        self.animation_list = self._load_picture()
        self.running = True

    def run(self, total_time, kills_count):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.running = False
            self.screen.fill(BLACK)
            self._draw(total_time, kills_count)

            pygame.display.flip()
            self.clock.tick(20)

    @staticmethod
    def _load_picture():
        animation_list = [pygame.transform.scale(load_image(TEXTURES_PATH, f'losing/{i}.gif'), PICTURE_SIZE) for i in
                          range(SKULL_AMOUNT)]
        return collections.deque(animation_list)

    def _draw(self, total_time, kills_count):
        shot_sprite = self.animation_list[0]
        self.screen.blit(shot_sprite, PICTURE_POS)
        self.animation_count += 1
        if self.animation_count == ANIMATION_SPEED:
            self.animation_list.rotate(-1)
            self.animation_count = 0
            self.lost_frames_count += 1
        color = random.randrange(0, 255)
        button(self.screen, LOSE, (color, color, color), SENT_POS, SENT_SIZE[0], SENT_SIZE[1], font)
        show_res(self.screen, total_time, kills_count)
