import pygame as pygame
from key import Key

class Player(pygame.sprite.Sprite):
    def __init__(self, current_game):
        super().__init__()
        self.game = current_game

        self.keys = [Key(1, current_game), Key(2, current_game), Key(3, current_game), Key(4, current_game)]
        for key in self.keys:
            self.game.all_sprites.add(key)
        # --- stats ---
        self.combo = 0
        self.health = 100
        self.misses = 0
        self.totalNotes = 0
        self.maxCombo = 0
        # -------------
        self.gameEnded = False

    def showStats(self):
        self.percent = round(100 - self.game.getLastY() / self.game.map_length * 100, 1)
        if self.health == 0 and not self.gameEnded:
            self.deathPercent = self.percent
            self.gameEnded = True
        if self.combo > self.maxCombo:
            self.maxCombo = self.combo
        font = pygame.font.Font('freesansbold.ttf', 16)
        comboText = font.render('Combo: ' + str(self.combo) + " / " + str(self.maxCombo), True, (255, 255, 255),
                                (0, 0, 0))
        comboTextRect = comboText.get_rect()
        self.game.displaysurface.blit(comboText, comboTextRect)

        accuracy = 100.0
        if self.totalNotes > 0:
            accuracy = ((self.totalNotes - self.misses) / self.totalNotes) * 100
        acc_score = self.game.accToScore(accuracy)
        accuracyText = font.render('Accuracy: ' + str(round(accuracy, 2)) + "% (" + acc_score + ")", True,
                                   (255, 255, 255), (0, 0, 0))
        accuracyTextRect = accuracyText.get_rect()
        accuracyTextRect.y = 20
        self.game.displaysurface.blit(accuracyText, accuracyTextRect)

    def get_stats_str(self):
        accuracy = ((self.totalNotes - self.misses) / self.totalNotes) * 100
        result = {
            'progress': self.deathPercent,
            'max_combo': self.maxCombo,
            'misses': self.misses,
            'accuracy': ((self.totalNotes - self.misses) / self.totalNotes) * 100,
            'score': self.game.accToScore(accuracy)
        }
        return result

