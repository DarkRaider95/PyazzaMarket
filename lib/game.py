import pygame
from .constants import FPS, WIDTH, HEIGHT
from .board import Board
from .player import Player
from .dice import Dice

class Game:
    def __init__(self, width, height, clock, players):
        self.clock = clock
        self.width = width
        self.height = height
        self.running = True
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('PyazzaMarket')
        self.players = players
        self.board = Board()
        self.dice = Dice()

    def start(self):
        players = []
        for player in self.players:
            players.append(Player(player["name"], player["color"]))
        self.board.initialiaze_cells(self.window)
        self.board.draw(self.window)
        self.dice.drawDices(self.window)

        for index, player in enumerate(players):
            self.board.drawPlayerCar(self.window, 0, player, index, len(players))

        while self.running:
            self.clock.tick(FPS)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:#quit_button.collidepoint(mouse_pos) == 'QUIT' or event.type == pygame.QUIT:
                    self.running = False