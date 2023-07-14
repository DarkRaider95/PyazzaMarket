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
    def __init__(self, cellDef, position, name):
        self.color = cellDef['color']
        self.__original_value = cellDef['value']
        self.stock_value = cellDef['value']
        self.logo = None # cellDef['logo']
        self.font_stock_value = pygame.font.Font(None, 100)
        self.fees = pygame.font.Font(None, 32)
        self.position = position
        self.name = name
        self.penalties = cellDef['penalty']
        self.surface = pygame.Surface((STOCK_WIDTH, STOCK_HEIGHT))
        self.owner = None        

    def draw(self):
        #Draw stock and spaces for logo and fees
        logo_x = STOCK_WIDTH // 2 - LOGO_WIDTH // 2
        logo_y = 50 
        price_x = STOCK_WIDTH // 2 - PRICE_WIDTH // 2
        price_y = logo_y + LOGO_HEIGHT + 150
        rect = pygame.Rect(0, 0, STOCK_WIDTH, STOCK_HEIGHT)
        logorect = pygame.Rect(logo_x, logo_y, LOGO_WIDTH, LOGO_HEIGHT)
        feesrect = pygame.Rect(price_x, price_y, PRICE_WIDTH, PRICES_HEIGHT)
        pygame.draw.rect(self.surface, self.color, rect)
        pygame.draw.rect(self.surface, WHITE, logorect)
        pygame.draw.rect(self.surface, WHITE, feesrect)
        #Draw stock price and fees
        stock_price = self.font_stock_value.render(str(self.stock_value) + "  SCUDI", True, WHITE)
        self.surface.blit(stock_price, (STOCK_WIDTH // 2 - stock_price.get_width() // 2, logo_y + LOGO_HEIGHT + 50))

        for i in range(0,len(self.penalties)):
            #write string value
            string_value = self.fees.render(Stock.string_values[i], True, BLACK)
            self.surface.blit(string_value, (price_x + 10, price_y + 30 * i + 1))
            #write fee value for that string
            fee_price = self.fees.render(str(self.penalties[i]) + " SCUDI", True, BLACK)
            self.surface.blit(fee_price, (price_x + PRICE_WIDTH - fee_price.get_width() - 10, price_y + 30 * i + 1))

    def updatePenalties(self, new_penalties):
        self.penalties = new_penalties

    def getOriginalValue(self):
        return self.__original_value