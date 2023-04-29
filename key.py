import pygame
from consts import *

class Key(pygame.sprite.Sprite):
    def __init__(self, xPos, current_game):
        super().__init__()
        self.game = current_game

        self.type = xPos
        self.surf = pygame.Surface((55, 20))
        self.col = (35, 183, 231)
        self.surf.fill(self.col)
        self.rect = self.surf.get_rect(center=(xPos * 60, HEIGHT - 50))
        self.rect.size = (40, 20)
        self.pressed = False
        self.tickPressed = False

    def tick(self):
        pressedKeys = pygame.key.get_pressed()
        self.pressed = pressedKeys[KEYS[self.type]]

        if self.pressed:
            tint = (40, 40, 20)
            self.surf.fill((self.col[0] + tint[0], self.col[1] + tint[1], self.col[2] + tint[2]))

            if not self.tickPressed:
                self.tickPressed = True
                for note in self.game.map_sprites:
                    if type(note) == KEYS.HoldNote:
                        hit = self.rect.colliderect(note.rectPress)
                        if hit:
                            self.game.score(True)
                            note.pressed = True
                    else:
                        hit = self.rect.colliderect(note.rect)
                        if hit:
                            self.game.score(True)
                            note.kill()
        else:
            if self.tickPressed:
                for note in self.game.map_sprites:
                    if type(note) == KEYS.HoldNote:
                        hit = self.rect.colliderect(note.rectPress)
                        if hit:
                            if -250 < note.sizeY < 250:
                                self.game.score(True)
                            else:
                                self.game.score(False)
                            note.kill()
                            break
                self.tickPressed = False
            self.surf.fill(self.col)

