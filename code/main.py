import menus as m # Used to display menus
import os

game_name = "My Turn-Based Game" # The name of the game, if you can think of a better name, please change this.

if os.name == 'nt': # If the OS is Windows
    import ctypes
    ctypes.windll.kernel32.SetConsoleTitleW(game_name) # Change the command line's title
else:
    print('\33]0;' + game_name + '\a', end='', flush=True) # Change the GNU terminal's title
    # May not work on mac.

menu = None

def update_screen():
    menu.show()

m.TitleScreen() # Show the title screen
