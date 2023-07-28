import pytest
from lib.gameLogic import *
from lib.board import Board
from lib.constants import *
from lib.player import Player

""" 
def check_for_penalty(cells, players, player_number): # testare per vedere se riconosce quando le celle sono uguali
    current_player = players[player_number]
    cell = cells[current_player.position]
    players.pop(player_number) # we drop the current player in order to not check him self in the for loops
    own_by_the_player = False # then we check if the player own the stock
    for stock in current_player.getStocks():
        if cell.position == stock.position:
            own_by_the_player = True
    if not own_by_the_player: # if it is not owned by the player we check if it is owned by another player
        for player in players:
            for stock in player.getStocks():
                if cell.position == stock.position:
                    penality = player.computePenalty(stock)
                    current_player.change_balance(-penality)
                    player.change_balance(penality)
                    break # we break in order to pay only once the fee if the player have more than one card in the same cell 
"""

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
    stock_value = cells[1].getStocks()[0].getStockValue()
    assert players[1].getBalance() == INITIAL_BALANCE - CELLS_DEF["ORANGE"]["penalty"][0]
    assert players[0].getBalance() == INITIAL_BALANCE + CELLS_DEF["ORANGE"]["penalty"][0] - stock_value
    # test when the player own the stock
    buy_stock(cells, players[1])
    cells = board.get_cells()
    check_for_penalty(cells, players, 1)
    assert players[1].getBalance() == INITIAL_BALANCE - CELLS_DEF["ORANGE"]["penalty"][0] - stock_value
    assert players[0].getBalance() == INITIAL_BALANCE + CELLS_DEF["ORANGE"]["penalty"][0] - stock_value

def test_check_for_penalty_owning_both_stokcs_in_the_cell():
    # creating board and players
    board = Board(enableGraphics = False)
    cells = board.get_cells()
    players = [Player("player1", CAR_BLACK), Player("player2", CAR_BLUE), Player("player3", CAR_RED)]
    # saving the price of the stock
    stock_value = cells[1].getStocks()[0].getStockValue()
    # first player buy the first stock twice
    players[0].move(1)
    buy_stock(cells, players[0])
    cells = board.get_cells()
    buy_stock(cells, players[0])
    # moving the player to the first cell
    players[1].move(1)
    cells = board.get_cells()
    check_for_penalty(cells, players, 1)
    assert players[1].getBalance() == INITIAL_BALANCE - CELLS_DEF["ORANGE"]["penalty"][1]
    assert players[0].getBalance() == INITIAL_BALANCE + CELLS_DEF["ORANGE"]["penalty"][1] - (stock_value * 2) 