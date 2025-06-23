import pygame as pg

import view.ui_arra
from custenums import BlockType
from custenums import GameState
from custtypes import *
from model.mod import Model
from presenter.main import Presenter
from view.constants import *

pg.init()

class View:
    def __init__(self, screen: pg.display, presenter: Presenter, buttons: view.ui_arra):
        self._screen = screen
        self._presenter = presenter
        self._buttons = buttons

    def _buttonsUpdate(self, mouse_state: MouseState):
        for btn in self._buttons:
            btn.value.update(self._screen, mouse_state)

class MainMenuView(View):
    def __init__(self, screen: pg.display, presenter: Presenter):
        super().__init__(screen, presenter, view.ui_arra.MainMenu)

        self._buttons.start_btn.value.setActionOnClick(self._presenter.startGameplay)
        # self._buttons.saves_btn.value.setActionOnClick(self._presenter.openSavesMenu)
        self._buttons.exit_btn.value.setActionOnClick(exit)

    def update(self, mouse_state: MouseState):
        self._screen.fill(Colors.water_shadowed)

        super()._buttonsUpdate(mouse_state)

class GameplayView(View):
    def __init__(self, screen: pg.display, presenter: Presenter):
        super().__init__(screen, presenter, view.ui_arra.GameplayGUI)
    def __drawHearts(self):
        for heart in self._presenter.getHearts():
            if not heart.isCollected():
                pg.draw.rect(self._screen, (255, 0, 0), heart.getRect())  # مستطيل أحمر كمثال

            self._buttons.pause.value.setActionOnClick(self._presenter.togglePause)

    def __drawEnemies(self):
        for enemy in self._presenter.getEnemies():
            if enemy.getIsVisible():
                pg.draw.rect(self._screen, Colors.enemy_ship, enemy.getRect())
    def __drawPlayerHealthBar(self):
        player = self._presenter.getPlayer()
        max_hp = player.getMaxHP()
        current_hp = player.getHP()
        bar_width = 100
        bar_height = 10
        x = 10
        y = 10
        # خلفية الشريط
        pg.draw.rect(self._screen, (128, 128, 128), (x, y, bar_width, bar_height))
        # الشريط نفسه
        hp_width = int(bar_width * (current_hp / max_hp))
        pg.draw.rect(self._screen, (0, 255, 0), (x, y, hp_width, bar_height))

    def __drawPlayer(self):
        pg.draw.rect(self._screen, Colors.ship, self._presenter.getPlayer().getRect())

    def __drawWorld(self):
        for coords, block in self._presenter.getVisibleBlockMap().items():
            match block.getBlockType():
                case BlockType.island:
                    color = Colors.island
                case BlockType.water:
                    color = Colors.water
                    continue
                case other:
                    raise Exception(f"Not defined color for BlockType: {other}")

            pg.draw.rect(self._screen, color, block.getRect())

    def update(self, mouse_state: MouseState):
        self.__drawHearts()
        self.__drawPlayerHealthBar()
        self._screen.fill(Colors.water)

        self._presenter.tickGameplay()

        self.__drawWorld()
        self.__drawPlayer()
        self.__drawEnemies()

        super()._buttonsUpdate(mouse_state)


class SavesMenuView(View):
    def __init__(self, screen: pg.display, presenter: Presenter):
        super().__init__(screen, presenter, view.ui_arra.SavesMenu)

        self._buttons.main_menu.value.setActionOnClick(presenter.openMainMenu)
        # self._buttons.load_save.value.setActionOnClick(self.__presenter.)

    def update(self, mouse_state: MouseState):
        self._screen.fill(Colors.water_shadowed)

        super()._buttonsUpdate(mouse_state)


class PauseMenuView(View):
    def __init__(self, screen: pg.display, presenter: Presenter):
        super().__init__(screen, presenter, view.ui_arra.PauseMenu)

        self._buttons.unpause.value.setActionOnClick(self._presenter.togglePause)
        self._buttons.main_menu.value.setActionOnClick(self._presenter.openMainMenu)

    def update(self, mouse_state: MouseState):
        self._screen.fill(Colors.water_shadowed)

        super()._buttonsUpdate(mouse_state)


class GeneralView:
    def __init__(self, presenter: Presenter, model: Model, screen_resolution: Vec2):
        self.__presenter = presenter
        self.__model = model

        self.__mouse_state = MouseState(False, False, (0, 0), 0.0)
        self.__screen = pg.display.set_mode(screen_resolution, vsync=True)
        self.__clock = pg.time.Clock()

        self.__main_menu_view = MainMenuView(self.__screen, presenter)
        self.__gameplay_view = GameplayView(self.__screen, presenter)
        # self.__saves_menu_view = SavesMenuView(self.__screen, presenter)
        self.__pause_menu_view = PauseMenuView(self.__screen, presenter)

    def showFPS(self):
        if hasattr(self.__model, "_player"):
            message = f"FPS: {round(self.__clock.get_fps())} PLAYER_COORDS: {self.__model.getPlayer().getCoordinates()}"
        else:
            message = f"FPS: {round(self.__clock.get_fps())}"
        pg.display.set_caption(message)

    def updateMouseState(self):
        mouse_pressed = pg.mouse.get_pressed()
        self.__mouse_state.is_clicked_left = mouse_pressed[0]
        self.__mouse_state.is_clicked_right = mouse_pressed[2]
        self.__mouse_state.position = pg.mouse.get_pos()

    def update(self):
        self.updateMouseState()

        match self.__model.getGameState():
            case GameState.main_menu:
                self.__main_menu_view.update(self.__mouse_state)
            case GameState.saves_menu:
                self.__saves_menu_view.update(self.__mouse_state)
            case GameState.pause:
                self.__pause_menu_view.update(self.__mouse_state)
            case GameState.gameplay:
                self.__gameplay_view.update(self.__mouse_state)

        pg.display.flip()
        self.__clock.tick(FPS_CAP)
        self.showFPS()
