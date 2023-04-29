import pygame
from pygame import mixer

from consts import *
from notes.hold_note import HoldNote
from notes.note import Note
from player import Player
from screens.end_screen import EndScreen
from sprites.floor import Floor
from sprites.health_bar import HealthBar
from sprites.progress_bar import ProgressBar

class OsuMania:
    def __init__(self, data_path, audio_path):
        self.data_path = data_path
        self.audio_path = audio_path
        self.all_sprites = pygame.sprite.Group()
        self.map_sprites = pygame.sprite.Group()
        self.speed = 0.55
        self.clock = pygame.time.Clock()

        self.acc_scores = [
            [100, 'SS'],
            [95, 'S'],
            [90, 'A'],
            [80, 'B'],
            [60, 'C'],
            [0, 'D']
        ]

        mapText = open(data_path, encoding="utf8").read()
        self.mapTextToData(mapText)
        self.map_length = self.getLastY()

        self.g_player = Player(self)
        self.g_floor = Floor(self)
        self.g_healthbar = HealthBar()
        self.g_endscreen = EndScreen(self)
        self.g_progressbar = ProgressBar()
        self.g_time = 0

        self.p = False
        self.musicIndex = HEIGHT - 50 + 10000

        mixer.init()
        mixer.music.load(audio_path)
        mixer.music.set_volume(0.2)

        pygame.init()
        self.displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(data_path.split("- ")[1])

    def accToScore(self, percent):
        for i in self.acc_scores:
            if percent >= i[0]:
                return i[1]

    def mapTextToData(self, text):
        hitObjects = text.split("[HitObjects]\n")[1]
        length = 0
        for i in hitObjects.split("\n"):
            data = i.split(",")
            if len(data) == 1:
                continue
            ma = {
                1: 1,
                3: 2,
                5: 3,
                7: 4
            }
            HoldNoteTime = int(data[5].split(":")[0])
            isHoldNote = HoldNoteTime - int(data[2]) > 0

            x = ma[int(int(data[0]) / 64)]
            y = int(data[2]) * self.speed
            length = max(length, y)
            if isHoldNote:
                t = int((HoldNoteTime - int(data[2])) * self.speed)
                newNote = HoldNote(x, y, t, self)
            else:
                newNote = Note(x, y, self)
            self.all_sprites.add(newNote)
            self.map_sprites.add(newNote)
        return length

    def getLastY(self):
        if len(self.map_sprites.sprites()) == 0:
            self.g_player.deathPercent = 100.0
            self.g_player.gameEnded = True
            return 0
        lastNote = self.map_sprites.sprites()[len(self.map_sprites.sprites()) - 1]
        if type(lastNote) == HoldNote:
            return lastNote.rectPress.y
        return lastNote.rect.y

    def score(self, miss):
        self.g_player.totalNotes += 1
        if miss:
            self.g_player.combo += 1
            self.g_player.health = min(self.g_player.health + 3, 100)
        else:
            self.g_player.combo = 0
            self.g_player.misses += 1
            self.g_player.health = max(self.g_player.health - 15, 0)

    def tick(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
        self.musicIndex -= self.g_time * self.speed
        if self.musicIndex <= 0 and not self.p:
            self.p = True
            mixer.music.play()

        self.displaysurface.fill((0, 0, 0))

        for entity in self.all_sprites:
            self.displaysurface.blit(entity.surf, entity.rect)
            if type(entity) == HoldNote:
                self.displaysurface.blit(entity.surfPress, entity.rectPress)

        # --- update ---
        for key in self.g_player.keys:
            key.tick()

        for note in self.map_sprites:
            note.tick()

        self.g_floor.tick()

        self.g_healthbar.update(self.g_player.health, 100)
        self.displaysurface.blit(self.g_healthbar.surfMax, self.g_healthbar.rectMax)
        self.displaysurface.blit(self.g_healthbar.surfCur, self.g_healthbar.rectCur)
        self.g_player.showStats()

        self.g_progressbar.tick(self.g_player.percent)
        self.displaysurface.blit(self.g_progressbar.surf, self.g_progressbar.rect)

        self.displaysurface.blit(self.g_endscreen.surf, self.g_endscreen.rect)
        self.g_endscreen.update()

        if not self.g_endscreen.quitting:
            pygame.display.update()
            self.g_time += self.clock.get_time()
            self.clock.tick(FPS)
            return True
        else:
            return False
