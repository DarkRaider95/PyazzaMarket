import pytest
from lib.gameLogic import *
from lib.board import Board
from lib.constants import *
from lib.player import Player
from collections import deque

def test_roll():
    for _ in range(10):
        dice = roll()
        assert len(dice) == 2
        assert 1 <= dice[0] <= 6
        assert 1 <= dice[1] <= 6

def test_is_double():
    assert is_double((1, 1)) is True
    assert is_double((2, 2)) is True
    assert is_double((3, 4)) is False
    assert is_double((6, 6)) is True
    assert is_double((5, 6)) is False

@pytest.fixture
def player() -> Player:
    player = Player("test", CAR_RED)
    player.move(1)
    return player

@pytest.fixture
def board() -> Board:
    return Board(enableGraphics = False)

@pytest.fixture
def player_with_cell(board: Board) -> Player:
    player = Player("test", CAR_RED)
    player.move(1)
    cells = board.get_cells()
    buy_stock(cells, player)
    return player

@pytest.fixture
def board_witout_one_cell(player: Player) -> Board:
    board = Board(enableGraphics = False)
    player.move(1)
    cells = board.get_cells()
    buy_stock(cells, player)
    return board

def test_buy_stock(player: Player, board: Board):
    cells = board.get_cells()
    buy_stock(cells, player)
    assert len(player.get_stocks()) == 1
    assert player.get_stocks()[0].name == 'gled'
    assert len(cells[1].get_stocks()) == 1

    cells = board.get_cells()
    buy_stock(cells, player)
    assert (len(player.get_stocks()) == 2)
    assert player.get_stocks()[1].name == 'gled'
    assert len(cells[1].get_stocks()) == 0

def test_check_if_can_buy_stock(player: Player, board: Board):
    cells = board.get_cells()
    assert check_if_can_buy_stock(cells[1], player) is True
    assert check_if_can_buy_stock(cells[0], player) is False
    cells[1].sellStock()
    cells[1].sellStock()
    assert check_if_can_buy_stock(cells[1], player) is False
    player.change_balance(-3000)
    assert check_if_can_buy_stock(cells[2], player) is False

def test_check_for_penalty():
    # creating board and players
    board = Board(enableGraphics = False)
    cells = board.get_cells()
    players = [Player("player1", CAR_BLACK), Player("player2", CAR_BLUE), Player("player3", CAR_RED)]
    # first player buy a stock
    players[0].move(1)
    buy_stock(cells, players[0])
    # moving the player to the first cell
    players[1].move(1)
    cells = board.get_cells()
    check_for_penalty(cells, players, 1)
    # saving the price of the stock
    stock_value = cells[1].get_stocks()[0].get_stock_value()
    assert players[1].get_balance() == INITIAL_BALANCE - CELLS_DEF["ORANGE"]["penalty"][0]
    assert players[0].get_balance() == INITIAL_BALANCE + CELLS_DEF["ORANGE"]["penalty"][0] - stock_value
    # test when the player own the stock
    buy_stock(cells, players[1])
    cells = board.get_cells()
    check_for_penalty(cells, players, 1)
    assert players[1].get_balance() == INITIAL_BALANCE - CELLS_DEF["ORANGE"]["penalty"][0] - stock_value
    assert players[0].get_balance() == INITIAL_BALANCE + CELLS_DEF["ORANGE"]["penalty"][0] - stock_value

def test_check_for_penalty_owning_both_stokcs_in_the_cell():
    # creating board and players
    board = Board(enableGraphics = False)
    cells = board.get_cells()
    players = [Player("player1", CAR_BLACK), Player("player2", CAR_BLUE), Player("player3", CAR_RED)]
    # saving the price of the stock
    stock_value = cells[1].get_stocks()[0].get_stock_value()
    # first player buy the first stock twice
    players[0].move(1)
    buy_stock(cells, players[0])
    cells = board.get_cells()
    buy_stock(cells, players[0])
    # moving the player to the first cell
    players[1].move(1)
    cells = board.get_cells()
    check_for_penalty(cells, players, 1)
    assert players[1].get_balance() == INITIAL_BALANCE - CELLS_DEF["ORANGE"]["penalty"][1]
    assert players[0].get_balance() == INITIAL_BALANCE + CELLS_DEF["ORANGE"]["penalty"][1] - (stock_value * 2) 

def test_check_crash():
    players = [Player("player1", CAR_BLACK), Player("player2", CAR_BLUE), Player("player3", CAR_RED)]
    players[0].set_position(1)
    players[1].set_position(1)
    assert check_crash(players, 1) == 1
    assert players[0].get_balance() == INITIAL_BALANCE + CRASH_FEE
    assert players[1].get_balance() == INITIAL_BALANCE - CRASH_FEE
    players[0].set_position(2)
    assert check_crash(players, 0) == 0

def test_check_turn(player: Player):
    # we have 40 cells on the board, so we move until he do a complete turn
    player.move(8)
    check_turn(player)
    assert player.get_balance() == INITIAL_BALANCE
    player.move(8)
    check_turn(player)
    assert player.get_balance() == INITIAL_BALANCE
    player.move(8)
    check_turn(player)
    assert player.get_balance() == INITIAL_BALANCE
    player.move(8)
    check_turn(player)
    assert player.get_balance() == INITIAL_BALANCE
    player.move(8)
    check_turn(player)
    assert player.get_balance() == INITIAL_BALANCE + TURN_FEE

def test_stock_prize_logic(player_with_cell: Player):
    balance_before = player_with_cell.get_balance()
    stock_prize_logic(player_with_cell)
    assert player_with_cell.get_balance() == balance_before + 100

""" 
def quotation_logic(players, board, quotation, game):
    new_quotation = quotation[0]
    for player in players:
        for stock in player.get_stocks():
            difference = stock.updateValue(new_quotation[stock.get_index()])
            player.change_balance(difference)
            game.set_square_balance(difference)
    for cell in board.get_cells():
        if cell.get_stocks() is not None:                                                                          
            cell.updateCellValue(new_quotation[cell.get_index()])
            for stock in cell.get_stocks():
                _ = stock.updateValue(new_quotation[stock.get_index()])

    quotation.rotate(-1)
 """
class fakeGame:
    def __init__(self):
        self.square_balance = 0
    def set_square_balance(self, balance):
        self.square_balance = balance

def test_quotation_logic(board_witout_one_cell: Board, player_with_cell: Player):
    players = [player_with_cell, Player("player2", CAR_BLUE), Player("player3", CAR_RED)]
    quotation = deque(QUOTATION)
    new_quotation = quotation[0]
    # first test all the stocks are in the board
    quotation_logic(players, board_witout_one_cell, quotation, fakeGame())
    # check if all the cells have the correct value
    for cell in board_witout_one_cell.get_cells():
        # check only for stock cells
        if cell.get_stocks() is not None:
            for stock in cell.get_stocks():
                assert stock.get_stock_value() == new_quotation[stock.get_index()]
    stocks_owned = player_with_cell.get_stocks()
    for stock in stocks_owned:
        assert stock.get_stock_value() == new_quotation[stock.get_index()]

"""     
    for i in range(40):
        cells = board.get_cells()
        buy_stock
 """