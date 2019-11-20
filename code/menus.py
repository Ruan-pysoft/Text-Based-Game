import os

if os.name == 'nt': #on Windows System
    clear = lambda: os.system('cls') # command to clear the console
else: #on Linux System
    clear = lambda: os.system('clear') # command to clear the console

class MenuAction: # like a action, but for a menu, not the player
    def __init__(self, method, name, **kwargs):
        self.method = method # function/method to run
        self.name = name # name to be printed to screen
        self.kwargs = kwargs # other stuff

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

class Menu: # Here we start using menus!
    def __init__(self, name, actions, **kwargs):
        self.name = name # name to be printed to screen
        self.actions = actions # available menu actions
        self.kwargs = kwargs # other stuff

        clear() # clear the console window
        import main
        main.menu = self
        main.update_screen()

    def __str__(self):
        return "{}".format(self.name)

    def show(self):
        print(f'{self.name}:\n =========== \n\n') # print the menu's name
        for i, a in enumerate(self.actions, 1): # print every available menu action
            print(f'{i}: {a}')
        self.action = -1
        def get_action(): # get user input
            try:
                self.action = int(input('Choose an action: ')) - 1
            except:
                print("That isn't a valid action!")
                get_action()
        get_action()
        self.actions[self.action].method() # do what the user says

class TitleScreen(Menu): # title screen or main menu
    def __init__(self):
        super().__init__(name='Title Screen', actions=[OpenSettings(), PlayGame(), LoadGame(), QuitGame()])

class Settings(Menu): # settings screen
    def __init__(self):
        super().__init__(name='Settings', actions=[MainMenu()]) # currently there's no settings

def getmap():
    maps = []
    for file in os.listdir("./resources"):
        if file.endswith(".map"):
            maps.append('.'.join(file.split('.')[:-1]))
    for i, m in enumerate(maps, 1):
        print(f'{i}) {m}')
    print('Q) Quit to Title\n')
    def get_map():
            m = input('Choose a map: ')
            if m.lower() == 'q':
                TitleScreen()
            try:
                m = int(m)
            except:
                print("That isn't a valid map!")
            if int(m) > len(maps) or int(m) < 1:
                print("That isn't a valid map!")
                get_map()
            else:
                return m
    m = get_map() # for some reason this is neaded because "return get_map()" either doesn't return or returns None
    clear()
    return m

class NewGame(Menu): # start a new game
    def __init__(self):
        super().__init__(name='New Game', actions=[])

    def show(self):
        import game
        global getmap
        print(f'Choose a map:\n ========== \n\n')
        game.play(getmap()) # make a game with a map of the player's choosing
        TitleScreen()

class OldGame(Menu):
    def __init__(self):
        import save
        super().__init__(name='Load a Game', actions=save.list_saves())

    def show(self):
        print(f'Load a Game:\n ========= \n\n')
        for i, a in enumerate(self.actions, 1):
            print(f'{i}) {a}') # list all the saves

        print('Q) Quit to Title\n')

        self.action = -1
        def get_action():
            self.action = input('Choose a save: ')
            if self.action.lower() == 'q':
                TitleScreen()
            try:
                self.action = int(self.action)
            except:
                print("That isn't a valid save!")
                get_action()
            if int(self.action) > len(self.actions) or int(self.action) < 1:
                print("That isn't a valid save!")
                get_action()
        get_action()
        import game
        clear()
        game.play(self.action, l=True) # continue playing on that save
        TitleScreen()
