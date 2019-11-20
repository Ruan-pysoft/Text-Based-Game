import traceback

try:
    import menus as m # Used to display menus
    import os

    game_name = "My Turn-Based Game" # The name of the game, if you can think of a better name, please change this.

    if os.name == 'nt': # If the OS is Windows
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(game_name) # Change the command line's title
    else:
        print('\33]0;' + game_name + '\a', end='', flush=True) # Change the GNU terminal's title
        # May not work on mac, IDK.

    menu = None

    def update_screen(): # everything happens in menus.py
        menu.show()

    m.TitleScreen() # Show the title screen
except Exception as e:
    print(f''' Something went wrong :(
=========================
Please report this at https://github.com/TBBYT/Turn-Based-Game/issues
Error:''')
    traceback.print_exc()
    input('Press ENTER to close window')
