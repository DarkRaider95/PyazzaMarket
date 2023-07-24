import pygame
from .constants import FPS, WIDTH, HEIGHT, CHOOSE_STOCK_TYPE, FREE_STOP_TYPE, CHANCE_TYPE, QUOTATION
from .board import Board
from .player import Player
from .gameUI import GameUI
from .dice import Dice
from .event import Event
from .gameLogic import *
import pygame_gui
from collections import deque
import time
import random

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
        #creating events
        events = Event.initialize_events()
        self.events = deque(events)
        random.shuffle(self.events)
        self.__squareBalance = 2000
        random.shuffle(QUOTATION) # this function do an inplace shuffle to QUOTATION
        self.newQuotation = deque(QUOTATION) # this function create a ring list that work using rotate()

        Player.last_stock_update = time.time()
        for player in players:
            self.players.append(Player(player["name"], player["color"]))

        self.currentPlayer = 0 # Magari al posto dell'indice possiamo salvare direttamente il giocatare, così evitiamo di cercarlo all'interno dell'array di giocatori

    def start(self):
        self.board.initialiaze_cells()
        self.board.draw(self.screen)
        self.dice.drawDices(self.screen)
        self.gameUI.draw_actions_ui()
        self.gameUI.draw_leaderboard(self.players, self.__squareBalance, self.players[self.currentPlayer])
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
                        buyStock(self.board.cells, curr_player)
                        self.gameUI.updateAllPlayerLables(self.players)
                        self.gameUI.buyButton.disable()
                        self.gameUI.enableShowStockButton(self.players[self.currentPlayer])
                    elif event.ui_element == self.gameUI.passButton:
                        self.currentPlayer = (self.currentPlayer + 1) % len(self.players)
                        self.skipTurn()
                        self.gameUI.updateTurnLabel(self.players[self.currentPlayer])
                        self.gameUI.launchDice.enable()
                        self.gameUI.passButton.disable()
                        self.gameUI.buyButton.disable()
                        self.gameUI.enableShowStockButton(self.players[self.currentPlayer])
                    elif event.ui_element == self.gameUI.showStocks:
                        curr_player = self.players[self.currentPlayer]
                        self.gameUI.disableActions()
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
                        self.gameUI.renableActions()
                    elif event.ui_element == self.gameUI.chooseBut:
                        curr_player = self.players[self.currentPlayer]
                        chosenStock = self.gameUI.getShowedStock()
                        curr_player.addStock(chosenStock)
                        curr_player.changeBalance(-chosenStock.getStockValue())
                        self.board.removeStock(chosenStock)
                        self.gameUI.closeStockUi()
                        self.screen.fill(BLACK)
                        self.dice.drawDices(self.screen)
                        self.gameUI.updateAllPlayerLables(self.players)
                        self.gameUI.renableActions()
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
                    elif event.ui_element == self.gameUI.eventBut:
                        curr_player = self.players[self.currentPlayer]
                        self.eventsLogic(curr_player)
                        self.gameUI.closeEventUi()
                        self.screen.fill(BLACK)
                        self.dice.drawDices(self.screen)
                        self.gameUI.updateAllPlayerLables(self.players)
                        self.gameUI.renableActions()
                    elif event.ui_element == self.gameUI.buyAnyBut:
                        chosenStock = self.gameUI.getShowedStock()
                        curr_player = self.players[self.currentPlayer]
                        transferStock(self.board, curr_player, chosenStock)
                        self.gameUI.updateAllPlayerLables(self.players)
                        self.gameUI.renableActions()
                    elif event.ui_element == self.gameUI.closeAlertBut:
                        self.gameUI.closeAlert(self.players, self.dice)
                self.gameUI.manager.process_events(event)            
            
            # Now we update at all turn the stockboard for avoiding 
            self.gameUI.updateStockboard(self.players, Player.last_stock_update, self.dice)
            self.board.draw(self.screen)
            for i, player in enumerate(self.players):
                self.board.drawPlayerCar(self.screen, player, i, len(self.players))
            
            time_delta = self.clock.tick(FPS) / 1000.0
            self.gameUI.manager.update(time_delta)            
            self.gameUI.manager.draw_ui(self.screen)
            pygame.display.update()

    def skipTurn(self):
        curr_player = self.players[self.currentPlayer]
        while curr_player.getSkipTurn():
            curr_player.skipTurn(False)
            self.currentPlayer =  (self.currentPlayer+1) % len(self.players)
            curr_player = self.players[self.currentPlayer]

    def turn(self):
        tiroDoppio = False
        #disablePassButton = False
        self.gameUI.launchDice.disable()
        self.gameUI.passButton.enable()
        score = roll()
        self.dice.updateDice(score,self.screen)
        #is double
        if is_double(score):
            self.gameUI.passButton.disable()
            self.gameUI.launchDice.enable()
            tiroDoppio = True

        curr_player = self.players[self.currentPlayer]
        curr_player.move(score[0] + score[1])
        #curr_player.move(4)
        cell = self.board.cells[curr_player.position]
        #check turn and crash before any other events or effect of the cells
        checkTurn(curr_player)
        crash = checkCrash(self.players.copy(), self.currentPlayer)
        if tiroDoppio and crash:
            self.gameUI.drawAlert("Doppio e incidente!")
        elif tiroDoppio:
            self.gameUI.drawAlert("Tiro doppio!")
        elif crash:
            self.gameUI.drawAlert("Incidente!")
        #case cell with stock
        if(cell.cellType == STOCKS_TYPE):
            #curr_player.move(10)
            self.enableBuyButton(cell, curr_player)
            # we need to create a copy of the list in order to perform some edit of the list later
            checkForPenalty(self.board.cells, self.players.copy(), self.currentPlayer)            
        #case special cell
        else:
            #disablePassButton = self.specialCellLogic(cell, curr_player)
            self.specialCellLogic(cell, curr_player)

        self.gameUI.updateAllPlayerLables(self.players)
        
        #self.gameUI.passButton.enable()
#        if disablePassButton:
#            self.gameUI.passButton.disable()
#        else:
#           self.gameUI.passButton.enable()
            #disablePassButton = self.specialCellLogic(cell, curr_player)

    def enableBuyButton(self, cell, player):
    
        if(cell.cellType != STOCKS_TYPE or len(cell.stocks)  == 0):
            self.gameUI.buyButton.disable()
        else:
            if player.balance >= cell.stocks[0].getStockValue():
                self.gameUI.buyButton.enable()
            else:
                self.gameUI.buyButton.disable()

    def specialCellLogic(self, cell, player):
        #disablePassButton = False

        if cell.cellType == START_TYPE:
            startLogic(player)        
        elif cell.cellType == EVENTS_TYPE:
            self.gameUI.disableActions()
            self.gameUI.showEventUi(self.events[0])
            #disablePassButton = True  
        elif cell.cellType == STOCKS_PRIZE_TYPE:
            stockPrizeLogic(player)
        elif cell.cellType == QUOTATION_TYPE:
            quotationLogic(self.players, self.board, self.newQuotation, self)
        elif cell.cellType == CHOOSE_STOCK_TYPE:
            stocks = self.board.getAvailbleStocks()
            self.gameUI.disableActions()
            self.gameUI.showMoveToStock(stocks, 'Scegli su quale cedola vuoi spostarti')
            #disablePassButton = True
        elif cell.cellType == SIX_HUNDRED_TYPE:
            sixHundredLogic(player)
        elif cell.cellType == FREE_STOP_TYPE:
            stocks = self.board.getPurchasableStocks(player.balance)
            self.gameUI.disableActions()
            self.gameUI.showChooseStock(stocks, 'Scegli quale vuoi comprare')
            #disablePassButton = True
        elif cell.cellType == CHANCE_TYPE:
            score, amount = chanceLogic(player, self.__squareBalance)
            if amount < 0:
                self.__squareBalance += 0
            else:
                self.__squareBalance += amount
            self.dice.updateDice(score, self.screen)
            self.gameUI.updateSquareBalanceLabel(self.__squareBalance)

        #return disablePassButton
        
    def eventsLogic(self, player):
        event = self.events[0]
        
        if event.evenType == COLOR_EVENT:
            pass
        elif event.evenType == BUY_ANTHING_EVENT:
            stocks = self.board.getAvailbleStocks()            
            for p in self.players:
                if p != player:
                    stocks.extend(player.getStocks())
            self.gameUI.disableActions()
            self.gameUI.showBuyAnythingStock(stocks, 'Scegli quale vuoi comprare (Nessuno può opporsi alla vendita)')            
        elif event.evenType == STOP_1:
            player.skipTurn(True)
        elif event.evenType == FREE_PENALTY:
            player.freePenalty(True)
        elif event.evenType == FREE_PENALTY_MARTINI:
            player.freeMartini(True)
        elif event.evenType == EVERYONE_FIFTY_EVENT:
            everyOneFifty(self.players)
        elif event.evenType == PREVIOUS_PLAYER_GALUP:
            previousPlayerIndex = (self.currentPlayer-1) % len(self.players)
            previousPlayer = self.players[previousPlayerIndex]
            previousPlayer.setPosition(39)
            playerOwnStock = whoOwnsStock(self.players, 39)[0] #bisogna ragionare come gestire questo caso se ci sono più giocatori quale penalità prendo quella più alta o quella più bassa?
            stock = playerOwnStock.getStockByPos(39)
            amount = playerOwnStock.computePenalty(stock)
            previousPlayer.changeBalance(amount)
        elif event.evenType == NEXT_PLAYER_PAY:
            nextPlayerIndex = (self.currentPlayer+1) % len(self.players)
            nextPlayer = self.players[nextPlayerIndex]
            nextPlayer.changeBalance(-200)
        elif event.evenType == GIFT_EVENT:
            effectData = event.effectData   
            stock = self.board.getStockIfAvailable(effectData['stockIndex'])
            if stock is not None:
                player.addStock(stock)
            else:                
                player.changeBalance(effectData['amount'])
        elif event.evenType == GET_EVENT:
            effectData = event.effectData
            
            if 'from' in effectData.keys():
                fromWho = effectData['from']
                if fromWho == 'others':
                    getMoneyFromOthers(self.players.copy(), self.currentPlayer, effectData['amount'])
            else:
                player.changeBalance(effectData['amount'])
        elif event.evenType == GO_EVENT:
            self.goEventLogic(player, event)
        elif event.evenType == PAY_EVENT:
            effectData = event.effectData

            if 'to' in effectData.keys():
                toWho = effectData['to']
                if toWho == 'others':
                    payMoneyToOthers(self.players.copy(), self.currentPlayer, effectData['amount'])
            else:
                player.changeBalance(-effectData['amount'])
        elif event.evenType == OWN_EVENT:
            effectData = event.effectData
            
            owners = whoOwnsStockByName(self.players, effectData['stockName'])
            
            if len(owners) > 0:
                for owner in owners:
                    update_owner_balance(owner, effectData['stockName'], effectData['getAmount'], effectData['each'])

            if effectData['othersPayValue'] is not None:
                update_others_balance(self.players.copy(), owners, effectData['othersPayValue'])

        elif event.evenType == BUY_EVENT:
            stock = self.board.getStockIfAvailable(effectData['stockIndex'])
            if stock is not None:
                player.addStock(stock)
                player.changeBalance(-stock.getOriginalValue())
            else:
                print('BUY CASE START NEGOTIATION')
                pass # avviare trattativa con proprietario
        
        #rotate the events list
        self.events.rotate(-1)


    def goEventLogic(self, player, event):
        effectData = event.effectData

        if effectData['startCheck']:
            passStart = checkStartPass(player, effectData['destination'])
            if passStart:
                player.changeBalance(300)

        if effectData['pass'] is not None:
            passAmount = computePassAmount(self.players.copy(), player.position, self.currentPlayer, effectData['pass'], effectData['destination'])
            player.changeBalance(passAmount)

        if effectData['someone']:#implement interface to choose someone
            print('GOTO SOMEONE CASE')
            pass

        if effectData['buy']:
            stock = self.board.getStockIfAvailable(effectData['destination'])
            if stock is not None:
                player.addStock(stock)
                player.changeBalance(-stock.getOriginalValue())
            else:
                print('GOTO BUY CASE START NEGOTIATION')
                pass #implement gui to start negotiation with owner

        if effectData['get'] is not None:
            player.changeBalance(effectData['get'])

        player.setPosition(effectData['destination'])

    def setSquareBalance(self, new_balance):
        self.__squareBalance += new_balance
        if self.__squareBalance < 0:
            self.__squareBalance == 0
        self.gameUI.updateSquareBalanceLabel(self.__squareBalance)
