import pytest
from lib.constants import *
from lib.player import Player
from lib.board import Board
from lib.gameLogic import *
from lib.stock import Stock

@pytest.fixture
def stock():
    return Stock(CELLS_DEF['ORANGE'], 1, 'gled', False)

def test_update_value(stock: Stock):
    old_penalty = stock.get_penalty()
    assert stock.update_value(100) == -100
    assert stock.get_stock_value() == 100
    assert stock.get_original_value() == 200
    assert stock.get_penalty() == [i / 2 for i in old_penalty]