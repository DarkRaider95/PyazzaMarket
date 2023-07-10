import pygame
from .constants import FPS, WIDTH, HEIGHT, CHOOSE_STOCK_TYPE, FREE_STOP_TYPE, CHANCE_TYPE
from .board import Board
from .player import Player
from .gameUI import GameUI
from .dice import Dice
from .gameLogic import *
import pygame_gui

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
                        self.cells = buyStock(self.board.cells, curr_player)
                        self.gameUI.updateLabel(curr_player)
                        self.gameUI.buyButton.disable()
                    elif event.ui_element == self.gameUI.passButton:
                        self.currentPlayer = (self.currentPlayer + 1) % len(self.players)
                        self.gameUI.launchDice.enable()
                        self.gameUI.passButton.disable()

                self.gameUI.manager.process_events(event)            
            
            self.board.draw(self.screen)
            for i, player in enumerate(self.players):
                self.board.drawPlayerCar(self.screen, player, i, len(self.players))
            
            time_delta = self.clock.tick(FPS) / 1000.0
            self.gameUI.manager.update(time_delta)            
            self.gameUI.manager.draw_ui(self.screen)
            pygame.display.update()

    def turn(self):
        score = roll()
        self.dice.updateDice(score,self.screen)
        curr_player = self.players[self.currentPlayer]
        curr_player.move(score[0] + score[1])
        cell = self.board.cells[curr_player.position]
        #case cell with stock
        if(cell.cellType == STOCKS_TYPE):
            #curr_player.move(10)
            self.enableBuyButton(cell, curr_player)
            # we need to create a copy of the list in order to perform some edit of the list later
            checkForPenalty(self.board.cells, self.players.copy(), self.currentPlayer)            
        #case special cell
        else:
            self.specialCellLogic(cell, curr_player)

        checkCrash(self.players.copy(), self.currentPlayer)
        checkTurn(curr_player)
        self.gameUI.updateAllPlayerLables(self.players)
        self.gameUI.launchDice.disable()
        self.gameUI.passButton.enable()
        
    def enableBuyButton(self, cell, player):
    
        if(cell.cellType != STOCKS_TYPE or len(cell.stocks)  == 0):
            self.gameUI.buyButton.disable()
        else:
            if player.balance >= cell.stocks[0].stock_value:
                self.gameUI.buyButton.enable()
            else:
                self.gameUI.buyButton.disable()

    def specialCellLogic(self, cell, player):

        if cell.cellType == START_TYPE:
            startLogic(player)        
        elif cell.cellType == EVENTS_TYPE:
            eventsLogic(player)
        elif cell.cellType == STOCKS_PRIZE_TYPE:
            stockPrizeLogic(player)
        elif cell.cellType == QUOTATION_TYPE:
            quotationLogic(player)
        elif cell.cellType == CHOOSE_STOCK_TYPE:
            #player.stocks.append(chosenStock)
            pass
        elif cell.cellType == SIX_HUNDRED_TYPE:
            sixHundredLogic(player)
        elif cell.cellType == FREE_STOP_TYPE:
            #player.stocks.append(chosenStock)
            pass
        elif cell.cellType == CHANCE_TYPE:
            score, amount = chanceLogic(player, self.squareBalance)
            self.squareBalance += amount
            self.dice.updateDice(score, self.screen)
            #update dice
        