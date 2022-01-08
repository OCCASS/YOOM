import pygame
import pygame_gui

from config import *


class Menu:
    def __init__(self, manager):
        self.manager = manager
        self.hello_button = pygame_gui.elements.UIButton(text='hello', relative_rect=pygame.Rect(0, 0, 100, 100),
                                                    manager=self.manager)
