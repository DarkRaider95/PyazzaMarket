import pygame
from .constants import FPS, WIDTH, HEIGHT
from .board import Board
from .player import Player
from .gameUI import GameUI
from .dice import Dice
from .gameLogic import roll
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
        
        for player in players:
            self.players.append(Player(player["name"], player["color"]))

        self.currentPlayer = 0

    def start(self):
        self.board.initialiaze_cells()
        self.board.draw(self.screen)
        self.dice.drawDices(self.screen)
        self.gameUI.draw_actions_ui()

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
                        self.players[self.currentPlayer].move(score[0] + score[1])
                        curr_pos = self.players[self.currentPlayer].position
                        if(self.board.checkIfStockCell(self.players[self.currentPlayer]) or len(self.board.cells[curr_pos].stocks)  == 0):
                            self.gameUI.buyButton.disable()
                        else:
                            self.gameUI.buyButton.enable()
                        self.gameUI.launchDice.disable()
                        self.gameUI.passButton.enable()                        
                    elif event.ui_element == self.gameUI.buyButton:
                        curr_pos = self.players[self.currentPlayer].position
                        if(len(self.board.cells[curr_pos].stocks) > 0):
                            stock = self.board.cells[curr_pos].stocks.pop()
                            self.players[self.currentPlayer].stocks.append(stock)
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