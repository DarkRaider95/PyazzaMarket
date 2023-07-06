import pygame
from .constants import FPS, WIDTH, HEIGHT, RED, CORNER_1
from .stock import Stock
from .cell import Cell
from .board import Board

class Game:
    def __init__(self, width, height, clock):
        self.clock = clock
        self.width = width
        self.height = height
        self.running = True
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('PyazzaMarket')

    def start(self):
        #stock = Stock(RED, 100, [100, 280, 280, 360, 460, 900], None, 1)
        #image = pygame.image.load('PyazzaMarket/assets/corner_1.png')
        #cell = Cell(RED, 500, None, 0, 0, image)
        board = Board()
        board.initialiaze_cells(self.window)
        board.draw(self.window)

        while self.running:
            self.clock.tick(FPS)
            
            #cell.drawCorner(self.window)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:#quit_button.collidepoint(mouse_pos) == 'QUIT' or event.type == pygame.QUIT:
                    self.running = False