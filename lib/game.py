import pygame
from .constants import FPS, WIDTH, HEIGHT, CHOOSE_STOCK_TYPE, FREE_STOP_TYPE, CHANCE_TYPE
from .board import Board
from .player import Player
from .gameUI import GameUI
from .dice import Dice
from .gameLogic import *
import pygame_gui
import time

class Game:
    def __init__(self, width, height, clock, players):
        self.clock = clock
        self.width = width
        self.height = height
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('PyazzaMarket')
        self.board = Board()
        self.dice = Dice()
        self.gameUI = GameUI(self.screen, self.clock)
        self.players = []
        self.squareBalance = 2000

        Player.last_stock_update = time.time()
        for player in players:
            self.players.append(Player(player["name"], player["color"]))

        self.currentPlayer = 0 # Magari al posto dell'indice possiamo salvare direttamente il giocatare, così evitiamo di cercarlo all'interno dell'array di giocatori

    def start(self):
        self.board.initialiaze_cells()
        self.board.draw(self.screen)
        self.dice.drawDices(self.screen)
        self.gameUI.draw_actions_ui()
        self.gameUI.draw_leaderboard(self.players, self.squareBalance)
        self.gameUI.draw_stockboard(self.players)

        for index, player in enumerate(self.players):
            self.board.drawPlayerCar(self.screen, player, index, len(self.players))

        while self.running:
            self.clock.tick(FPS)            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.gameUI.launchDice:                        
                        self.turn()
                    elif event.ui_element == self.gameUI.buyButton:
                        curr_player = self.players[self.currentPlayer]
                        #questo non so serve salvarlselo
                        #self.cells = buyStock(self.board.cells, curr_player)
                        buyStock(self.board.cells, curr_player)
                        self.gameUI.updateLabel(curr_player)
                        self.gameUI.buyButton.disable()
                        self.gameUI.enableShowStockButton(self.players[self.currentPlayer])
                    elif event.ui_element == self.gameUI.passButton:
                        self.currentPlayer = (self.currentPlayer + 1) % len(self.players)
                        self.gameUI.launchDice.enable()
                        self.gameUI.passButton.disable()
                        self.gameUI.enableShowStockButton(self.players[self.currentPlayer])
                    elif event.ui_element == self.gameUI.showStocks:
                        curr_player = self.players[self.currentPlayer]
                        self.gameUI.showStocksUi(curr_player.getStocks(), 'Le cedole di '+curr_player.playerName)
                    elif event.ui_element == self.gameUI.nextStock:
                        curr_player = self.players[self.currentPlayer]
                        self.gameUI.showNextStock()
                    elif event.ui_element == self.gameUI.previousStock:
                        curr_player = self.players[self.currentPlayer]
                        self.gameUI.showPreviousStock()
                    elif event.ui_element == self.gameUI.closeStock:                        
                        self.gameUI.closeStockUi()
                        self.screen.fill(BLACK)
                        self.dice.drawDices(self.screen)
                        self.gameUI.passButton.enable()
                    elif event.ui_element == self.gameUI.chooseBut:
                        curr_player = self.players[self.currentPlayer]
                        chosenStock = self.gameUI.getShowedStock()
                        curr_player.addStock(chosenStock)
                        curr_player.changeBalance(-chosenStock.stock_value)
                        self.board.removeStock(chosenStock)
                        self.gameUI.closeStockUi()
                        self.screen.fill(BLACK)
                        self.dice.drawDices(self.screen)
                        self.gameUI.updateLabel(curr_player)
                        self.gameUI.passButton.enable()
                        self.gameUI.showStocks.enable()
                    elif event.ui_element == self.gameUI.chooseMoveBut:
                        curr_player = self.players[self.currentPlayer]
                        chosenStock = self.gameUI.getShowedStock()
                        curr_cell = self.board.getCell(chosenStock.position)
                        curr_player.setPosition(chosenStock.position)
                        self.enableBuyButton(curr_cell, curr_player)
                        self.gameUI.closeStockUi()
                        self.screen.fill(BLACK)
                        self.dice.drawDices(self.screen)
                        self.gameUI.passButton.enable()
                        self.gameUI.showStocks.enable()

                self.gameUI.manager.process_events(event)            
            
            # Now we update at all turn the stockboard for avoiding 
            self.gameUI.updateStockboard(self.players, Player.last_stock_update)
            self.board.draw(self.screen)
            for i, player in enumerate(self.players):
                self.board.drawPlayerCar(self.screen, player, i, len(self.players))
            
            time_delta = self.clock.tick(FPS) / 1000.0
            self.gameUI.manager.update(time_delta)            
            self.gameUI.manager.draw_ui(self.screen)
            pygame.display.update()

    def turn(self):
        disablePassButton = False
        score = roll()
        self.dice.updateDice(score,self.screen)
        curr_player = self.players[self.currentPlayer]
        #curr_player.move(score[0] + score[1])
        curr_player.move(5)
        cell = self.board.cells[curr_player.position]
        #check turn and crash before any other events or effect of the cells
        checkTurn(curr_player)
        checkCrash(self.players.copy(), self.currentPlayer)
        #case cell with stock
        if(cell.cellType == STOCKS_TYPE):
            #curr_player.move(10)
            self.enableBuyButton(cell, curr_player)
            # we need to create a copy of the list in order to perform some edit of the list later
            checkForPenalty(self.board.cells, self.players.copy(), self.currentPlayer)            
        #case special cell
        else:
            self.gameUI.buyButton.disable()
            disablePassButton = self.specialCellLogic(cell, curr_player)
        
        self.gameUI.updateAllPlayerLables(self.players)
        self.gameUI.launchDice.disable()

        if disablePassButton:
            self.gameUI.passButton.disable()
        else:
            self.gameUI.passButton.enable()

        if is_double(score):
            self.gameUI.passButton.disable()
            self.gameUI.launchDice.enable()

    def enableBuyButton(self, cell, player):
    
        if(cell.cellType != STOCKS_TYPE or len(cell.stocks)  == 0):
            self.gameUI.buyButton.disable()
        else:
            if player.balance >= cell.stocks[0].stock_value:
                self.gameUI.buyButton.enable()
            else:
                self.gameUI.buyButton.disable()

    def specialCellLogic(self, cell, player):
        disablePassButton = False

        if cell.cellType == START_TYPE:
            startLogic(player)        
        elif cell.cellType == EVENTS_TYPE:
            eventsLogic(player)
        elif cell.cellType == STOCKS_PRIZE_TYPE:
            stockPrizeLogic(player)
        elif cell.cellType == QUOTATION_TYPE:
            quotationLogic(player)
        elif cell.cellType == CHOOSE_STOCK_TYPE:
            stocks = self.board.getAvailbleStocks()
            self.gameUI.disableActions()
            self.gameUI.showMoveToStock(stocks, 'Scegli su quale cedola vuoi spostarti')
            disablePassButton = True
        elif cell.cellType == SIX_HUNDRED_TYPE:
            sixHundredLogic(player)
        elif cell.cellType == FREE_STOP_TYPE:
            stocks = self.board.getPurchasableStocks(player.balance)
            self.gameUI.disableActions()
            self.gameUI.showChooseStock(stocks, 'Scegli quale vuoi comprare')
            disablePassButton = True
        elif cell.cellType == CHANCE_TYPE:
            score, amount = chanceLogic(player, self.squareBalance)
            self.squareBalance += amount
            self.dice.updateDice(score, self.screen)
            self.gameUI.updateSquareBalanceLabel(self.squareBalance)

        return disablePassButton
        