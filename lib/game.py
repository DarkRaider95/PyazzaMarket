import pygame
from .constants import FPS, WIDTH, HEIGHT
from .board import Board
from .player import Player
from .gameUI import GameUI

class Game:
    def __init__(self, width, height, clock, players):
        self.clock = clock
        self.width = width
        self.height = height
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('PyazzaMarket')
        self.players = players

    def start(self):
        players = []
        for player in self.players:
            players.append(Player(player["name"], player["color"]))
        board = Board()
        board.initialiaze_cells(self.screen)
        board.draw(self.screen)

        gameUI = GameUI(self.screen, self.clock)
        gameUI.draw_actions_ui()
        #stock = Stock('RED', 500, [180, 200, 555 ,848,8484,488484], None, 0)
        #stock.draw(self.window)
        for index, player in enumerate(players):
            board.drawPlayerCar(self.screen, 0, player, index, len(players))

        while self.running:
            self.clock.tick(FPS)
            
            #cell.drawCorner(self.window)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:#quit_button.collidepoint(mouse_pos) == 'QUIT' or event.type == pygame.QUIT:
                    self.running = False

                gameUI.manager.process_events(event)

            time_delta = self.clock.tick(FPS) / 1000.0
            gameUI.manager.update(time_delta)

            #gameUI.manager.draw_ui(gameUI.actions_UI)            
            gameUI.manager.draw_ui(self.screen)