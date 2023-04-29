import json

import pygame
from pygame import mixer

from consts import *

class EndScreen(pygame.sprite.Sprite):
    def __init__(self, current_game):
        super().__init__()
        self.game = current_game

        self.surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.opacity = 0
        self.surf.fill((0, 0, 0, self.opacity))
        self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.timeToExit = 5000
        self.quitting = False

    def update(self):
        if self.game.g_player.gameEnded:
            mixer.music.stop()
            self.opacity = min(self.opacity + 10, 255)
            self.surf.fill((0, 0, 0, self.opacity))
            self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            if self.opacity == 255:
                font = pygame.font.Font('freesansbold.ttf', 16)
                # --- combo ---
                comboText = font.render('Max combo: ' + str(self.game.g_player.maxCombo), True, (255, 255, 255), (0, 0, 0))
                # --- accuracy ---
                accuracy = ((self.game.g_player.totalNotes - self.game.g_player.misses) / self.game.g_player.totalNotes) * 100
                accScore = self.game.accToScore(accuracy)
                accuracyText = font.render('Accuracy: ' + str(round(accuracy, 2)) + "% (" + accScore + ")", True,
                                           (255, 255, 255),
                                           (0, 0, 0))
                # --- progress ---
                progressText = font.render('Progress: ' + str(self.game.g_player.deathPercent) + "%", True, (255, 255, 255),
                                           (0, 0, 0))

                comboTextRect = comboText.get_rect(center=(WIDTH / 2, 80))
                accuracyTextRect = accuracyText.get_rect(center=(WIDTH / 2, 100))
                progressTextRect = progressText.get_rect(center=(WIDTH / 2, 120))

                self.game.displaysurface.blit(comboText, comboTextRect)
                self.game.displaysurface.blit(accuracyText, accuracyTextRect)
                self.game.displaysurface.blit(progressText, progressTextRect)
                self.timeToExit -= self.game.g_time
                if self.timeToExit <= 0:
                    self.quitting = True

                    saveData = {
                        "data": self.game.data_path,
                        "audio": self.game.audio_path
                    }
                    saveFile = open("save.json", "w")
                    saveFile.write(json.dumps(saveData))
                    saveFile.close()
                    pygame.quit()

# ----------------------------------------------------------------------------------------------------------------------
