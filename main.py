import json
import time
import pygame
import os

from consts import *
from osu_mania import OsuMania
from utils import choose_map

while True:
    print()
    print("Key binds: ")
    print("|   |   |   |   |")
    print("|   |   |   |   |")
    print(f"| {chr(KEYS[1])} | {chr(KEYS[2])} | {chr(KEYS[3])} | {chr(KEYS[4])} |")
    print("|   |   |   |   |")
    print()

    replay = False

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
        datas = choose_map()
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
