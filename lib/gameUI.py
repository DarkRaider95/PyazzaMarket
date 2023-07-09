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

        #self.actions_UI = pygame.Surface((ACTIONS_WIDTH, ACTIONS_HEIGHT))
        #self.actions_rect = pygame.Rect(30, HEIGHT - 30 - ACTIONS_HEIGHT, ACTIONS_WIDTH, ACTIONS_HEIGHT)#pygame.Surface((ACTIONS_WIDTH, ACTIONS_HEIGHT))
        self.actions_UI = None
        self.leaderboard = None
    

    def draw_actions_ui(self):
        panel_rect = pygame.Rect((30, HEIGHT - 30 - ACTIONS_HEIGHT), (ACTIONS_WIDTH, ACTIONS_HEIGHT))
        self.actions_UI = UIPanel(panel_rect, manager=self.manager)
        self.actions_UI.background_colour = WHITE
        #actionLabel = self.font.render(str('AZIONI'), True, BLACK)
        label_rect = pygame.Rect((ACTIONS_WIDTH // 2 - LABEL_WIDTH // 2, 10), (LABEL_WIDTH, LABEL_HEIGHT))
        self.actionLabel = UILabel(label_rect, "AZIONI", manager=self.manager, container=self.actions_UI)
        #self.actions_UI.blit(actionLabel, (ACTIONS_WIDTH // 2 - actionLabel.get_width() // 2, 10))
        self.launchDice = UIButton(relative_rect=pygame.Rect(ACTIONS_WIDTH // 2 - BUTTON_WIDTH // 2, 50, BUTTON_WIDTH, BUTTON_HEIGHT),
                                text="Lancia i dadi",
                                container=self.actions_UI,
                                object_id = 'LAUNCH_DICE',
                                manager=self.manager)

        self.buyButton = UIButton(relative_rect=pygame.Rect(ACTIONS_WIDTH // 2 - BUTTON_WIDTH // 2, 100, BUTTON_WIDTH, BUTTON_HEIGHT),
                                text="Compra",
                                container=self.actions_UI,
                                object_id = 'BUY',
                                manager=self.manager)
        
        self.buyButton.disable()
        
        self.showStocks = UIButton(relative_rect=pygame.Rect(ACTIONS_WIDTH // 2 - BUTTON_WIDTH // 2, 150, BUTTON_WIDTH, BUTTON_HEIGHT),
                                text="Mostra Cedole",
                                container=self.actions_UI,
                                object_id = 'SHOW_STOCKS',
                                manager=self.manager)
        

        self.passButton = UIButton(relative_rect=pygame.Rect(ACTIONS_WIDTH // 2 - BUTTON_WIDTH // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT),
                                text="Passa il turno",
                                container=self.actions_UI,
                                object_id = 'PASS',
                                manager=self.manager)
        
        self.passButton.disable()
        

        #self.actions_UI.add(self.launchDice)
        #self.actions_UI.add(self.buyButton)
        #self.actions_UI.add(self.showStocks)
        #self.actions_UI.add(self.passButton)
        #pygame.draw.rect(self.screen, WHITE, self.actions_rect)
        #self.screen.blit(self.actions_UI, (30, HEIGHT - 30 - ACTIONS_HEIGHT))
        

    def draw_leaderboard(self, players, squareBalance): # For the moment we will owerwrite the leaderboard each time, but we can also store each single lable in update it
        # DRAWING THE BOARD
        panel_rect = pygame.Rect((30, 30), (LEADERBOARD_WIDTH, LEADERBOARD_HEIGHT)) # x, y, width, height
        self.leaderboard = UIPanel(panel_rect, manager=self.manager)
        self.leaderboard.background_colour = WHITE
        # ADDING THE TITLE LABEL
        title_rect = pygame.Rect((LEADERBOARD_WIDTH // 2 - LEADERBOARD_LABEL_WIDTH // 2, 10), (LEADERBOARD_LABEL_WIDTH, LABEL_HEIGHT))
        self.leaderboardLabel = UILabel(title_rect, "LEADERBOARD", manager=self.manager, container=self.leaderboard)
        # ADDING SQUARE BALANCE LABEL
        balance_rect = pygame.Rect((LEADERBOARD_WIDTH // 2 - LEADERBOARD_LABEL_WIDTH // 2, 30), (LEADERBOARD_LABEL_WIDTH, LABEL_HEIGHT))
        UILabel(balance_rect, "Riserva di piazza : " + str(squareBalance), manager=self.manager, container=self.leaderboard)
        # ADDING THE PLAYERS LABELS
        for i, player in enumerate(players):
            player_label_rect = pygame.Rect((LEADERBOARD_WIDTH // 2 - LEADERBOARD_LABEL_WIDTH // 2, 30 + (20 * (i + 1))), (LEADERBOARD_LABEL_WIDTH, LABEL_HEIGHT))
            UILabel(player_label_rect,  "Scudi " + player.playerName + " : " + str(player.balance), manager=self.manager, container=self.leaderboard)
            

