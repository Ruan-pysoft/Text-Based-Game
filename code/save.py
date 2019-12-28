import functions as f
import json, os
from inspect import currentframe, getframeinfo
from pathlib import Path

def make_valid_file(name):
    invalid_symbols = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for s in invalid_symbols:
        name = name.replace(s, '_')
    return name

def save(data, save, file): # save data to a save
    path = str(Path(getframeinfo(currentframe()).filename).resolve().parent) + str(Path(f'/saves/{make_valid_file(save)}/'))
    file = path + f'\\{file}.json'
    if not os.path.exists(path):
        os.makedirs(path)
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, separators=(',', ':'))

def load(save, file): # load data from a save
    file = str(Path(getframeinfo(currentframe()).filename).resolve().parent) + str(Path(f'/saves/{save}/{file}.json'))
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_saves(): # list all folders in the './saves' directory
    path = str(Path(getframeinfo(currentframe()).filename).resolve().parent) + str(Path(f'/saves/'))
    #print(path)
    #print([di for di in os.listdir(path=path) if os.path.isdir(os.path.join(path,di))])
    return [di for di in os.listdir(path=path) if os.path.isdir(os.path.join(path,di))]

def save_settings(settings): # save settings (the game currently has no settings)
    path = str(Path(getframeinfo(currentframe()).filename).resolve().parent)
    file = path + '\\settings.json'
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, separators=(',', ':'))

def load_settings(): # load settings (the game currently has no settings)
    path = str(Path(getframeinfo(currentframe()).filename).resolve().parent)
    file = path + '\\settings.json'
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

def settings(): # get settings (the game currently has no settings)
    defualt_settings = {}
    if not os.path.exists(str(Path(getframeinfo(currentframe()).filename).resolve().parent) + '\\settings.json'):
        save_settings(defualt_settings)
    return load_settings()
