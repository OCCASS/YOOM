import pygame
import sys
import collections
import random

from config import *
from menu import button
from load_image import load_image

font = pygame.font.Font(FONT, 200)


class Win:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.animation_count = 0
        self.lost_frames_count = 0
        self.animation_list = self._load_picture()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.running = False
            self.screen.fill('black')
            self._draw()

            pygame.display.flip()
            self.clock.tick(20)

    @staticmethod
    def _load_picture():
        animation_list = [pygame.transform.scale(load_image(TEXTURES_PATH, f'win/{i}.gif'), (400, 400)) for i in
                          range(11)]
        return collections.deque(animation_list)

    def _draw(self):
        shot_sprite = self.animation_list[0]
        self.screen.blit(shot_sprite, (800, 100))
        self.animation_count += 1
        if self.animation_count == ANIMATION_SPEED:
            self.animation_list.rotate(-1)
            self.animation_count = 0
            self.lost_frames_count += 1
        color = random.randrange(0, 255)
        button(self.screen, "YOU WON", (color, color, color), (10, 165), 250, 100, font)


class Losing:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.animation_count = 0
        self.lost_frames_count = 0
        self.animation_list = self._load_picture()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.running = False
            self.screen.fill('black')
            self._draw()

            pygame.display.flip()
            self.clock.tick(20)

    @staticmethod
    def _load_picture():
        animation_list = [pygame.transform.scale(load_image(TEXTURES_PATH, f'losing/{i}.gif'), (400, 400)) for i in
                          range(3)]
        return collections.deque(animation_list)

    def _draw(self):
        shot_sprite = self.animation_list[0]
        self.screen.blit(shot_sprite, (800, 100))
        self.animation_count += 1
        if self.animation_count == ANIMATION_SPEED:
            self.animation_list.rotate(-1)
            self.animation_count = 0
            self.lost_frames_count += 1
        color = random.randrange(0, 255)
        button(self.screen, "YOU LOSE", (color, color, color), (10, 165), 250, 100, font)

