from .constants import STOCK_HEIGHT, STOCK_WIDTH, LOGO_WIDTH, LOGO_HEIGHT, PRICE_WIDTH, PRICES_HEIGHT, WIDTH, HEIGHT, WHITE, BLACK
import pygame

class Stock:
    string_values = [
        "1 Cedola",
        "2 Cedole della stessa società",
        "3 Cedole della stesso colore",
        "4 Cedole della stesso colore",
        "5 Cedole della stesso colore",
        "6 Cedole della stesso colore",
    ]
    def __init__(self, color, stock_value, values, logo, position):
        self.color = color
        self.stock_value = stock_value
        self.values = values
        self.logo = logo
        self.position = position
        self.font_stock_value = pygame.font.Font(None, 100)
        self.fees = pygame.font.Font(None, 32)

    def draw(self, screen):
        #Draw stock and spaces for logo and fees
        stock_x = WIDTH // 2 - STOCK_WIDTH // 2
        stock_y = HEIGHT // 2 - STOCK_HEIGHT // 2
        logo_x = WIDTH // 2 - LOGO_WIDTH // 2
        logo_y = stock_y + 50 
        price_x = WIDTH // 2 - PRICE_WIDTH // 2
        price_y = logo_y + LOGO_HEIGHT + 150
        rect = pygame.Rect(stock_x, stock_y, STOCK_WIDTH, STOCK_HEIGHT)
        logorect = pygame.Rect(logo_x, logo_y, LOGO_WIDTH, LOGO_HEIGHT)
        feesrect = pygame.Rect(price_x, price_y, PRICE_WIDTH, PRICES_HEIGHT)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, WHITE, logorect)
        pygame.draw.rect(screen, WHITE, feesrect)

        #Draw stock price and fees
        stock_price = self.font_stock_value.render(str(self.stock_value) + "  SCUDI", True, WHITE)
        screen.blit(stock_price, (WIDTH // 2 - stock_price.get_width() // 2, logo_y + LOGO_HEIGHT + 50))

        for i in range(0,len(self.values)):
            #write string value
            string_value = self.fees.render(Stock.string_values[i], True, BLACK)
            screen.blit(string_value, (price_x + 10, price_y + 30 * i + 1))
            #write fee value for that string
            fee_price = self.fees.render(str(self.values[i]) + " SCUDI", True, BLACK)
            screen.blit(fee_price, (price_x + PRICE_WIDTH - fee_price.get_width() - 10, price_y + 30 * i + 1))

