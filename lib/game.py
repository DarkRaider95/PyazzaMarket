import pygame
from .constants import FPS, WIDTH, HEIGHT, CHOOSE_STOCK_TYPE, FREE_STOP_TYPE, CHANCE_TYPE, QUOTATION
from .board import Board
from .player import Player
from .gameUI import GameUI
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
        self.gameUI = GameUI(self.screen, self.clock)
        self.__players = []
        #creating events
        events = Event.initialize_events()
        self.events = deque(events)
        random.shuffle(self.events)
        self.__squareBalance = 2000
        random.shuffle(QUOTATION) # this function do an inplace shuffle to QUOTATION
        self.new_quotation = deque(QUOTATION) # this function create a ring list that work using rotate()
        self.establish_players_order = True # we use this variable to understand when we have launched the game for the first time
        self.highestScore = 0 # we save the score for deciding which is the play with the highest score that will start first
        self.firstPlayerIndex = 0 # we save the index of the player that will start first
        self.firstPlayerStarted = True # we check if the all the players have throw the dices for decide who will start first

        Player.last_stock_update = time.time()
        for player in players:
            self.__players.append(Player(player["name"], player["color"]))

        self.currentPlayer = 0 # Magari al posto dell'indice possiamo salvare direttamente il giocatare, così evitiamo di cercarlo all'interno dell'array di giocatori

    def start(self):
        self.board.draw(self.screen)
        self.gameUI.drawDices()
        self.gameUI.draw_actions_ui()
        self.gameUI.draw_leaderboard(self.get_players(), self.__squareBalance, self.__players[self.currentPlayer])
        self.gameUI.draw_stockboard(self.get_players())

        self.gameUI.drawDiceOverlay(self.__players[self.currentPlayer].get_name() + ' tira dadi', 'Decisione turni')
        # we will handle the next players in the while loop

        for index, player in enumerate(self.get_players()):
            self.board.draw_player_car(self.screen, player, index, len(self.__players))

        while self.running:
            self.clock.tick(FPS)            

            for event in pygame.event.get():
                self.manage_events(event)
                self.gameUI.manager.process_events(event)            
            
            # Now we update at all turn the stockboard for avoiding 
            self.gameUI.updateStockboard(self.get_players(), Player.last_stock_update, self.gameUI)
            self.board.draw(self.screen)
            for i, player in enumerate(self.get_players()):
                self.board.draw_player_car(self.screen, player, i, len(self.get_players()))
            
            time_delta = self.clock.tick(FPS) / 1000.0
            self.gameUI.manager.update(time_delta)            
            self.gameUI.manager.draw_ui(self.screen)
            pygame.display.update()

    def set_skip_turn(self):
        curr_player = self.__players[self.currentPlayer]
        while curr_player.get_skip_turn():
            curr_player.set_skip_turn(False)
            self.currentPlayer =  (self.currentPlayer+1) % len(self.get_players())
            curr_player = self.__players[self.currentPlayer]

    def turn(self):
        tiroDoppio = False
        #disablePassButton = False
        self.gameUI.launchDice.disable()
        self.gameUI.passButton.enable()
        score = roll()
        self.gameUI.updateDice(score)
        #is double
        if is_double(score):
            self.gameUI.passButton.disable()
            self.gameUI.launchDice.enable()
            tiroDoppio = True

        curr_player = self.__players[self.currentPlayer]
        curr_player.move(score[0] + score[1])
        #curr_player.move(4)
        cell = self.board.get_cells()[curr_player.get_position()]
        #check turn and crash before any other events or effect of the cells
        check_turn(curr_player)
        crash = check_crash(self.get_players(), self.currentPlayer)
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
            check_for_penalty(self.board.get_cells(), self.get_players(), self.currentPlayer)            
        #case special cell
        else:
            #disablePassButton = self.specialCellLogic(cell, curr_player)
            self.specialCellLogic(cell, curr_player)

        self.gameUI.updateAllPlayerLables(self.get_players())
        
        #self.gameUI.passButton.enable()
#        if disablePassButton:
#            self.gameUI.passButton.disable()
#        else:
#           self.gameUI.passButton.enable()
            #disablePassButton = self.specialCellLogic(cell, curr_player)

    def manage_events(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.gameUI.launchDice:                        
                self.turn()
            elif event.ui_element == self.gameUI.buyButton:
                curr_player = self.__players[self.currentPlayer]
                buy_stock(self.board.get_cells(), curr_player)
                self.gameUI.updateAllPlayerLables(self.get_players())
                self.gameUI.buyButton.disable()
                self.gameUI.enableShowStockButton(self.__players[self.currentPlayer])
            elif event.ui_element == self.gameUI.passButton:
                self.currentPlayer = (self.currentPlayer + 1) % len(self.get_players())
                self.set_skip_turn()
                self.gameUI.updateTurnLabel(self.__players[self.currentPlayer])
                self.gameUI.launchDice.enable()
                self.gameUI.passButton.disable()
                self.gameUI.buyButton.disable()
                self.gameUI.enableShowStockButton(self.__players[self.currentPlayer])
            elif event.ui_element == self.gameUI.showStocks:
                curr_player = self.__players[self.currentPlayer]
                self.gameUI.disableActions()
                self.gameUI.showStocksUi(curr_player.get_stocks(), 'Le cedole di '+curr_player.get_name())
            elif event.ui_element == self.gameUI.nextStock:
                curr_player = self.__players[self.currentPlayer]
                self.gameUI.showNextStock()
            elif event.ui_element == self.gameUI.previousStock:
                curr_player = self.__players[self.currentPlayer]
                self.gameUI.showPreviousStock()
            elif event.ui_element == self.gameUI.closeStock:                        
                self.gameUI.closeStockUi()
                self.screen.fill(BLACK)
                self.gameUI.drawDices()
                self.gameUI.renableActions()
            elif event.ui_element == self.gameUI.chooseBut:
                curr_player = self.__players[self.currentPlayer]
                chosen_stock = self.gameUI.getShowedStock()
                curr_player.add_stock(chosen_stock)
                curr_player.change_balance(-chosen_stock.get_stock_value())
                self.board.remove_stock(chosen_stock)
                self.gameUI.closeStockUi()
                self.screen.fill(BLACK)
                self.gameUI.drawDices()
                self.gameUI.updateAllPlayerLables(self.get_players())
                self.gameUI.renableActions()
            elif event.ui_element == self.gameUI.chooseMoveBut:
                curr_player = self.__players[self.currentPlayer]
                chosen_stock = self.gameUI.getShowedStock()
                curr_cell = self.board.get_cell(chosen_stock.get_position())
                curr_player.set_position(chosen_stock.get_position())
                self.enableBuyButton(curr_cell, curr_player)
                self.gameUI.closeStockUi()
                self.screen.fill(BLACK)
                self.gameUI.drawDices()
                self.gameUI.passButton.enable()
                self.gameUI.showStocks.enable()
            elif event.ui_element == self.gameUI.eventBut:
                curr_player = self.__players[self.currentPlayer]
                self.eventsLogic(curr_player)
                self.gameUI.closeEventUi()
                self.screen.fill(BLACK)
                self.gameUI.drawDices()
                self.gameUI.updateAllPlayerLables(self.get_players())
                self.gameUI.renableActions()
            elif event.ui_element == self.gameUI.buyAnyBut:
                chosen_stock = self.gameUI.getShowedStock()
                curr_player = self.__players[self.currentPlayer]
                transfer_stock(self.board, curr_player, chosen_stock)
                self.gameUI.updateAllPlayerLables(self.get_players())
                self.gameUI.renableActions()
            elif event.ui_element == self.gameUI.closeAlertBut:
                self.gameUI.closeAlert(self.get_players(), self.gameUI)
            elif event.ui_element == self.gameUI.closeDiceOverlayBut:
                if self.establish_players_order:
                    self.gameUI.closeDiceOverlay(self.get_players(), self.gameUI)
                    self.currentPlayer =  (self.currentPlayer+1) % len(self.get_players())
                    self.gameUI.drawDiceOverlay(self.__players[self.currentPlayer].get_name() + ' tira dadi', 'Decisione turni')
                elif self.firstPlayerStarted:
                    # this will be fired only after all the players have throw the dices
                    self.gameUI.closeDiceOverlay(self.get_players(), self.gameUI)
                    self.currentPlayer = self.firstPlayerIndex
                    self.gameUI.updateTurnLabel(self.__players[self.currentPlayer])
                    self.firstPlayerStarted = False
                else:
                    self.gameUI.closeDiceOverlay(self.get_players(), self.gameUI)
            elif event.ui_element == self.gameUI.launchOverlayDiceBut:
                # when you throw the dices maybe you are deciding the order of the players
                # or you are in a chance cell
                if self.establish_players_order:
                    score = roll()
                    self.gameUI.updateDiceOverlay(score)
                    diceSum = score[0] + score[1]
                    if self.highestScore < diceSum:
                        self.firstPlayerIndex = self.currentPlayer
                        self.highestScore = diceSum
                    if self.currentPlayer == len(self.get_players()) - 1:
                        self.establish_players_order = False
                else:
                    # amount is the amount of money that the player has to pay or receive
                    score, amount = chance_logic(self.get_players[self.currentPlayer], self.__squareBalance)
                    self.gameUI.updateDiceOverlay(score)
                    if self.__squareBalance + amount < 0:
                        self.__squareBalance == 0
                    else:
                        self.__squareBalance += amount
                    self.gameUI.updateDice(score)
                    self.gameUI.updateSquareBalanceLabel(self.__squareBalance)
            else:
                print("Evento non gestito")

    def enableBuyButton(self, cell, player):
        if check_if_can_buy_stock(cell, player):
            self.gameUI.buyButton.enable()
        else:
            self.gameUI.buyButton.disable()

    def specialCellLogic(self, cell, player):
        #disablePassButton = False

        if cell.cellType == START_TYPE:
            start_logic(player)        
        elif cell.cellType == EVENTS_TYPE:
            self.gameUI.disableActions()
            self.gameUI.showEventUi(self.events[0])
        elif cell.cellType == STOCKS_PRIZE_TYPE:
            stock_prize_logic(player)
        elif cell.cellType == QUOTATION_TYPE:
            quotation_logic(self.get_players(), self.board, self.new_quotation, self)
        elif cell.cellType == CHOOSE_STOCK_TYPE:
            stocks = self.board.get_availble_stocks()
            self.gameUI.disableActions()
            self.gameUI.showMoveToStock(stocks, 'Scegli su quale cedola vuoi spostarti')
            #disablePassButton = True
        elif cell.cellType == SIX_HUNDRED_TYPE:
            six_hundred_logic(player)
        elif cell.cellType == FREE_STOP_TYPE:
            stocks = self.board.get_purchasable_stocks(player.get_balance())
            self.gameUI.disableActions()
            self.gameUI.showChooseStock(stocks, 'Scegli quale vuoi comprare')
            #disablePassButton = True
        elif cell.cellType == CHANCE_TYPE:
            self.gameUI.drawDiceOverlay(self.__players[self.currentPlayer].get_name() + ' tira dadi', 'Riserva monetaria', False)

        #return disablePassButton
        
    def eventsLogic(self, player):
        event = self.events[0]
        
        if event.evenType == COLOR_EVENT:
            pass
        elif event.evenType == BUY_ANTHING_EVENT:
            stocks = self.board.get_availble_stocks()            
            for p in self.__players:
                if p != player:
                    stocks.extend(player.get_stocks())
            self.gameUI.disableActions()
            self.gameUI.showBuyAnythingStock(stocks, 'Scegli quale vuoi comprare (Nessuno può opporsi alla vendita)')            
        elif event.evenType == STOP_1:
            player.set_skip_turn(True)
        elif event.evenType == FREE_PENALTY:
            player.freePenalty(True)
        elif event.evenType == FREE_PENALTY_MARTINI:
            player.set_free_martini(True)
        elif event.evenType == EVERYONE_FIFTY_EVENT:
            every_one_fifty(self.get_players())
        elif event.evenType == PREVIOUS_PLAYER_GALUP:
            previousPlayerIndex = (self.currentPlayer-1) % len(self.__players)
            previousPlayer = self.__players[previousPlayerIndex]
            previousPlayer.set_position(39)
            playerOwnStock = who_owns_stock(self.get_players(), 39)[0] #bisogna ragionare come gestire questo caso se ci sono più giocatori quale penalità prendo quella più alta o quella più bassa?
            stock = playerOwnStock.get_stock_by_pos(39)
            amount = playerOwnStock.compute_penalty(stock)
            previousPlayer.change_balance(amount)
        elif event.evenType == NEXT_PLAYER_PAY:
            nextPlayerIndex = (self.currentPlayer+1) % len(self.__players)
            nextPlayer = self.__players[nextPlayerIndex]
            nextPlayer.change_balance(-200)
        elif event.evenType == GIFT_EVENT:
            effectData = event.effectData   
            stock = self.board.get_stock_if_available(effectData['stockIndex'])
            if stock is not None:
                player.add_stock(stock)
            else:                
                player.change_balance(effectData['amount'])
        elif event.evenType == GET_EVENT:
            effectData = event.effectData
            
            if 'from' in effectData.keys():
                fromWho = effectData['from']
                if fromWho == 'others':
                    get_money_from_others(self.get_players(), self.currentPlayer, effectData['amount'])
            else:
                player.change_balance(effectData['amount'])
        elif event.evenType == GO_EVENT:
            self.goEventLogic(player, event)
        elif event.evenType == PAY_EVENT:
            effectData = event.effectData

            if 'to' in effectData.keys():
                toWho = effectData['to']
                if toWho == 'others':
                    pay_money_to_others(self.get_players(), self.currentPlayer, effectData['amount'])
            else:
                player.change_balance(-effectData['amount'])
        elif event.evenType == OWN_EVENT:
            effectData = event.effectData
            
            owners = who_owns_stock_by_name(self.get_players(), effectData['stockName'])
            
            if len(owners) > 0:
                for owner in owners:
                    update_owner_balance(owner, effectData['stockName'], effectData['getAmount'], effectData['each'])

            if effectData['othersPayValue'] is not None:
                update_others_balance(self.__players, owners, effectData['othersPayValue'])

        elif event.evenType == BUY_EVENT:
            stock = self.board.get_stock_if_available(effectData['stockIndex'])
            if stock is not None:
                player.add_stock(stock)
                player.change_balance(-stock.get_original_value())
            else:
                print('BUY CASE START NEGOTIATION')
                pass # avviare trattativa con proprietario
        
        #rotate the events list
        self.events.rotate(-1)


    def goEventLogic(self, player, event):
        effectData = event.effectData

        if effectData['startCheck']:
            passStart = check_start_pass(player, effectData['destination'])
            if passStart:
                player.change_balance(300)

        if effectData['pass'] is not None:
            passAmount = compute_pass_amount(self.__players, self.currentPlayer, effectData['pass'], effectData['destination'])
            player.change_balance(passAmount)

        if effectData['someone']:#implement interface to choose someone
            print('GOTO SOMEONE CASE')
            pass

        if effectData['buy']:
            stock = self.board.get_stock_if_available(effectData['destination'])
            if stock is not None:
                player.add_stock(stock)
                player.change_balance(-stock.get_original_value())
            else:
                print('GOTO BUY CASE START NEGOTIATION')
                pass #implement gui to start negotiation with owner

        if effectData['get'] is not None:
            player.change_balance(effectData['get'])

        player.set_position(effectData['destination'])

    def set_square_balance(self, new_balance):
        self.__squareBalance += new_balance
        if self.__squareBalance < 0:
            self.__squareBalance == 0
        self.gameUI.updateSquareBalanceLabel(self.__squareBalance)

    def get_players(self):
        return self.__players.copy()