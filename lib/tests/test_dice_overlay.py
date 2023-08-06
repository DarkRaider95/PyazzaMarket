from lib.game import Game
import pytest
import pygame
from lib.constants import *
from pytest import MonkeyPatch
from lib.dice_overlay import DiceOverlay

# we need to do pygame.init() in order to be able to run pygame
pygame.init()

clock = pygame.time.Clock()

@pytest.fixture
def game() -> Game:
    game = Game(WIDTH, HEIGHT, clock, [{"name":"Player1", "color": CAR_RED}, {"name":"Player2", "color": CAR_BLACK}])
    game.get_gameUI().draw_dices()
    game.get_gameUI().draw_actions_ui()
    game.get_gameUI().drawDiceOverlay(game.get_current_player().get_name() + ' tira dadi', 'Decisione turni')
    return game

@pytest.fixture
def diceOverlay(game: Game) -> DiceOverlay:
    diceOverlay = DiceOverlay(game)
    return diceOverlay

def test_roll_dice(diceOverlay: DiceOverlay, monkeypatch: MonkeyPatch, game: Game):
    monkeypatch.setattr('lib.dice_overlay.roll', lambda x,y: (1, 3))
    diceOverlay.roll_dice()
    assert diceOverlay.get_who_will_start() == 0
    assert diceOverlay.get_hihgest_score() == 4
    game.set_current_player_index(1)
    monkeypatch.setattr('lib.dice_overlay.roll', lambda x,y: (2, 3))
    diceOverlay.roll_dice()
    assert diceOverlay.get_who_will_start() == 1
    assert diceOverlay.get_hihgest_score() == 5

def test_roll_dice_double(diceOverlay: DiceOverlay, monkeypatch: MonkeyPatch, game: Game):
    monkeypatch.setattr('lib.dice_overlay.roll', lambda x,y: (2, 2))
    diceOverlay.roll_dice()
    assert diceOverlay.get_who_will_start() == 0
    assert diceOverlay.get_hihgest_score() == 4
    game.set_current_player_index(1)
    monkeypatch.setattr('lib.dice_overlay.roll', lambda x,y: (2, 2))
    diceOverlay.roll_dice()
    assert diceOverlay.get_who_will_start() == 0
    assert diceOverlay.get_hihgest_score() == 4
    assert diceOverlay.get_second_round_who_start() == [0, 1]