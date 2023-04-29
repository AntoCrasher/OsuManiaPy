import pygame
from consts import *


class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 200
        self.surfMax = pygame.Surface((15, self.size))
        self.surfCur = pygame.Surface((15, self.size))
        self.surfCur.fill((0, 255, 0))
        self.surfMax.fill((255, 255, 255))

        self.xPos = WIDTH - 15

        self.rectMax = self.surfMax.get_rect(center=(self.xPos, HEIGHT / 2 - self.surfMax.get_size()[1] / 2 + 160))
        self.rectCur = self.surfCur.get_rect(center=(self.xPos, HEIGHT / 2 - self.surfCur.get_size()[1] / 2 + 160))

    def update(self, health, maxHealth):
        self.surfCur = pygame.Surface((15, self.size * (health / maxHealth)))
        self.surfCur.fill((0, 255, 0))
        self.rectCur = self.surfCur.get_rect(center=(self.xPos, HEIGHT / 2 - self.surfCur.get_size()[1] / 2 + 160))