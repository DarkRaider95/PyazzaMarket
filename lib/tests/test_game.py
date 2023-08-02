from lib.game import Game
import pytest
import pygame
import pygame_gui
from lib.constants import *
from pytest import MonkeyPatch

pygame.init()

clock = pygame.time.Clock()

class FakeEvent:
    def __init__(self, event_type, ui_element):
        self.type = event_type
        self.ui_element = ui_element

@pytest.fixture
def game() -> Game:
    players = [{"name":"Player1", "color": CAR_RED}, {"name":"Player2", "color": CAR_BLACK}]
    game = Game(WIDTH, HEIGHT, clock, players)
    game.gameUI.drawDices()
    game.gameUI.draw_actions_ui()
    game.gameUI.draw_leaderboard(game.get_players(), 2000, game.get_players()[game.currentPlayer])
    game.gameUI.draw_stockboard(game.get_players())

    return game

def test_quit(game: Game):
    fakeEvent = FakeEvent(pygame.QUIT, None)
    game.manage_events(fakeEvent)
    assert game.running == False


def test_launch_dice(game: Game, monkeypatch: MonkeyPatch):    
    fakeEvent = FakeEvent(pygame_gui.UI_BUTTON_PRESSED, game.gameUI.launchDice)
    player = game.get_players()[0]
    #when python does an import of the methods in a different file it does copy and paste of the methods
    #so when we mock a method that it is in a different file from the one that we are testing we need to mock the method
    #as if it is inside the file that we are testing
    #in this case we have roll that it is inside gameLogic.py, we need to mock it but it is called inside game.py
    #so we need to mock lib.game.roll and not lib.gameLogic.roll
    #because game.py has a copy of roll inside
    monkeypatch.setattr('lib.game.roll', lambda: (1, 5))

    game.manage_events(fakeEvent)     

    assert player.get_position() == 6
    assert game.gameUI.launchDice.is_enabled == False
    assert game.gameUI.passButton.is_enabled == True
    assert game.gameUI.buyButton.is_enabled == True
    assert game.gameUI.showStocks.is_enabled == False

def test_launch_dice_double(game: Game, monkeypatch: MonkeyPatch):    
    fakeEvent = FakeEvent(pygame_gui.UI_BUTTON_PRESSED, game.gameUI.launchDice)
    player = game.get_players()[0]

    monkeypatch.setattr('lib.game.roll', lambda: (1, 1))

    game.manage_events(fakeEvent)     

    assert player.get_position() == 2
    assert game.gameUI.launchDice.is_enabled == False
    assert game.gameUI.passButton.is_enabled == False
    assert game.gameUI.buyButton.is_enabled == True
    assert game.gameUI.showStocks.is_enabled == False

#def test_launch_dice_and_pass_turn(game: Game, monkeypatch: MonkeyPatch):
#    monkeypatch.setattr('lib.gameLogic.roll', lambda: (1, 2))
#    fakeEvent = FakeEvent(pygame_gui.UI_BUTTON_PRESSED, game.gameUI.launchDice)
#    player = game.get_players()[0]
#    game.manage_events(fakeEvent)
#    player2 = game.get_players()[game.currentPlayer]
#
#    assert player.get_position() == 3
#    assert player2.get_name() == 'Player2'
#if event.type == pygame.QUIT:
#            self.running = False
#
#        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
#            if event.ui_element == self.gameUI.launchDice:                        
#                self.turn()
#            elif event.ui_element == self.gameUI.buyButton:
#                curr_player = self.__players[self.currentPlayer]
#                buy_stock(self.board.get_cells(), curr_player)
#                self.gameUI.updateAllPlayerLables(self.getPlayers())
#                self.gameUI.buyButton.disable()
#                self.gameUI.enableShowStockButton(self.__players[self.currentPlayer])
#            elif event.ui_element == self.gameUI.passButton:
#                self.currentPlayer = (self.currentPlayer + 1) % len(self.getPlayers())
#                self.set_skip_turn()
#                self.gameUI.updateTurnLabel(self.__players[self.currentPlayer])
#                self.gameUI.launchDice.enable()
#                self.gameUI.passButton.disable()
#                self.gameUI.buyButton.disable()
#                self.gameUI.enableShowStockButton(self.__players[self.currentPlayer])
#            elif event.ui_element == self.gameUI.showStocks:
#                curr_player = self.__players[self.currentPlayer]
#                self.gameUI.disableActions()
#                self.gameUI.showStocksUi(curr_player.get_stocks(), 'Le cedole di '+curr_player.get_name())
#            elif event.ui_element == self.gameUI.nextStock:
#                curr_player = self.__players[self.currentPlayer]
#                self.gameUI.showNextStock()
#            elif event.ui_element == self.gameUI.previousStock:
#                curr_player = self.__players[self.currentPlayer]
#                self.gameUI.showPreviousStock()
#            elif event.ui_element == self.gameUI.closeStock:                        
#                self.gameUI.closeStockUi()
#                self.screen.fill(BLACK)
#                self.gameUI.drawDices()
#                self.gameUI.renableActions()
#            elif event.ui_element == self.gameUI.chooseBut:
#                curr_player = self.__players[self.currentPlayer]
#                chosen_stock = self.gameUI.getShowedStock()
#                curr_player.add_stock(chosen_stock)
#                curr_player.change_balance(-chosen_stock.get_stock_value())
#                self.board.remove_stock(chosen_stock)
#                self.gameUI.closeStockUi()
#                self.screen.fill(BLACK)
#                self.gameUI.drawDices()
#                self.gameUI.updateAllPlayerLables(self.getPlayers())
#                self.gameUI.renableActions()
#            elif event.ui_element == self.gameUI.chooseMoveBut:
#                curr_player = self.__players[self.currentPlayer]
#                chosen_stock = self.gameUI.getShowedStock()
#                curr_cell = self.board.get_cell(chosen_stock.get_position())
#                curr_player.set_position(chosen_stock.get_position())
#                self.enableBuyButton(curr_cell, curr_player)
#                self.gameUI.closeStockUi()
#                self.screen.fill(BLACK)
#                self.gameUI.drawDices()
#                self.gameUI.passButton.enable()
#                self.gameUI.showStocks.enable()
#            elif event.ui_element == self.gameUI.eventBut:
#                curr_player = self.__players[self.currentPlayer]
#                self.eventsLogic(curr_player)
#                self.gameUI.closeEventUi()
#                self.screen.fill(BLACK)
#                self.gameUI.drawDices()
#                self.gameUI.updateAllPlayerLables(self.getPlayers())
#                self.gameUI.renableActions()
#            elif event.ui_element == self.gameUI.buyAnyBut:
#                chosen_stock = self.gameUI.getShowedStock()
#                curr_player = self.__players[self.currentPlayer]
#                transfer_stock(self.board, curr_player, chosen_stock)
#                self.gameUI.updateAllPlayerLables(self.getPlayers())
#                self.gameUI.renableActions()
#            elif event.ui_element == self.gameUI.closeAlertBut:
#                self.gameUI.closeAlert(self.getPlayers(), self.gameUI)
#            elif event.ui_element == self.gameUI.closeDiceOverlayBut:
#                if self.establish_players_order:
#                    self.gameUI.closeDiceOverlay(self.getPlayers(), self.gameUI)
#                    self.currentPlayer =  (self.currentPlayer+1) % len(self.getPlayers())
#                    self.gameUI.drawDiceOverlay(self.__players[self.currentPlayer].get_name() + ' tira dadi', 'Decisione turni')
#                elif self.firstPlayerStarted:
#                    # this will be fired only after all the players have throw the dices
#                    self.gameUI.closeDiceOverlay(self.getPlayers(), self.gameUI)
#                    self.currentPlayer = self.firstPlayerIndex
#                    self.gameUI.updateTurnLabel(self.__players[self.currentPlayer])
#                    self.firstPlayerStarted = False
#                else:
#                    self.gameUI.closeDiceOverlay(self.getPlayers(), self.gameUI)
#            elif event.ui_element == self.gameUI.launchOverlayDiceBut:
#                # when you throw the dices maybe you are deciding the order of the players
#                # or you are in a chance cell
#                if self.establish_players_order:
#                    score = roll()
#                    self.gameUI.updateDiceOverlay(score)
#                    diceSum = score[0] + score[1]
#                    if self.highestScore < diceSum:
#                        self.firstPlayerIndex = self.currentPlayer
#                        self.highestScore = diceSum
#                    if self.currentPlayer == len(self.getPlayers()) - 1:
#                        self.establish_players_order = False
#                else:
#                    # amount is the amount of money that the player has to pay or receive
#                    score, amount = chance_logic(player, self.__squareBalance)
#                    self.gameUI.updateDiceOverlay(score)
#                    if self.__squareBalance + amount < 0:
#                        self.__squareBalance == 0
#                    else:
#                        self.__squareBalance += amount
#                    self.gameUI.updateDice(score)
#                    self.gameUI.updateSquareBalanceLabel(self.__squareBalance)
#            else:
#                print("Evento non gestito")