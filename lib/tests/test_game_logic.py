import pytest
from lib.gameLogic import *
from lib.board import Board
from lib.constants import *
from lib.player import Player
from collections import deque
from pytest import MonkeyPatch

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

def test_chance_logic(player: Player,monkeypatch:  MonkeyPatch):
    monkeypatch.setattr('lib.gameLogic.roll', lambda: (1, 2))
    score, amount = chance_logic(player, 3000)
    assert score == (1, 2)
    assert amount == -1500
    monkeypatch.setattr('lib.gameLogic.roll', lambda: (4, 2))
    score, amount = chance_logic(player, 3000)
    assert score == (4, 2)
    assert amount == 1000

def test_six_hundred_logic(player: Player):
    six_hundred_logic(player)
    assert player.get_balance() == INITIAL_BALANCE + 600

def test_start_logic(player: Player):
    start_logic(player)
    assert player.get_balance() == INITIAL_BALANCE + (TURN_FEE * 2)

def test_every_one_fifty():
    players = [Player("player1", CAR_BLACK), Player("player2", CAR_BLUE), Player("player3", CAR_RED)]
    every_one_fifty(players)
    for player in players:
        assert player.get_balance() == INITIAL_BALANCE + 50

def test_who_owns_stock(player_with_cell: Player, player: Player):
    players = [player, player_with_cell]
    assert who_owns_stock(players, 1) == [player_with_cell]
    
def test_who_owns_stock_by_name(player_with_cell: Player, player: Player):
    players = [player, player_with_cell]
    assert who_owns_stock_by_name(players, 'gled') == [player_with_cell]

""" 
def transfer_stock(board, current_player, chosen_stock):
    if chosen_stock.owner is not None:
        chosen_stock.owner.remove_stock(chosen_stock)    
    else:
        board.remove_stock(chosen_stock)
        
    chosen_stock.owner = current_player
    current_player.add_stock(chosen_stock)
"""

def test_transfer_stock(board_witout_one_cell: Board, player_with_cell: Player, player: Player):
    stock = player_with_cell.get_stocks()[0]
    transfer_stock(board_witout_one_cell, player, player_with_cell.get_stocks()[0])
    assert len(player_with_cell.get_stocks()) == 0
    assert player.get_stocks()[0] == stock