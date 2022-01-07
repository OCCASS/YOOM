import pygame

"""
Батталов Арслан 05.01.2022 Добавлен класс Music и SoundEffect
Батталов Арслан 07.01.2022. Добавлен класс GunSound
"""


class Music:
    def __init__(self, path):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        self.init_track(path)

    def init_track(self, path):
        self.theme = pygame.mixer.music
        self.theme.load(path)

    def play_music(self):
        self.theme.set_volume(0.5)
        self.theme.play(-1)


class SoundEffect(Music):
    def __init__(self, path):
        super().__init__(path)

    def init_track(self, path):
        self.effect = pygame.mixer.Sound(path)

    def play_sound(self):
        if not pygame.mixer.Channel(2).get_busy():
            pygame.mixer.Channel(2).play(self.effect)


class GunSound(SoundEffect):
    def play_sound(self):
        if not pygame.mixer.Channel(1).get_busy():
            pygame.mixer.Channel(1).play(self.effect)
