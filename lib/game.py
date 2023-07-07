import pygame
from .constants import FPS, WIDTH, HEIGHT
from .board import Board
from .player import Player
from .gameUI import GameUI
from .dice import Dice

class Game:
    def __init__(self, width, height, clock, players):
        self.clock = clock
        self.width = width
        self.height = height
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('PyazzaMarket')
        self.players = players
        self.board = Board()
        self.dice = Dice()
        self.gameUI = GameUI(self.screen, self.clock)

    def start(self):
        players = []
        for player in self.players:
            players.append(Player(player["name"], player["color"]))
        
        self.board.initialiaze_cells(self.screen)
        self.board.draw(self.screen)
        self.dice.drawDices(self.screen)
        self.gameUI.draw_actions_ui()

        for index, player in enumerate(players):
            self.board.drawPlayerCar(self.screen, 0, player, index, len(players))

        while self.running:
            self.clock.tick(FPS)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.gameUI.manager.process_events(event)

            time_delta = self.clock.tick(FPS) / 1000.0
            self.gameUI.manager.update(time_delta)
            
            self.gameUI.manager.draw_ui(self.screen)