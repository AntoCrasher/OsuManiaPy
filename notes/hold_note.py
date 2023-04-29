import pygame
from consts import *


class HoldNote(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, holdTime, current_game):
        super().__init__()
        self.game = current_game

        self.type = xPos
        self.sizeY = holdTime
        if holdTime < 0:
            del self
            return
        self.surf = pygame.Surface((60, holdTime))
        self.col = (50, 50, 50)
        self.surf.fill(self.col)

        self.yPos = -yPos - holdTime
        self.holdTime = holdTime

        # --- press ---

        self.surfPress = pygame.Surface((60, 20))
        self.colPress = (33, 214, 231)
        self.surfPress.fill(self.colPress)
        self.rectPress = self.surfPress.get_rect(center=(xPos * 60, -yPos))
        self.rectPress.size = (40, 60)

        # --------------

        self.rect = self.surf.get_rect(center=(xPos * 60, self.yPos))
        self.rect.size = (40, holdTime + 20)
        self.pressed = False
        self.t = 0
        self.vel = self.game.speed


    def tick(self):
        self.rect.y = self.yPos + self.game.g_time * self.game.speed
        if not self.pressed:
            self.rectPress.y = self.yPos + self.holdTime + self.game.g_time * self.game.speed
            self.t = 0
        else:
            self.rectPress.y = HEIGHT - 60
            self.t += self.game.g_time
            self.sizeY = HEIGHT - self.rect.y - 50
            self.surf = pygame.Surface((60, max(self.sizeY, 0)))
            self.surf.fill(self.col)
            self.rect.size = (40, max(self.sizeY, 0))