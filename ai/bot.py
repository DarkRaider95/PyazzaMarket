import pygame_gui

class FakeEvent:
    def __init__(self, event_type, ui_element):
        self.type = event_type
        self.ui_element = ui_element

class Bot:
    def __init__(self, game) -> None:
        self.__game = game
        self.__actions_status = game.get_actions_status()
        self.__gameUI = game.get_gameUI()

    def play(self) -> None:
        if self.__actions_status.get_throw_dices():
            self.__game.manage_events(FakeEvent(pygame_gui.UI_BUTTON_PRESSED, self.__gameUI.launchDice))
        elif self.__actions_status.get_buy_property():
            self.__game.manage_events(FakeEvent(pygame_gui.UI_BUTTON_PRESSED, self.__gameUI.buyButton))
        elif self.__actions_status.get_pass_turn():
            self.__game.manage_events(FakeEvent(pygame_gui.UI_BUTTON_PRESSED, self.__gameUI.passButton))