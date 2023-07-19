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
        self.logo = None # cellDef['logo']
        self.font_stock_value = pygame.font.Font(None, 100)
        self.fees = pygame.font.Font(None, 32)
        self.position = position
        self.name = name
        self.__penalties = cellDef['penalty']
        self.surface = pygame.Surface((STOCK_WIDTH, STOCK_HEIGHT))
        self.owner = None        
        self.__new_value = self.__original_value
        self.__index = cellDef['index']
        self.__new_penalties = self.__penalties

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
        stock_price = self.font_stock_value.render(str(self.__new_value) + "  SCUDI", True, WHITE)
        self.surface.blit(stock_price, (STOCK_WIDTH // 2 - stock_price.get_width() // 2, logo_y + LOGO_HEIGHT + 50))

        for i in range(0,len(self.__new_penalties)):
            #write string value
            string_value = self.fees.render(Stock.string_values[i], True, BLACK)
            self.surface.blit(string_value, (price_x + 10, price_y + 30 * i + 1))
            #write fee value for that string
            fee_price = self.fees.render(str(self.__new_penalties[i]) + " SCUDI", True, BLACK)
            self.surface.blit(fee_price, (price_x + PRICE_WIDTH - fee_price.get_width() - 10, price_y + 30 * i + 1))

    def updateValue(self, new_value):
        self.__new_value = new_value
        self.updatePenalties()
        return self.__new_value - self.__original_value

    def getOriginalValue(self):
        return self.__original_value
    
    def getStockValue(self):
        return self.__new_value
    
    def getIndex(self):
        return self.__index
    
    def updatePenalties(self):
        self.__new_penalties = []
        for penalty in self.__penalties:
            self.__new_penalties.append(int(round((penalty / self.__original_value) * self.__new_value)))

    def getPenalty(self):
        return self.__new_penalties.copy() # we pass a copy so that the original list is not modified
    
    def get_name(self):
        return self.name
