import pygame
from .constants import FPS, WIDTH, HEIGHT
from .board import Board
from .player import Player
from .gameUI import GameUI
from .dice import Dice
from .gameLogic import roll, buyStock, enableBuyButton, checkForPenality
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

        for index, player in enumerate(self.players):
            self.board.drawPlayerCar(self.screen, player, index, len(self.players))

        while self.running:
            self.clock.tick(FPS)            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.gameUI.launchDice:                        
                        score = roll()
                        self.dice.updateDice(score,self.screen)
                        curr_player = self.players[self.currentPlayer]
                        #curr_player.move(score[0] + score[1])
                        curr_player.move(3)
                        enableBuyButton(self.board.cells, curr_player, self.gameUI, self.board)
                        checkForPenality(self.board.cells, self.players, self.currentPlayer, self.gameUI)
                        self.gameUI.launchDice.disable()
                        self.gameUI.passButton.enable()                        
                    elif event.ui_element == self.gameUI.buyButton:
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