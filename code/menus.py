import os

if os.name == 'nt':
    clear = lambda: os.system('cls') #on Windows System
else:
    clear = lambda: os.system('clear') #on Linux System

class MenuAction:
    def __init__(self, method, name, **kwargs):
        self.method = method
        self.name = name
        self.kwargs = kwargs
 
    def __str__(self):
        return "{}".format(self.name)

class OpenSettings(MenuAction):
    def __init__(self):
        super().__init__(method=Settings, name='View Settings')

class QuitGame(MenuAction):
    def __init__(self):
        import sys
        super().__init__(method=sys.exit, name='Quit Game')

class MainMenu(MenuAction):
    def __init__(self):
        super().__init__(method=TitleScreen, name='Quit to Title Screen')

class PlayGame(MenuAction):
    def __init__(self):
        super().__init__(method=NewGame, name='Start a new game')

class LoadGame(MenuAction):
    def __init__(self):
        super().__init__(method=OldGame, name='Load a save')

class Menu:
    def __init__(self, name, actions, **kwargs):
        self.name = name
        self.actions = actions
        self.kwargs = kwargs

        clear()
        import main
        main.menu = self
        main.update_screen()
 
    def __str__(self):
        return "{}".format(self.name)

    def show(self):
        print(f'{self.name}:\n =========== \n\n')
        for i, a in enumerate(self.actions, 1):
            print(f'{i}: {a}')
        self.action = -1
        def get_action():
            try:
                self.action = int(input('Choose an action: ')) - 1
            except:
                print("That isn't a valid action!")
                get_action()
        get_action()
        self.actions[self.action].method()

class TitleScreen(Menu):
    def __init__(self):
        super().__init__(name='Title Screen', actions=[OpenSettings(), PlayGame(), LoadGame(), QuitGame()])

class Settings(Menu):
    def __init__(self):
        super().__init__(name='Settings', actions=[MainMenu()])

def getmap():
    maps = []
    for file in os.listdir("./resources"):
        if file.endswith(".map"):
            maps.append('.'.join(file.split('.')[:-1]))
    for m in maps:
        print(m)
    def get_map():
            m = input('Choose a save: ')
            if m not in maps:
                print("That isn't a valid map!")
                get_map()
            else:
                return m
    m = get_map() # for some reason this is neaded because "return get_map()" either doesn't return or returns None
    return m

class NewGame(Menu):
    def __init__(self):
        super().__init__(name='Game', actions=[])

    def show(self):
        import game
        global getmap
        game.play(getmap())
        Menu()

class OldGame(Menu):
    def __init__(self):
        super().__init__(name='Game', actions=save.list_saves())

    def show(self):
        print(f'Load a Game:\n ========= \n\n')
        for a in self.actions:
            print(f'{a}')
        
        self.action = -1
        def get_action():
            self.action = input('Choose a save: ')
            if self.action not in self.actions:
                print("That isn't a valid save!")
                get_action()
        get_action()
        import game
        game.play(self.action, l=True)
        Menu()
