from enum import Enum

class GameState(Enum):
    main_menu = 1
    saves_menu = 2
    gameplay = 3
    death_screen = 4
    pause = 5

class BlockType(Enum):
    water = 0
    island = 1


    