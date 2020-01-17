import world, mainclasses, items, enemies, tiles
import save as ssave

class _:
    def __init__(self):
        get = lambda x: variables[x]

    def __repr__(self):
        return str([v for v in variables])

    def get(self, var):
        return variables[var]

variables = {'Game variables': {}, 'Player': None, 'World': None}
s = ''

var = _()

def main():
    global s
    print('Saves:')
    for i, a in enumerate(ssave.list_saves(), 1):
        print(f'{i}) {a}') # list all the saves
    o = input("Which save do you want to load? ")
    try:
        o = int(o)
        if int(o) > len(ssave.list_saves()) or int(o) < 1:
            print("That isn't a valid save!")
            main()
    except:
        print("That isn't a valid number!")
        main()
    s = ssave.list_saves()[o - 1]
    load()
    print('Variables:\n  "Game variables", "Player", "World"\nAccess with "get(variable)" or "variables[variable]"\nSave the game with "save()"')

def load():
    variables['Player'] = ssave.load(s, 'player')
    world.load(ssave.load(s, 'world')) #load the world
    variables['World'] = world._world
    data = ssave.load(s, 'game') # retrieve game data
    variables['Game variables']['Current turn'] = data['turn'] # set current turn
    variables['Game variables']['Previous turn'] = data['prev. turn'] # set previous turn

def save():
    ssave.save(variables['Player'], s, 'player')
    ssave.save(world._world, s, 'world')
    ssave.save({'turn': variables['Game variables']['Current turn'], 'prev. turn': variables['Game variables']['Previous turn']}, s, 'game')

print('I recomend that you back up the save you want to edit!')

main()
print(world.full_string())
