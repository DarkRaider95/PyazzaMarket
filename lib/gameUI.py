import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UIPanel, UILabel, UIImage
from .constants import *
import time

# Inizializzazione della finestra di gioco
pygame.display.set_caption("Menu di Gioco")

class GameUI:
    def __init__(self, screen, clock):  #each player initialised with its data
        self.screen = screen
        self.running = True # Used to shutdown the game
        self.clock = clock
        self.manager = UIManager((WIDTH, HEIGHT)) # Create something similar to pygame.display.set_mode((WIDTH, HEIGHT))
        self.buyButton = None
        self.playerLabels = []
        self.closeStock = None
        self.chooseMoveBut = None
        self.chooseBut = None
        self.stockboardLabels = []
        self.latestStockUpdate = None
        self.buyAnyBut = None
        self.eventBut = None
        self.nextStock = None
        self.previousStock = None
        self.turnName = None
        self.actionsEnabled = []
        self.actions = []
        self.disableActionCount = 0 # if you have two events that call disable action you have to make sure that you call for both renable action before to enable again the bottons

    def draw_actions_ui(self):
        panel_rect = pygame.Rect((30, HEIGHT - 30 - ACTIONS_HEIGHT), (ACTIONS_WIDTH, ACTIONS_HEIGHT))
        actions_UI = UIPanel(panel_rect, manager=self.manager)
        #actionLabel = self.font.render(str('AZIONI'), True, BLACK)
        label_rect = pygame.Rect((ACTIONS_WIDTH // 2 - LABEL_WIDTH // 2, 10), (LABEL_WIDTH, LABEL_HEIGHT))
        UILabel(label_rect, "AZIONI", manager=self.manager, container=actions_UI)
        #self.actions_UI.blit(actionLabel, (ACTIONS_WIDTH // 2 - actionLabel.get_width() // 2, 10))
        self.launchDice = UIButton(relative_rect=pygame.Rect(ACTIONS_WIDTH // 2 - BUTTON_WIDTH // 2, 50, BUTTON_WIDTH, BUTTON_HEIGHT),
                                text="Lancia i dadi",
                                container=actions_UI,
                                object_id = 'LAUNCH_DICE',
                                manager=self.manager)

        self.buyButton = UIButton(relative_rect=pygame.Rect(ACTIONS_WIDTH // 2 - BUTTON_WIDTH // 2, 100, BUTTON_WIDTH, BUTTON_HEIGHT),
                                text="Compra",
                                container=actions_UI,
                                object_id = 'BUY',
                                manager=self.manager)
        
        
        
        self.showStocks = UIButton(relative_rect=pygame.Rect(ACTIONS_WIDTH // 2 - BUTTON_WIDTH // 2, 150, BUTTON_WIDTH, BUTTON_HEIGHT),
                                text="Mostra Cedole",
                                container=actions_UI,
                                object_id = 'SHOW_STOCKS',
                                manager=self.manager)
        

        self.passButton = UIButton(relative_rect=pygame.Rect(ACTIONS_WIDTH // 2 - BUTTON_WIDTH // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT),
                                text="Passa il turno",
                                container=actions_UI,
                                object_id = 'PASS',
                                manager=self.manager)
        
        self.buyButton.disable()
        self.passButton.disable()
        self.showStocks.disable()

        self.actions = [self.launchDice, self.buyButton, self.showStocks, self.passButton]
        

    def draw_leaderboard(self, players, squareBalance, currentPlayer):
        # DRAWING THE BOARD
        position_x = LEADERBOARD_WIDTH // 2 - LEADERBOARD_LABEL_WIDTH // 2
        label_dimension = (LEADERBOARD_LABEL_WIDTH, LABEL_HEIGHT)
        panel_rect = pygame.Rect((30, 30), (LEADERBOARD_WIDTH, LEADERBOARD_HEIGHT)) # x, y, width, height
        leaderboard = UIPanel(panel_rect, manager=self.manager)
        # ADDING THE TITLE LABEL
        title_rect = pygame.Rect((position_x, 10), label_dimension)
        UILabel(title_rect, "LEADERBOARD", manager=self.manager, container=leaderboard)
        # ADDING WHO IS THE TURN
        turn_rect = pygame.Rect((position_x, 30), label_dimension)
        self.turnName = UILabel(turn_rect, "Turno di " + currentPlayer.playerName, manager=self.manager, container=leaderboard)
        # ADDING SQUARE BALANCE LABEL
        balance_rect = pygame.Rect((position_x, 50), label_dimension)
        self.squareBalanceLabel = UILabel(balance_rect, "Riserva di piazza : " + str(squareBalance), manager=self.manager, container=leaderboard)
        # Head of players table
        player_label_rect = pygame.Rect((position_x, 70), label_dimension)
        UILabel(player_label_rect,  "Giocatore: Scudi | Azioni ", manager=self.manager, container=leaderboard)
        # ADDING THE PLAYERS LABELS
        for i, player in enumerate(players): # considerare di fare una lable unica e andare a capo per ogni riga
            player_label_rect = pygame.Rect((position_x, 70 + (20 * (i + 1))), label_dimension)
            label = UILabel(player_label_rect,  player.playerName + " : " + str(player.balance) + " | " + str(player.stockValue()), manager=self.manager, container=leaderboard)
            self.playerLabels.append(label)
    
    def updateSquareBalanceLabel(self, squareBalance):
        self.squareBalanceLabel.set_text("Riserva di piazza : " + str(squareBalance))

    def updateTurnLabel(self, currentPlayer):
        self.turnName.set_text("Turno di " + currentPlayer.playerName)
         
    def draw_stockboard(self, players):
        # DRAWING THE BOARD
        label_dimension = (150, LABEL_HEIGHT)
        sorted_players = sorted(players, key=lambda x: len(x.getStocks()), reverse=True)
        max_stock = max(len(sorted_players[0].getStocks()), 1)
        num_columns = min(3, len(sorted_players))
        self.drawRowStockboard(0,num_columns,sorted_players, 20, 0, label_dimension, True)
        if len(sorted_players) > 3:
            self.drawRowStockboard(3, len(sorted_players), sorted_players, 60, max_stock, label_dimension, False)
        self.latestStockUpdate = time.time()
        # since we update the lastestStockUpdate we will not update twice the stockboard if someone sold a stock to another player

    def drawRowStockboard(self, start_range, end_range, sorted_player, offset, max_stock, label_dimension, first_row):
        for i in range(start_range, end_range):
            player = sorted_player[i]
            if first_row:
                position_x = WIDTH + 25 - CORNER_WIDTH - (CELL_WIDTH * 9) + (STOCKBOARD_WIDTH * i)
            else:
                position_x = WIDTH + 25 - CORNER_WIDTH - (CELL_WIDTH * 9) + (STOCKBOARD_WIDTH * (i - 3))
            # ADDING THE TITLE LABEL
            title_rect = pygame.Rect((position_x, offset + CELL_HEIGHT + (max_stock * 20)),(label_dimension))
            nameLabel = UILabel(title_rect, player.playerName, manager=self.manager)
            self.stockboardLabels.append(nameLabel)
            if len(player.getStocks()) == 0:
                player_label_rect = pygame.Rect((position_x, offset + 20 + CELL_HEIGHT + (max_stock * 20)), label_dimension)
                noStockLabel = UILabel(player_label_rect,  "No stock", manager=self.manager)
                self.stockboardLabels.append(noStockLabel)
            else:
                count_label = 0
                latest_stock_position = -1 # setted to -1 because the first stock will always be different
                for stock in player.getStocks(): # considerare di fare una lable unica e andare a capo per ogni riga
                    position_y = offset + 20 + CELL_HEIGHT + (20 * count_label) + (max_stock * 20)
                    if latest_stock_position == stock.position:
                        self.stockboardLabels[-1].set_text(stock.name + " 2x")
                    else:    
                        player_label_rect = pygame.Rect((position_x, position_y), label_dimension)
                        stockNameLabel = UILabel(player_label_rect,  stock.name, manager=self.manager)
                        count_label += 1
                        latest_stock_position = stock.position
                        self.stockboardLabels.append(stockNameLabel)

    def updateStockboard(self, players, last_stock_update, dice):
        # add a class variable for and update of the stock board as a or on the if cicle
        if last_stock_update > self.latestStockUpdate:
            for label in self.stockboardLabels:
                label.kill()
            self.screen.fill(BLACK)
            dice.drawDices(self.screen)
            self.stockboardLabels = []
            self.draw_stockboard(players)

    def updateAllPlayerLables(self, players):
        sorted_players = sorted(players, key=lambda x: x.balance + x.stockValue(), reverse=True)
        for i, player in enumerate(sorted_players):
            self.playerLabels[i].set_text(player.playerName + " : " + str(player.balance) + " | " + str(player.stockValue()))

    def showStocksUi(self, stocks, title):
        self.stocks = stocks
        self.showedStock = 0
        self.drawStockUi(title, True)

    def showBuyAnythingStock(self, stocks, title):
        self.stocks = stocks
        self.showedStock = 0
        self.drawStockUi(title, False)
        buyRect = pygame.Rect((STOCK_UI_WIDTH - STOCK_UI_BUT_WIDTH - 10, STOCK_UI_HEIGHT - STOCK_UI_BUT_HEIGHT - 10), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))

        self.buyAnyBut = UIButton(relative_rect=buyRect,
                                text="Compra quale vuoi",
                                container=self.stocksUi,
                                object_id = 'BUY_ANYTHING',
                                manager=self.manager)
        
    def showChooseStock(self, stocks, title):
        self.stocks = stocks
        self.showedStock = 0
        self.drawStockUi(title, True)
        chooseRect = pygame.Rect((STOCK_UI_WIDTH - STOCK_UI_BUT_WIDTH - 10, STOCK_UI_HEIGHT - STOCK_UI_BUT_HEIGHT - 10), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))

        self.chooseBut = UIButton(relative_rect=chooseRect,
                                text="Scegli",
                                container=self.stocksUi,
                                object_id = 'CHOOSE_STOCK',
                                manager=self.manager)
        
    def showMoveToStock(self, stocks, title):
        self.stocks = stocks
        self.showedStock = 0
        self.drawStockUi(title, False)
        chooseRect = pygame.Rect((STOCK_UI_WIDTH - STOCK_UI_BUT_WIDTH - 10, STOCK_UI_HEIGHT - STOCK_UI_BUT_HEIGHT - 10), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))

        self.chooseMoveBut = UIButton(relative_rect=chooseRect,
                                text="Scegli",
                                container=self.stocksUi,
                                object_id = 'CHOOSE_AND_MOVE',
                                manager=self.manager)

    def getShowedStock(self):
        return self.stocks[self.showedStock]

    def drawStockUi(self, title, close):
        panel_rect = pygame.Rect((WIDTH // 2 - STOCK_UI_WIDTH // 2, 20), (STOCK_UI_WIDTH, STOCK_UI_HEIGHT))
        self.stocksUi = UIPanel(panel_rect, starting_height= 2, manager=self.manager)
        
        title_rect = pygame.Rect((STOCK_UI_WIDTH // 2 - STOCK_UI_TITLE_WIDTH // 2, 10), (STOCK_UI_TITLE_WIDTH, STOCK_UI_TITLE_HEIGHT))
        UILabel(title_rect, title, manager=self.manager, container=self.stocksUi)

        nextRect = pygame.Rect((STOCK_UI_WIDTH - 30 - STOCK_UI_BUT_WIDTH, STOCK_UI_HEIGHT // 2 - STOCK_UI_BUT_HEIGHT // 2), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))
        prevRect = pygame.Rect((30, STOCK_UI_HEIGHT // 2 - STOCK_UI_BUT_HEIGHT // 2), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))
        closeRect = pygame.Rect((STOCK_UI_WIDTH - STOCK_UI_BUT_WIDTH, 0), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))

        self.nextStock = UIButton(relative_rect=nextRect,
                                text=">",
                                container=self.stocksUi,
                                object_id = 'NEXT_STOCK',
                                manager=self.manager)
        
        self.previousStock = UIButton(relative_rect=prevRect,
                                text="<",
                                container=self.stocksUi,
                                object_id = 'PREV_STOCK',
                                manager=self.manager)
        if(close):
            self.closeStock = UIButton(relative_rect=closeRect,
                                    text="X",
                                    container=self.stocksUi,
                                    object_id = 'CLOSE_STOCK_UI',
                                    manager=self.manager)
        
        stockImageRect = pygame.Rect((STOCK_UI_WIDTH // 2 - STOCK_WIDTH // 2, 60), (STOCK_WIDTH, STOCK_HEIGHT))        
        
        currStock =self.stocks[self.showedStock]
        currStock.draw()
        self.stockImage = UIImage(stockImageRect, currStock.surface, container=self.stocksUi, manager=self.manager)
        
    def showNextStock(self):
        self.showedStock = (self.showedStock + 1) % len(self.stocks)
        currStock =self.stocks[self.showedStock]
        currStock.draw()
        self.stockImage.set_image(currStock.surface)    
    
    def showPreviousStock(self):
        self.showedStock = (self.showedStock - 1) % len(self.stocks)
        currStock =self.stocks[self.showedStock]
        currStock.draw()
        self.stockImage.set_image(currStock.surface)
    
    def closeStockUi(self):
        self.stocksUi.kill()

    def enableShowStockButton(self, player):
        if len(player.getStocks()) > 0:
            self.showStocks.enable()
        else:
            self.showStocks.disable()

    def disableActions(self):
        for action in self.actions:
            if action.is_enabled:
                self.actionsEnabled.append(action)            
        self.launchDice.disable()
        self.buyButton.disable()
        self.passButton.disable()
        self.showStocks.disable()
        self.disableActionCount += 1

    def renableActions(self):
        self.disableActionCount += -1
        if self.disableActionCount == 0:
            for action in self.actionsEnabled:
                action.enable()

            self.actionsEnabled.clear()

    def showEventUi(self, event):
        self.showedEvent = event        
        self.drawEventUi()

    def drawEventUi(self):
        panel_rect = pygame.Rect((WIDTH // 2 - EVENT_UI_WIDTH // 2, 20), (EVENT_UI_WIDTH, EVENT_UI_HEIGHT))
        self.eventUi = UIPanel(panel_rect, starting_height= 2, manager=self.manager)
        
        title_rect = pygame.Rect((EVENT_UI_WIDTH // 2 - EVENT_UI_TITLE_WIDTH // 2, 10), (EVENT_UI_TITLE_WIDTH, EVENT_UI_TITLE_HEIGHT))
        UILabel(title_rect, 'EVENTI', manager=self.manager, container=self.eventUi)

        eventRect = pygame.Rect((EVENT_UI_WIDTH - 30 - EVENT_UI_BUT_WIDTH, EVENT_UI_HEIGHT // 2 - EVENT_UI_BUT_HEIGHT // 2), (EVENT_UI_BUT_WIDTH, EVENT_UI_BUT_WIDTH))
        

        self.eventBut = UIButton(relative_rect=eventRect,
                                text="OK",
                                container=self.eventUi,
                                object_id = 'EVENT_OK',
                                manager=self.manager)
        
        eventImageRect = pygame.Rect((EVENT_UI_WIDTH // 2 - EVENT_WIDTH // 2, 60), (EVENT_WIDTH, EVENT_HEIGHT))        
        
        self.showedEvent.draw()
        self.eventImage = UIImage(eventImageRect, self.showedEvent.surface, container=self.eventUi, manager=self.manager)

    def closeEventUi(self):
        self.eventUi.kill()

    def drawAlert(self, message):
        surface = pygame.Rect(((WIDTH - ALERT_WIDTH) // 2, (HEIGHT - ALERT_HEIGHT) // 2), (ALERT_WIDTH, ALERT_HEIGHT))
        self.alertUi = UIPanel(surface, starting_height=2, manager=self.manager)

        message_rect = pygame.Rect(((ALERT_WIDTH - ALERT_MESSAGE_WIDTH) // 2, (ALERT_HEIGHT - ALERT_MESSAGE_HEIGHT - 20) // 2), (ALERT_MESSAGE_WIDTH, ALERT_MESSAGE_HEIGHT))
        UILabel(message_rect, message, manager=self.manager, container=self.alertUi)

        close_rect = pygame.Rect(((ALERT_WIDTH - ALERT_BUT_WIDTH) // 2, ALERT_HEIGHT - ALERT_BUT_HEIGHT - 10), (ALERT_BUT_WIDTH, ALERT_BUT_HEIGHT))
        self.closeAlertBut = UIButton(relative_rect=close_rect, text="chiudi", container=self.alertUi, object_id="CLOSE_ALERT", manager=self.manager)

        self.disableActions()

    def closeAlert(self, players, dice):
        # since screen.fill(BLACK) is already on updateStockboard and 
        # dice.draw also we directly call that function
        self.alertUi.kill()
        self.updateStockboard(players, time.time(), dice)
        self.renableActions()
        