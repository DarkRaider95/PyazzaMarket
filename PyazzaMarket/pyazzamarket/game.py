import pygame
from .constants import FPS, WIDTH, HEIGHT, RED
from .stock import Stock

class Game:
    def __init__(self, width, height, clock):
        self.clock = clock
        self.width = width
        self.height = height
        self.running = True
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('PyazzaMarket')

    def start(self):
        stock = Stock(RED, 100, [100], None, 1)
        while self.running:
            self.clock.tick(FPS)
            stock.draw(self.window)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:#quit_button.collidepoint(mouse_pos) == 'QUIT' or event.type == pygame.QUIT:
                    self.running = False