import game, player, world
import functions as f
import csv, pickle, json, os
from inspect import currentframe, getframeinfo
from pathlib import Path

def save(data, save, file):
    path = str(Path(getframeinfo(currentframe()).filename).resolve().parent) + str(Path(f'/saves/{save}/'))
    file = path + f'\\{file}.json'
    if not os.path.exists(path):
        os.makedirs(path)
    with open(file, 'w') as f:
        json.dump(data, f, indent=2, separators=(',', ':'))

def load(save, file):
    file = str(Path(getframeinfo(currentframe()).filename).resolve().parent) + str(Path(f'/saves/{save}/{file}.json'))
    with open(file, 'r') as f:
        return json.load(f)

def list_saves():
    path = str(Path(getframeinfo(currentframe()).filename).resolve().parent) + str(Path(f'/saves/'))
    #print(path)
    #print([di for di in os.listdir(path=path) if os.path.isdir(os.path.join(path,di))])
    return [di for di in os.listdir(path=path) if os.path.isdir(os.path.join(path,di))]

def save_settings(settings):
    path = str(Path(getframeinfo(currentframe()).filename).resolve().parent)
    file = path + '\\settings.json'
    with open(file, 'w') as f:
        json.dump(settings, f, indent=2, separators=(',', ':'))

def load_settings():
    path = str(Path(getframeinfo(currentframe()).filename).resolve().parent)
    file = path + '\\settings.json'
    with open(file, 'r') as f:
        return json.load(f)

def settings():
    defualt_settings = {}
    if not os.path.exists(str(Path(getframeinfo(currentframe()).filename).resolve().parent) + '\\settings.json'):
        save_settings(defualt_settings)
    return load_settings()
