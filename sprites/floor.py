import pygame
from consts import *
from notes.hold_note import HoldNote


class Floor(pygame.sprite.Sprite):
    def __init__(self, current_game):
        super().__init__()
        self.game = current_game

        self.surf = pygame.Surface((WIDTH, 10))
        self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT + 100))

    def tick(self):
        if self.game.g_player.gameEnded:
            return
        for i in self.game.map_sprites:
            if i.rect.colliderect(self.rect):
                if type(i) == HoldNote:
                    self.game.score(False)
                    self.game.score(False)
                else:
                    self.game.score(False)
                i.kill()