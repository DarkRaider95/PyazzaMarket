import pytest
from lib.gameLogic import *
from lib.board import Board
from lib.constants import *
from lib.player import Player

@pytest.fixture
def board() -> Board:
    return Board(enableGraphics = False)

@pytest.fixture
def player() -> Player:
    player = Player("test", CAR_RED)
    player.move(1)
    return player

def test_compute_next_coord_bot():    
    x,y = Board.compute_next_coord(0,0, 'BOT')
    assert x == -CELL_WIDTH
    assert y == 0

def test_compute_next_coord_bot():    
    x,y = Board.compute_next_coord(0,0, 'LEFT')
    assert x == 0
    assert y == -CELL_WIDTH

def test_compute_next_coord_bot():    
    x,y = Board.compute_next_coord(0,0, 'TOP')
    assert x == CELL_WIDTH
    assert y == 0

def test_compute_next_coord_bot():    
    x,y = Board.compute_next_coord(0,0, 'RIGHT')
    assert x == 0
    assert y == CELL_WIDTH        

def test_get_availble_stocks(board: Board):
    stocks = board.get_availble_stocks()
    assert len(stocks) == 24

def test_get_purchasable_stocks_1000_balance(board: Board):
    stocks = board.get_purchasable_stocks(1000)
    assert len(stocks) == 24

def test_get_purchasable_stocks_0_balance(board: Board):
    stocks = board.get_purchasable_stocks(0)
    assert len(stocks) == 0

def test_get_purchasable_stocks_200_balance(board: Board):
    stocks = board.get_purchasable_stocks(200)
    assert len(stocks) == 3

def test_get_stock_if_available(board: Board):
    stock = board.get_stock_if_available(1)
    assert stock.get_name() == 'gled'
    stock = board.get_stock_if_available(1)
    assert stock.get_name() == 'gled'
    stock = board.get_stock_if_available(1)
    assert stock is None
    stock = board.get_stock_if_available(2)
    assert stock.get_name() == 'friskies'

def test_board_init(board: Board):
    cells = board.get_cells()
    assert len(cells) == 40

    names = []
    for value in CELLS_DEF.values():
        names.extend(value['names'])

    assert len(names) == 24
    #curr_x = WIDTH - 10 - CORNER_WIDTH
    #curr_y = HEIGHT - 10 - CORNER_HEIGHT
    nameIndex = 0
    for cell in cells:
        stocks = cell.get_stocks()
        if stocks is not None:
            assert stocks[0].get_name() == names[nameIndex]
            nameIndex += 1