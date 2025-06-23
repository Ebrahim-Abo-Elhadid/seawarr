import time
from typing import Callable

import pygame as pg

from custtypes import *
from view.constants import *

pg.font.init()


class Button:
    CLICK_INTERVAL = 0.1
    def __init__(self, position: Vec2, size: Vec2 = None, text: str = "Plain text"):
        # if size is None, then calculate size depending on text size
        self.__text = text
        self.__font = pg.font.SysFont("Comic Sans MS", 20)
        self.__text_box = self.__font.render(self.__text, True, Colors.black)

        if size is None:
            self.__size = self.__text_box.get_size()
        else:
            self.__size = size

        self.__position = position[0] - self.__size[0] // 2, position[1] - self.__size[1] // 2
        self.__text = text

        self.__top_left_point = self.__position[0], self.__position[1]
        self.__bottom_right_point = self.__position[0] + self.__size[0], self.__position[1] + self.__size[1]

        self.__rect = pg.Rect((self.__top_left_point[0], self.__top_left_point[1]), (self.__size[0], self.__size[1]))

        self.__action: Callable

    def isMouseInBoundaries(self, mouse_pos: Vec2) -> bool:
        if self.__top_left_point[0] <= mouse_pos[0] <= self.__bottom_right_point[0] and \
                self.__top_left_point[1] <= mouse_pos[1] <= self.__bottom_right_point[1]:
            return True
        return False

    def setActionOnClick(self, action: Callable):
        if not callable(action):
            raise Exception(f"action should be FunctionType type. Actual type is {type(action)}")
        self.__action = action

    def onClick(self):
        try:
            self.__action()
        except AttributeError as ex:
            raise Exception(f"Action wasn't set before the actual call. {ex}")
        except Exception as ex:
            raise ex


    def update(self, screen: pg.display, mouse_state: MouseState):
        pg.draw.rect(screen, Colors.white, self.__rect)
        screen.blit(self.__text_box, self.__position)

        if mouse_state.is_clicked_left and \
                self.isMouseInBoundaries(mouse_state.position) and \
                mouse_state.last_left_click_time + self.CLICK_INTERVAL <= time.monotonic():
            mouse_state.last_left_click_time = time.monotonic()
            self.onClick()


