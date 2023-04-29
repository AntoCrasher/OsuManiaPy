from pygame.locals import *
from pygame import mixer
import json
import time
import pygame
import os

# ----------------------------------------------------------------------------------------------------------------------

vec = pygame.math.Vector2
keys = {
    1: K_s,
    2: K_d,
    3: K_SEMICOLON,
    4: K_QUOTE
}

HEIGHT = 540
WIDTH = 300
FPS = 60

# ----------------------------------------------------------------------------------------------------------------------

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
        self.pressed = pressedKeys[keys[self.type]]

        if self.pressed:
            tint = (40, 40, 20)
            self.surf.fill((self.col[0] + tint[0], self.col[1] + tint[1], self.col[2] + tint[2]))

            if not self.tickPressed:
                self.tickPressed = True
                for note in self.game.map_sprites:
                    if type(note) == Hold:
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
                    if type(note) == Hold:
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
class Hold(pygame.sprite.Sprite):
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
            self.t += FramePerSec.get_time()
            self.sizeY = HEIGHT - self.rect.y - 50
            self.surf = pygame.Surface((60, max(self.sizeY, 0)))
            self.surf.fill(self.col)
            self.rect.size = (40, max(self.sizeY, 0))
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
                if type(i) == Hold:
                    self.game.score(False)
                    self.game.score(False)
                else:
                    self.game.score(False)
                i.kill()
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
                self.timeToExit -= FramePerSec.get_time()
                if self.timeToExit <= 0:
                    self.quitting = True

                    saveData = {
                        "data": dataPath,
                        "audio": audioPath
                    }
                    saveFile = open("save.json", "w")
                    saveFile.write(json.dumps(saveData))
                    saveFile.close()
                    pygame.quit()
class OsuMania:
    def __init__(self, dataPath, audioPath):
        self.all_sprites = pygame.sprite.Group()
        self.map_sprites = pygame.sprite.Group()
        self.speed = 0.55

        self.acc_scores = [
            [100, 'SS'],
            [95, 'S'],
            [90, 'A'],
            [80, 'B'],
            [60, 'C'],
            [0, 'D']
        ]

        mapText = open(dataPath, encoding="utf8").read()
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
        mixer.music.load(audioPath)
        mixer.music.set_volume(0.2)

        pygame.init()
        self.displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(dataPath.split("- ")[1])

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
            holdTime = int(data[5].split(":")[0])
            isHold = holdTime - int(data[2]) > 0

            x = ma[int(int(data[0]) / 64)]
            y = int(data[2]) * self.speed
            length = max(length, y)
            if isHold:
                t = int((holdTime - int(data[2])) * self.speed)
                newNote = Hold(x, y, t, self)
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
        if type(lastNote) == Hold:
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
            if type(entity) == Hold:
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
            self.g_time += FramePerSec.get_time()
            FramePerSec.tick(FPS)
            return True
        else:
            return False

# ----------------------------------------------------------------------------------------------------------------------

def chooseMap():
    for map in maps:
        if len(map.split(".DS_Store")) > 1:
            continue
        mapDirPath = allMapsPath + "/" + map
        mapDir = os.listdir(mapDirPath)

        newMap = {
            "path": mapDirPath,
            "audio": [],
            "data": []
        }
        for i in mapDir:
            if len(i.split(".mp3")) > 1 or len(i.split(".ogg")) > 1:
                newMap["audio"].append(mapDirPath + "/" + i)
            if len(i.split(".osu")) > 1:
                newMap["data"].append(mapDirPath + "/" + i)
        mapList.append(newMap)
    for i in range(len(mapList)):
        print(i + 1, mapList[i]["path"], sep=") ")
    allAudios = []
    allDatas = []
    while True:
        mapPath = input("Select Map: ")
        if mapPath.isnumeric() and 0 < int(mapPath) <= len(mapList):
            mapPath = mapList[int(mapPath) - 1]
            allAudios = mapPath["audio"]
            allDatas = mapPath["data"]
            break
        else:
            print("Select a valid option")
    for i in range(len(allAudios)):
        audioPath = allAudios[i].split("/")
        print(i + 1, audioPath[len(audioPath) - 1], sep=") ")
    while True:
        audioPath = input("Select Audio: ")
        if audioPath.isnumeric() and 0 < int(audioPath) <= len(allAudios):
            audioPath = allAudios[int(audioPath) - 1]
            print("Selected: ", audioPath.split("/")[len(audioPath.split("/")) - 1])
            break
        else:
            print("Select a valid option")
    for i in range(len(allDatas)):
        dataPath = allDatas[i].split("/")
        print(i + 1, dataPath[len(dataPath) - 1], sep=") ")
    while True:
        dataPath = input("Select Data: ")
        if dataPath.isnumeric() and 0 < int(dataPath) <= len(allDatas):
            dataPath = allDatas[int(dataPath) - 1]
            print("Selected: ", dataPath.split("/")[len(dataPath.split("/")) - 1])
            break
        else:
            print("Select a valid option")
    print("\nResult:")
    print(dataPath)
    print(audioPath)

    return [dataPath, audioPath]

while True:
    allMapsPath = "maps"
    maps = os.listdir(allMapsPath)
    mapList = []

    dataPath = ""
    audioPath = ""

    replay = False

    print()
    print("Key binds: ")
    print("|   |   |   |   |")
    print("|   |   |   |   |")
    print(f"| {chr(keys[1])} | {chr(keys[2])} | {chr(keys[3])} | {chr(keys[4])} |")
    print("|   |   |   |   |")
    print()

    if os.path.exists("save.json"):
        save = open("save.json").read()
        loaded = json.loads(save)
        dataSplit = loaded["data"].split("/")
        print("Do you want to replay last map:", dataSplit[len(dataSplit) - 1].split(".")[0])
        repInp = input("Enter (y/n): ").lower()
        if repInp == "y" or repInp == "yes":
            dataPath = loaded["data"]
            audioPath = loaded["audio"]
            replay = True
    if not replay:
        datas = chooseMap()
        dataPath = datas[0]
        audioPath = datas[1]

    game = OsuMania(dataPath, audioPath)

    print()
    print("Click on your game window")
    print("Starting in:")
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    print("Good Luck!")

    FramePerSec = pygame.time.Clock()
    while True:
        if not game.tick():
            break

    print()
    print("Results:")
    print()
    res = game.g_player.get_stats_str()
    print("Progress:", str(res['progress']) + "%")
    print("Max Combo:", res['max_combo'])
    print("Misses:", res['misses'])
    print("Accuracy:", str(round(res['accuracy'] * 100) / 100) + "%", f"({res['score']})")
