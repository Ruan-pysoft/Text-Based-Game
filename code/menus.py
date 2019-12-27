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

class OpenTutorial(MenuAction):
    def __init__(self):
        super().__init__(method=Tutorial, name='View Tutorial')

class OpenHelp(MenuAction):
    def __init__(self):
        super().__init__(method=Help, name='View Help')

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
        self.__class__.actions=[PlayGame(), LoadGame(), OpenHelp(), OpenTutorial(), OpenSettings(), QuitGame()]
        super().__init__(name='Title Screen', actions=self.__class__.actions)

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
                return maps[m - 1]
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
                print("That isn't a valid number!")
                get_action()
            if int(self.action) > len(self.actions) or int(self.action) < 1:
                print("That isn't a valid save!")
                get_action()
        get_action()
        import game
        clear()
        game.play(self.actions[self.action - 1], l=True) # continue playing on that save
        TitleScreen()

class Tutorial(Menu):
    def __init__(self):
        import save
        super().__init__(name='Load a Game', actions=save.list_saves())

    def show(self):
        print(f'Tutorial:\n ========= \n\n')
        print(f'''(I suggest playing this tutorial in fullscreen, otherwise you may need to scroll around sometimes)

  When choosing "Start a new game" from the main menu you will be confronted with the following screen:
    Choose a map:
     ==========


    1) Map 1
    2) Map 2
    ...
    n) Map n
    Q) Quit to Title

    Choose a map:
On this screen you are expected to select a map to play on. You select a map by typing the number in front of the ")" and then pressing ENTER. You can also quit to title using "Q" or "q" in stead of a number.
In this tutorial we will asume you have selected "basic world", one of the two defualt maps that comes with the game, and is map 1 by defualt.
''')
        input('Press ENTER to continue... ')
        clear()
        print(f'''  When you have selected the "basic world" map you will see the following screen:

            You find yourself in a cave with a flickering torch on the wall.
            You can make out four paths, each equally as dark and foreboding.


    Play Turn 1, Choose an Action:

    d: Move East
    a: Move West
    w: Move North
    s: Move South
    e: View Inventory
    r: Rest
    R: Rest until healed (DANGEROUS IF FIGHTING ENEMY!)
    stats: View stats
    Menu: Save/Load/Quit Game
    Action:
So what does all this meen? Well, I'll split it up into setions.
''')
        input('Press ENTER to discover the sections... ')
        clear()
        print(f'''  SECTION I: Room Description:

            You find yourself in a cave with a flickering torch on the wall.
            You can make out four paths, each equally as dark and foreboding.

  This is just so that you know what the room you are in looks like, and has no pupose except to make the game playable. (Without it, it would be like stumbling around, deaf and blind in the map, only knowing in what direction you can go, what items you have, and how hurt you are)

SECTION II: Play turn:

    Play Turn 1, Choose an Action:

  This only tells you how long you've been playing.

SECTION III: Action:

    d: Move East
    a: Move West
    w: Move North
    s: Move South
    e: View Inventory
    r: Rest
    R: Rest until healed (DANGEROUS IF FIGHTING ENEMY!)
    stats: View stats
    Menu: Save/Load/Quit Game
    Action:

  This is where you do stuff.
''')
        input('Press ENTER to find out what stuff you can do... ')
        clear()
        print(f'''  So, firstly, you can move around:

    d: Move East
    a: Move West
    w: Move North
    s: Move South
    Action:

  Let me explain. You're in a world, so let me draw (badly drawn) a map for you:
____________
|      !!  |
|  ¢¢__:(  |
|    __    |
|    __    |
|##__::__$$|
|    ¢¢    |
|    __    |
|    :(    |
¯¯¯¯¯¯¯¯¯¯¯¯
  So, to clarify, every two symbols next to each other are one room. So let me give you the map key:

    KEY:
    :: = Where you start
       = Nothing, can't go here
    __ = Empty room
    :( = Room with a certain enemy in it
    ¢¢ = Room with only a coin in it
    $$ = Room with a lot of loot in it
    ## = Room with an enemy in it that can explode if it has low health

  As you can see, there are rooms surounding you on all sides, and because of that you can move in four directions (you cannot move diagnally). If you were to select "d" (by pressing the "d" key and then pressing ENTER), you would go "left" on this map, and "a" would make you go "right". If you were to select "w" you would go "up", and "s" would make you go "down".
''')
        input('Press ENTER to find out what other stuff you can do... ')
        clear()
        print(f'''  Secondly, you can view your stats and save/exit your game (or load a new one):

    e: View Inventory
    stats: View stats
    Menu: Save/Load/Quit Game
    Action:

  So if you select "e", you can see what items you have:

    Action: e

    ==========
    Inventory:

    Silver Coin
    =====
    A round coin with 10 stamped on the front.
    Value: 10


    Rock
    =====
    A fist-sized rock, suitable for bludgeoning.
    Value: 0
    Damage: 6

  As you can see, you start this map with only a silver coin and a rock.
  Your second option is to view your health and other stats:

    Action: stats

    ==========
    Health:
    50/50HP
    ==========
    Damage:
    1.0
    ==========
    Damage Resistance:
    Blunt: 8.9%
    Sharp: 9.0%
    Explotion: -31.0%
    ==========

  As you can see, this game's damage system is not as simple as it may look at first glance (NOTE: Your resistances are randomly generated within a certain range every time you start a new game). It has three types of damage: Blunt damage, Sharpness damage and Explotion damage. You may be confused about the negitive Explotion damage, but all that it means is that if something deals 10 explotion damage to you, your health will go down with 13.1 HP, instead of 9.1 HP, if it was sharpness damage.
  And lastly, you can save your game, load a old save, or quit to the main menu.
''')
        input('Press ENTER to find out how to save/load/quit... ')
        clear()
        print(f'''  SAVING YOUR GAME:
  This is how to save a game:

    1) Select "Menu"
      Action: Menu
      Do you want to:
      1) Save the game
      2) Load another game
      3) Quit game
    2) Select "1"
      1
      Give the save a name:
    3) Choose a name
      Give the save a name: A Game I Saved
      Done Saving!

  LOADING A GAME:
  This is how to load a game:

    1) Select "Menu"
      Action: Menu
      Do you want to:
      1) Save the game
      2) Load another game
      3) Quit game
    2) Select "2"
      2
      Saves:
      1) A Game I Saved
      Which save do you want to load?
    3) Choose a save
      Which save do you want to load? 1

      Play Turn 1, Choose an Action:
  QUIT TO MAIN:
  And lastly, how to quit a game:

    1) Select "Menu"
      Action: Menu
      Do you want to:
      1) Save the game
      2) Load another game
      3) Quit game
    2) Select "3"
      3
      Do you want to save first?
      (Y/N)
    3) Choose "Y" or "N"
      a.
        i: Choose "Y":
          (Y/N) y
          Give the save a name:
        ii: Type in a name:
          Give the save a name: Saving!
          Title Screen:
           ===========
      b.
        i: Choose "N":
          (Y/N) n
          Give the save a name:
        Title Screen:
         ===========
''')
        input('Press ENTER to quit to title screen... ')
        clear()

class Help(Menu):
    def __init__(self):
        super().__init__(name='Help Menu', actions=[MainMenu()])

    def show(self):
        import os
        print(f'{self.name}:\n ======= \n\n')
        tutorial = 0
        for i, _ in enumerate(TitleScreen.actions):
            if _.name == 'Play Tutorial':
                tutorial = i
        print(f'''\
This is a text-based and turn-based game. It has a Github repository here: https://github.com/TBBYT/Turn-Based-Game

You can view a tutorial by returning to the main menu, and then typing in "{tutorial+1}" and pressing enter.
''')
        input('Press ENTER to return to main menu.')
        self.actions[0].method() # Go to main menu
