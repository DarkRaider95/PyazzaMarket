import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UIPanel, UILabel
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
        #self.actions_UI = pygame.Surface((ACTIONS_WIDTH, ACTIONS_HEIGHT))
        #self.actions_rect = pygame.Rect(30, HEIGHT - 30 - ACTIONS_HEIGHT, ACTIONS_WIDTH, ACTIONS_HEIGHT)#pygame.Surface((ACTIONS_WIDTH, ACTIONS_HEIGHT))

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

        #self.actions_UI.add(self.launchDice)
        #self.actions_UI.add(self.buyButton)
        #self.actions_UI.add(self.showStocks)
        #self.actions_UI.add(self.passButton)
        #pygame.draw.rect(self.screen, WHITE, self.actions_rect)
        #self.screen.blit(self.actions_UI, (30, HEIGHT - 30 - ACTIONS_HEIGHT))
        

    def draw_leaderboard(self, players, squareBalance):
        # DRAWING THE BOARD
        position_x = LEADERBOARD_WIDTH // 2 - LEADERBOARD_LABEL_WIDTH // 2
        label_dimension = (LEADERBOARD_LABEL_WIDTH, LABEL_HEIGHT)
        panel_rect = pygame.Rect((30, 30), (LEADERBOARD_WIDTH, LEADERBOARD_HEIGHT)) # x, y, width, height
        leaderboard = UIPanel(panel_rect, manager=self.manager)
        # ADDING THE TITLE LABEL
        title_rect = pygame.Rect((position_x, 10), label_dimension)
        UILabel(title_rect, "LEADERBOARD", manager=self.manager, container=leaderboard)
        # ADDING SQUARE BALANCE LABEL
        balance_rect = pygame.Rect((position_x, 30), label_dimension)
        UILabel(balance_rect, "Riserva di piazza : " + str(squareBalance), manager=self.manager, container=leaderboard)
        # Head of players table
        player_label_rect = pygame.Rect((position_x, 50), label_dimension)
        UILabel(player_label_rect,  "Giocatore: Scudi | Azioni ", manager=self.manager, container=leaderboard)
        # ADDING THE PLAYERS LABELS
        for i, player in enumerate(players): # considerare di fare una lable unica e andare a capo per ogni riga
            player_label_rect = pygame.Rect((position_x, 50 + (20 * (i + 1))), label_dimension)
            label = UILabel(player_label_rect,  player.playerName + " : " + str(player.balance) + " | " + str(player.stockValue()), manager=self.manager, container=leaderboard)
            self.playerLabels.append({"name": player.playerName, "label": label})
    
         
    def draw_stockboard(self, players):
        # DRAWING THE BOARD
        label_dimension = (150, LABEL_HEIGHT)
        sorted_player = sorted(players, key=lambda x: len(x.stocks), reverse=True)
        max_stock = max(len(sorted_player[0].stocks), 1)
        num_columns = min(3, len(sorted_player))
        self.drawRowStockboard(0,num_columns,sorted_player, 20, 0, label_dimension, True)
        if len(sorted_player) > 3:
            self.drawRowStockboard(3, len(sorted_player), sorted_player, 60, max_stock, label_dimension, False)

    def drawRowStockboard(self, start_range, end_range, sorted_player, offset, max_stock, label_dimension, first_row):
        for i in range(start_range, end_range):
            player = sorted_player[i]
            if first_row:
                position_x = WIDTH + 25 - CORNER_WIDTH - (CELL_WIDTH * 9) + (STOCKBOARD_WIDTH * i)
            else:
                position_x = WIDTH + 25 - CORNER_WIDTH - (CELL_WIDTH * 9) + (STOCKBOARD_WIDTH * (i - 3))
            # ADDING THE TITLE LABEL
            title_rect = pygame.Rect((position_x, offset + CELL_HEIGHT + (max_stock * 20)),(label_dimension))
            UILabel(title_rect, player.playerName, manager=self.manager)
            if len(player.stocks) == 0:
                player_label_rect = pygame.Rect((position_x, offset + 20 + CELL_HEIGHT + (max_stock * 20)), label_dimension)
                UILabel(player_label_rect,  "No stock", manager=self.manager)
            else:
                for j, stock in enumerate(player.stocks): # considerare di fare una lable unica e andare a capo per ogni riga
                    position_y = offset + 20 + CELL_HEIGHT + (20 * j) + (max_stock * 20)
                    player_label_rect = pygame.Rect((position_x, position_y), label_dimension)
                    UILabel(player_label_rect,  stock.name, manager=self.manager)

    def updateLabel(self, player): # Maybe is better to update all the players each time since they are few
        for label in self.playerLabels:
            if label["name"] == player.playerName:
                label["label"].set_text(player.playerName + " : " + str(player.balance) + " | " + str(player.stockValue()))
                break
        
    def updateAllPlayerLables(self, players):
        for player in players:
            self.updateLabel(player)