from enum import Enum

from view.ui_elem import *


class MainMenu(Enum):
    start_btn = Button((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2 - 40), text="START")
    # saves_btn = Button((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2), text="SAVES")
    exit_btn = Button((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2 + 40), text="QUIT")

class GameplayGUI(Enum):
    pause = Button((BTN_SIZE[0] // 2, BTN_SIZE[1] // 2), text="PAUSE")

class SavesMenu(Enum):
    # load_save = Button((SCREEN_RESOLUTION[0] // 2 - 100, SCREEN_RESOLUTION[1] // 2 + 40), text="LOAD")
    main_menu = Button((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2 + 40), text="MAIN MENU")
    # save_save = Button((SCREEN_RESOLUTION[0] // 2 + 100, SCREEN_RESOLUTION[1] // 2 + 40), text="SAVE")

class PauseMenu(Enum):
    unpause = Button((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2), text="UNPAUSE")
    # load_save = Button((SCREEN_RESOLUTION[0] // 2 - 100, SCREEN_RESOLUTION[1] // 2 + 40), text="LOAD")
    main_menu = Button((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2 + 40), text="MAIN MENU")
    # save_save = Button((SCREEN_RESOLUTION[0] // 2 + 100, SCREEN_RESOLUTION[1] // 2 + 40), text="SAVE")

