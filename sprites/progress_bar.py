import pygame
from consts import *


class ProgressBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 200
        self.col = (255, 255, 255)

    def tick(self, percent):
        mult = percent / 100
        self.surf = pygame.Surface((WIDTH * mult, 5))
        self.surf.fill(self.col)
        self.rect = self.surf.get_rect(center=(WIDTH / 2 * mult, HEIGHT - 5))