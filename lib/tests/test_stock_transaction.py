import pytest
from lib.gameLogic import *
from lib.board import Board
from lib.constants import *
from lib.player import Player

@pytest.fixture
def player() -> Player:
    player = Player("test", CAR_RED)
    player.setPosition(1)
    return player

def test_buy_stock(player: Player):
    board = Board(enableGraphics = False)
    cells = board.get_cells()
    buy_stock(cells, player)
    assert len(player.getStocks()) == 1
    assert player.getStocks()[0].name == 'gled'
    assert len(cells[1].getStocks()) == 1

    cells = board.get_cells()
    buy_stock(cells, player)
    assert (len(player.getStocks()) == 2)
    assert player.getStocks()[1].name == 'gled'
    assert len(cells[1].getStocks()) == 0

def test_check_if_can_buy_stock(player: Player):
    board = Board(enableGraphics = False)
    cells = board.get_cells()
    assert check_if_can_buy_stock(cells[1], player) is True
    assert check_if_can_buy_stock(cells[0], player) is False
    cells[1].sellStock()
    cells[1].sellStock()
    assert check_if_can_buy_stock(cells[1], player) is False
    player.change_balance(-3000)
    assert check_if_can_buy_stock(cells[1], player) is False