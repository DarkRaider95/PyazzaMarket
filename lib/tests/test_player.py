import pytest
from lib.constants import *
from lib.player import Player
from lib.board import Board
from lib.gameLogic import *
from lib.stock import Stock

@pytest.fixture
def board() -> Board:
    return Board(enableGraphics = False)

@pytest.fixture
def player() -> Player:
    return Player('test', CAR_RED, False)

@pytest.fixture
def player_with_same_stocks() -> Player:
    player = Player('test', CAR_RED, False)
    player.move(1)
    board = Board(enableGraphics = False)
    cells = board.get_cells()
    buy_stock(cells, player)
    cells = board.get_cells()
    buy_stock(cells, player)
    return player

@pytest.fixture
def player_with_different_stocks() -> Player:
    player = Player('test', CAR_RED, False)
    player.move(1)
    board = Board(enableGraphics = False)
    cells = board.get_cells()
    buy_stock(cells, player)
    player.move(1)
    cells = board.get_cells()
    buy_stock(cells, player)
    return player

@pytest.fixture
def stock_gled() -> Stock:
    board = Board(enableGraphics = False)
    cells = board.get_cells()
    stock = cells[1].get_stocks()[0]
    return stock

@pytest.fixture
def stock_friskies() -> Stock:
    board = Board(enableGraphics = False)
    cells = board.get_cells()
    stock = cells[2].get_stocks()[0]
    return stock

def test_move(player: Player):
    player.move(5)
    assert player.get_old_position() == 0
    assert player.get_position() == 5

def test_move_over_40(player: Player):
    player.move(45)
    assert player.get_old_position() == 0
    assert player.get_position() == 5

def test_set_position(player: Player):
    player.set_position(10)
    assert player.get_old_position() == 0
    assert player.get_position() == 10

def test_stock_value(player_with_same_stocks: Player):
    assert player_with_same_stocks.stock_value() == 400

def test_add_stock(player: Player, stock_gled: Stock):
    player.add_stock(stock_gled)
    assert player.get_stocks() == [stock_gled]

def test_same_color_count(player_with_same_stocks: Player):
    assert player_with_same_stocks.same_color_count(ORANGE) == 2

def test_compute_penalty_one_stock(player_with_different_stocks: Player, stock_gled: Stock):
    assert player_with_different_stocks.compute_penalty(stock_gled) == 60

def test_compute_penalty_two_stocks(player_with_same_stocks: Player, stock_gled: Stock):
    assert player_with_same_stocks.compute_penalty(stock_gled) == 160

def test_compute_penalty_three_stocks(player_with_same_stocks: Player, stock_gled: Stock, stock_friskies: Stock):
    player_with_same_stocks.add_stock(stock_friskies)
    assert player_with_same_stocks.compute_penalty(stock_gled) == 160

def test_get_stock_by_pos_with_stock(player_with_same_stocks: Player):
    assert player_with_same_stocks.get_stock_by_pos(1).get_name() == 'gled'

def test_get_stock_by_pos_without_stock(player_with_same_stocks: Player):
    assert player_with_same_stocks.get_stock_by_pos(2) == None

def test_remove_stock(player_with_same_stocks: Player, stock_gled: Stock):
    player_with_same_stocks.remove_stock(stock_gled)
    player_with_same_stocks.remove_stock(stock_gled)
    assert player_with_same_stocks.get_stocks() == []
