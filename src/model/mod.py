from __future__ import annotations

import custenums
from custenums import *
from custtypes import *
from view.constants import SCREEN_RESOLUTION
import pygame as pg
from view.constants import *

import pygame as pg

class Object:
    def __init__(self,  coordinates: Vec2, size: Vec2, is_physical: bool = False, hp: float = None):
        self._coordinates = coordinates
        self._size = size
        self._hp = hp

        self._rect = pg.rect.Rect(
            (SCREEN_RESOLUTION[0] // 2 - self._size[0] // 2, SCREEN_RESOLUTION[1] // 2 - self._size[1] // 2),
            self._size)
        self._is_visible = False
        self._is_physical = is_physical
        self._acceleration = 0, 0

    def getAcceleration(self) -> Vec2:
        return self._acceleration

    def setAcceleration(self, acceleration: Vec2):
        self._acceleration = acceleration

    def getIsPhysical(self) -> bool:
        return self._is_physical

    def setIsPhysical(self, is_physical: bool):
        self._is_physical = is_physical

    def getSize(self) -> Vec2:
        return self._size

    def setCoordinates(self, coords: Vec2):
        self._coordinates = coords

    def getCoordinates(self) -> Vec2:
        return self._coordinates

    def calculateRect(self, screen_coords: Vec2):
        self._rect = pg.rect.Rect((screen_coords[0] + self._size[0] // 2,
                                   screen_coords[1] + self._size[1] // 2),
                                  self._size)

    def getRect(self) -> pg.Rect:
        return self._rect


    def changeCoordinatesBy(self, by: Vec2):
        self._coordinates[0] += by[0]
        self._coordinates[1] += by[1]

    def changeHPBy(self, by: float):
        self._hp += by

    def getHP(self) -> float | int:
        return self._hp

    def __hash__(self):
        return id(self)

    def getIsVisible(self) -> bool:
        return self._is_visible

    def setIsVisible(self, is_visible: bool):
        self._is_visible = is_visible


class Ship(Object):
    def __init__(self, coordinates: Vec2, size: Vec2, hp: float):
        super().__init__(coordinates, size, True, hp)
        self.__max_hp = hp
        self.__current_hp = hp
    
    def getHP(self):
        return self.__current_hp
    
    def getMaxHP(self):
        return self.__max_hp
    
    def takeDamage(self, damage):
        self.__current_hp = max(0, self.__current_hp - damage)
    
    def heal(self, amount):
        self.__current_hp = min(self.__max_hp, self.__current_hp + amount)
    
    def isDead(self):
        return self.__current_hp <= 0


class Block(Object):
    def __init__(
            self,
            coords: Vec2,
            size: Vec2,
            block_type: custenums.BlockType,
    ):
        super().__init__(coords, size)

        self._block_type = block_type

    def setBlockType(self, new_type: BlockType):
        self._block_type = new_type

    def getBlockType(self) -> BlockType:
        return self._block_type

    def __str__(self) -> str:
        return f"{self._coords}, {self._block_type}"


class Model:
    def __init__(self):
        self.__state = GameState.main_menu

        self.__enemies: set[Ship] = set()
        self.__last_time_enemy_spawned = 0

    def getEnemies(self) -> set[Ship]:
        return self.__enemies

    def getLastTimeEnemySpawned(self) -> float:
        return self.__last_time_enemy_spawned

    def setLastTimeEnemySpawned(self, _time: float):
        self.__last_time_enemy_spawned = _time

    def addEnemy(self, enemy: Ship):
        self.__enemies.add(enemy)

    def getBlockMap(self) -> set[Block]:
        return self._block_map

    def setBlockMap(self, block_map: set[Block]):
        self._block_map = block_map

    def getPlayer(self) -> Ship:
        return self._player

    def setPlayer(self, player: Ship):
        self._player = player

    def getGameState(self) -> custenums.GameState.__dict__:
        return self.__state

    def setGameState(self, game_state: custenums.GameState):
        self.__state = game_state
    # ... باقي الكود الموجود ...
        self.__hearts = set()  # مجموعة القلوب
    
    def getHearts(self):
        return self.__hearts
    
    def addHeart(self, heart):
        self.__hearts.add(heart)
    
    def removeHeart(self, heart):
        if heart in self.__hearts:
            self.__hearts.remove(heart)



# في ملف model/models.py أو ملف منفصل


class Heart:
    def __init__(self, coordinates, size=(30, 30)):
        self.__coordinates = list(coordinates)
        self.__size = size
        self.__rect = None
        self.__is_collected = False

    def getCoordinates(self):
        return self.__coordinates

    def getSize(self):
        return self.__size

    def getRect(self):
        return self.__rect

    def calculateRect(self, screen_coordinates):
        self.__rect = pg.Rect(screen_coordinates[0], screen_coordinates[1],
                             self.__size[0], self.__size[1])

    def isCollected(self):
        return self.__is_collected

    def collect(self):
        self.__is_collected = True

