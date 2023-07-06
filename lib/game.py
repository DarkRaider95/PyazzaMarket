import pygame
from .constants import FPS, WIDTH, HEIGHT, RED, CORNER_1, CAR_RED
from .stock import Stock
from .cell import Cell
from .board import Board
from .player import Player

class Game:
    def __init__(self, width, height, clock, player_names):
        self.clock = clock
        self.width = width
        self.height = height
        self.running = True
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('PyazzaMarket')
        self.player_names = player_names

    def start(self):
        #stock = Stock(RED, 100, [100, 280, 280, 360, 460, 900], None, 1)
        #image = pygame.image.load('PyazzaMarket/assets/corner_1.png')
        #cell = Cell(RED, 500, None, 0, 0, image)
        player = Player(self.player_names[0], CAR_RED)
        board = Board()
        board.initialiaze_cells(self.window)
        board.draw(self.window)
        board.drawPlayerCar(self.window, 1, player)

        while self.running:
            self.clock.tick(FPS)
            
            #cell.drawCorner(self.window)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:#quit_button.collidepoint(mouse_pos) == 'QUIT' or event.type == pygame.QUIT:
                    self.running = False