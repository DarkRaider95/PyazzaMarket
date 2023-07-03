from .constants import STOCK_HEIGHT, STOCK_WIDTH, LOGO_WIDTH, LOGO_HEIGHT, PRICE_WIDTH, PRICES_HEIGHT, WIDTH, HEIGHT, WHITE
import pygame

class Stock:

    def __init__(self, color, stock_value, values, logo, position):
        self.color = color
        self.stock_value = stock_value
        self.values = values
        self.logo = logo
        self.position = position

    def draw(self, screen):
        rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 200, STOCK_WIDTH, STOCK_HEIGHT)
        logorect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 100, LOGO_WIDTH, LOGO_HEIGHT)
        pricerect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, PRICE_WIDTH, PRICES_HEIGHT)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, WHITE, logorect)
        pygame.draw.rect(screen, WHITE, pricerect)

