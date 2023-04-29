import os
import requests
import zipfile
from ossapi import Ossapi

api = Ossapi(21849, 'PcS7KBx1x0M30fgwhSiDIFpszAA9Cvx69djDZD06')
def download(id):
    to_replace = ['\\','/',':','*','?','"','<','>','|']

    map = api.beatmapset(id)
    name = str(id) + ' ' + map.artist + ' - ' + map.title
    for i in to_replace:
        name = name.replace(i, ' ')
    name = name.strip(' ')

    print("Downloading:", name)

    path = f'./maps/{name}.osz'
    directory_to_extract_to = f'./maps/{name}/'

    print("Requesting .osz file")
    resp = requests.get(f'https://beatconnect.io/b/{id}')
    with open(path, 'wb') as f:
        for buff in resp:
            f.write(buff)

    print("Extracting .osz")
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)

    print("Removing .osz")
    os.remove(path)
    print("Done.")

maps_to_download = [
    1288045
]

for i in maps_to_download:
    download(i)
