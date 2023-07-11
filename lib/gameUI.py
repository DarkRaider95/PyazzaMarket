import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UIPanel, UILabel, UIImage
from .constants import *

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
        #self.actions_UI = pygame.Surface((ACTIONS_WIDTH, ACTIONS_HEIGHT))
        #self.actions_rect = pygame.Rect(30, HEIGHT - 30 - ACTIONS_HEIGHT, ACTIONS_WIDTH, ACTIONS_HEIGHT)#pygame.Surface((ACTIONS_WIDTH, ACTIONS_HEIGHT))

    def draw_actions_ui(self):
        panel_rect = pygame.Rect((30, HEIGHT - 30 - ACTIONS_HEIGHT), (ACTIONS_WIDTH, ACTIONS_HEIGHT))
        actions_UI = UIPanel(panel_rect, manager=self.manager)
        #actionLabel = self.font.render(str('AZIONI'), True, BLACK)
        label_rect = pygame.Rect((ACTIONS_WIDTH // 2 - LABEL_WIDTH // 2, 10), (LABEL_WIDTH, LABEL_HEIGHT))
        self.actionLabel = UILabel(label_rect, "AZIONI", manager=self.manager, container=actions_UI)
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
        
        self.buyButton.disable()
        
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
        
        self.passButton.disable()
        self.showStocks.disable()
        

    def draw_leaderboard(self, players, squareBalance):
        # DRAWING THE BOARD
        panel_rect = pygame.Rect((30, 30), (LEADERBOARD_WIDTH, LEADERBOARD_HEIGHT)) # x, y, width, height
        self.leaderboard = UIPanel(panel_rect, manager=self.manager)
        # ADDING THE TITLE LABEL
        title_rect = pygame.Rect((LEADERBOARD_WIDTH // 2 - LEADERBOARD_LABEL_WIDTH // 2, 10), (LEADERBOARD_LABEL_WIDTH, LABEL_HEIGHT))
        UILabel(title_rect, "LEADERBOARD", manager=self.manager, container=self.leaderboard)
        # ADDING SQUARE BALANCE LABEL
        balance_rect = pygame.Rect((LEADERBOARD_WIDTH // 2 - LEADERBOARD_LABEL_WIDTH // 2, 30), (LEADERBOARD_LABEL_WIDTH, LABEL_HEIGHT))
        self.squareBalanceLabel = UILabel(balance_rect, "Riserva di piazza : " + str(squareBalance), manager=self.manager, container=self.leaderboard)
        # Head of players table
        player_label_rect = pygame.Rect((LEADERBOARD_WIDTH // 2 - LEADERBOARD_LABEL_WIDTH // 2, 50), (LEADERBOARD_LABEL_WIDTH, LABEL_HEIGHT))
        UILabel(player_label_rect,  "Giocatore: Scudi | Azioni ", manager=self.manager, container=self.leaderboard)
        # ADDING THE PLAYERS LABELS
        for i, player in enumerate(players):
            player_label_rect = pygame.Rect((LEADERBOARD_WIDTH // 2 - LEADERBOARD_LABEL_WIDTH // 2, 50 + (20 * (i + 1))), (LEADERBOARD_LABEL_WIDTH, LABEL_HEIGHT))
            label = UILabel(player_label_rect,  player.playerName + " : " + str(player.balance) + " | " + str(player.stockValue()), manager=self.manager, container=self.leaderboard)
            self.playerLabels.append({"name": player.playerName, "label": label})
    
    def updateSquareBalanceLabel(self, squareBalance):
        self.squareBalanceLabel.set_text("Riserva di piazza : " + str(squareBalance))

    def updateLabel(self, player): # Maybe is better to update all the players each time since they are few
        for label in self.playerLabels:
            if label["name"] == player.playerName:
                label["label"].set_text(player.playerName + " : " + str(player.balance) + " | " + str(player.stockValue()))
                break
        
    def updateAllPlayerLables(self, players):
        for player in players:
            self.updateLabel(player)

    def showStocksUi(self, stocks, title):
        self.stocks = stocks
        self.showedStock = 0
        self.drawStockUi(title, True)

    def showChooseStock(self, stocks, title):
        self.stocks = stocks
        self.showedStock = 0
        self.drawStockUi(title, False)
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
        currStock.draw(self.screen)
        self.stockImage = UIImage(stockImageRect, currStock.surface, container=self.stocksUi, manager=self.manager)
        
    def showNextStock(self):
        self.showedStock = (self.showedStock + 1) % len(self.stocks)
        currStock =self.stocks[self.showedStock]
        currStock.draw(self.screen)
        self.stockImage.set_image(currStock.surface)    
    
    def showPreviousStock(self):
        self.showedStock = (self.showedStock - 1) % len(self.stocks)
        currStock =self.stocks[self.showedStock]
        currStock.draw(self.screen)
        self.stockImage.set_image(currStock.surface)
    
    def closeStockUi(self):
        self.stocksUi.kill()

    def enableShowStockButton(self, player):
        if len(player.stocks) > 0:
            self.showStocks.enable()
        else:
            self.showStocks.disable()

    def disableActions(self):
        self.launchDice.disable()
        self.buyButton.disable()
        self.passButton.disable()
        self.showStocks.disable()