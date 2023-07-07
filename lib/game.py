import pygame
from .constants import FPS, WIDTH, HEIGHT
from .board import Board
from .player import Player

class Game:
    def __init__(self, width, height, clock, players):
        self.clock = clock
        self.width = width
        self.height = height
        self.running = True
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('PyazzaMarket')
        self.players = players

    def start(self):
        players = []
        for player in self.players:
            players.append(Player(player["name"], player["color"]))
        board = Board()
        board.initialiaze_cells(self.window)
        board.draw(self.window)
        #stock = Stock('RED', 500, [180, 200, 555 ,848,8484,488484], None, 0)
        #stock.draw(self.window)
        for index, player in enumerate(players):
            board.drawPlayerCar(self.window, 0, player, index, len(players))

        while self.running:
            self.clock.tick(FPS)
            
            #cell.drawCorner(self.window)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:#quit_button.collidepoint(mouse_pos) == 'QUIT' or event.type == pygame.QUIT:
                    self.running = False