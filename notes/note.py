import pygame

class Note(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, current_game):
        super().__init__()
        self.game = current_game

        self.type = xPos

        self.surf = pygame.Surface((60, 20))
        self.col = (33, 214, 231)
        self.surf.fill(self.col)

        self.yPos = -yPos

        self.rect = self.surf.get_rect(center=(xPos * 60, self.yPos))
        self.rect.size = (40, 90)

        self.vel = self.game.speed

    def tick(self):
        self.rect.y = self.yPos + self.game.g_time * self.game.speed