from lib.game import Game
import pytest
import pygame
import pygame_gui
from lib.constants import *
from pytest import MonkeyPatch
from lib.board import Board

# we need to do pygame.init() in order to be able to run pygame
pygame.init()

clock = pygame.time.Clock()

class FakeEvent:
    def __init__(self, event_type, ui_element):
        self.type = event_type
        self.ui_element = ui_element

# check if we can remove drawdices, drawleaderboard and drawstockboard
@pytest.fixture
def game() -> Game:
    players = [{"name":"Player1", "color": CAR_RED, "bot": False}, {"name":"Player2", "color": CAR_BLACK, "bot": False}]
    game = Game(WIDTH, HEIGHT, clock, players)
    game.get_gameUI().draw_dices()
    game.get_gameUI().draw_actions_ui()
    game.get_gameUI().draw_leaderboard(game.get_players(), 2000, game.get_players()[game.get_current_player_index()])
    game.get_gameUI().draw_stockboard(game.get_players())

    return game

@pytest.fixture
def game_after_launch_dice(monkeypatch: MonkeyPatch) -> Game:
    players = [{"name":"Player1", "color": CAR_RED, "bot": False}, {"name":"Player2", "color": CAR_BLACK, "bot": False}]
    game = Game(WIDTH, HEIGHT, clock, players)
    game.get_gameUI().draw_dices()
    game.get_gameUI().draw_actions_ui()
    game.get_gameUI().draw_leaderboard(game.get_players(), 2000, game.get_players()[game.get_current_player_index()])
    game.get_gameUI().draw_stockboard(game.get_players())

    monkeypatch.setattr('lib.game.roll', lambda x,y: (1, 3))

    game.manage_events(FakeEvent(pygame_gui.UI_BUTTON_PRESSED, game.get_gameUI().launchDice))

    return game

def test_quit(game: Game):
    fakeEvent = FakeEvent(pygame.QUIT, None)
    game.manage_events(fakeEvent)
    assert game.running == False


def test_launch_dice(game: Game, monkeypatch: MonkeyPatch):
    #when python does an import of the methods in a different file it does copy and paste of the methods
    #so when we mock a method that it is in a different file from the one that we are testing we need to mock the method
    #as if it is inside the file that we are testing
    #in this case we have roll that it is inside gameLogic.py, we need to mock it but it is called inside game.py
    #so we need to mock lib.game.roll and not lib.gameLogic.roll
    #because game.py has a copy of roll inside
    fakeEvent = FakeEvent(pygame_gui.UI_BUTTON_PRESSED, game.get_gameUI().launchDice)
    player = game.get_players()[0]

    monkeypatch.setattr('lib.game.roll', lambda x,y: (1, 5))

    game.manage_events(fakeEvent)     

    assert player.get_position() == 6
    assert game.get_actions_status().get_throw_dices() == False
    assert game.get_actions_status().get_pass_turn() == True
    assert game.get_actions_status().get_buy_property() == True
    assert game.get_actions_status().get_show_stock() == False

# later we will need to test turn
def test_launch_dice_double(game: Game, monkeypatch: MonkeyPatch):    
    fakeEvent = FakeEvent(pygame_gui.UI_BUTTON_PRESSED, game.get_gameUI().launchDice)
    player = game.get_players()[0]

    monkeypatch.setattr('lib.game.roll', lambda x,y: (1, 1))

    game.manage_events(fakeEvent)

    fakeEventCloseAlert = FakeEvent(pygame_gui.UI_BUTTON_PRESSED, game.get_gameUI().closeAlertBut)
    game.manage_events(fakeEventCloseAlert)

    assert player.get_position() == 2
    assert game.get_actions_status().get_throw_dices() == True
    assert game.get_actions_status().get_pass_turn() == False
    assert game.get_actions_status().get_buy_property() == True
    assert game.get_actions_status().get_show_stock() == False

def test_buy_button(game_after_launch_dice: Game):
    fakeEvent = FakeEvent(pygame_gui.UI_BUTTON_PRESSED, game_after_launch_dice.get_gameUI().buyButton)

    game_after_launch_dice.manage_events(fakeEvent)     

    assert game_after_launch_dice.get_actions_status().get_throw_dices() == False
    assert game_after_launch_dice.get_actions_status().get_pass_turn() == True
    assert game_after_launch_dice.get_actions_status().get_buy_property() == False
    assert game_after_launch_dice.get_actions_status().get_show_stock() == True

def test_pass_button(game_after_launch_dice: Game):
    fakeEvent = FakeEvent(pygame_gui.UI_BUTTON_PRESSED, game_after_launch_dice.get_gameUI().passButton)

    game_after_launch_dice.manage_events(fakeEvent)     

    assert game_after_launch_dice.get_actions_status().get_throw_dices() == True
    assert game_after_launch_dice.get_actions_status().get_pass_turn() == False
    assert game_after_launch_dice.get_actions_status().get_buy_property() == False
    assert game_after_launch_dice.get_actions_status().get_show_stock() == False
    assert game_after_launch_dice.get_current_player_index() == 1