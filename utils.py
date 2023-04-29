import os

def choose_map():

    allMapsPath = "maps"
    maps = os.listdir(allMapsPath)
    mapList = []

    dataPath = ""
    audioPath = ""

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