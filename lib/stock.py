from .constants import STOCK_HEIGHT, STOCK_WIDTH, LOGO_WIDTH, LOGO_HEIGHT, PRICE_WIDTH, PRICES_HEIGHT, WIDTH, HEIGHT, WHITE, BLACK, LOGOS_DIR
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
    def __init__(self, cellDef, position, name, logo_path, enable_graphics):
        self.color = cellDef['color']
        self.__original_value = cellDef['value']
        self.__logo_path = logo_path
        self.__position = position
        self.__name = name
        self.__penalties = cellDef['penalty']
        self.__owner = None
        self.__new_value = self.__original_value
        self.__index = cellDef['index']
        self.__new_penalties = self.__penalties
        if enable_graphics:
            self.surface = pygame.Surface((STOCK_WIDTH, STOCK_HEIGHT))
            self.fees = pygame.font.Font(None, 32)
            self.font_stock_value = pygame.font.Font(None, 100)
            self.__rect = pygame.Rect(0, 0, STOCK_WIDTH, STOCK_HEIGHT)
            self.__logo_x = STOCK_WIDTH // 2 - LOGO_WIDTH // 2
            self.__logo_y = 50
            self.__price_x = STOCK_WIDTH // 2 - PRICE_WIDTH // 2
            self.__price_y = self.__logo_y + LOGO_HEIGHT + 150
            self.__feesrect = pygame.Rect(self.__price_x, self.__price_y, PRICE_WIDTH, PRICES_HEIGHT)
            logo = pygame.image.load(self.__logo_path) # aggiungere path completo
            self.__logo = pygame.transform.scale(logo, (LOGO_WIDTH, LOGO_HEIGHT))
            self.__stock_price = self.font_stock_value.render(str(self.__new_value) + "  SCUDI", True, WHITE)
            self.__string_values_rendered = []
            for i in range(0,len(self.__new_penalties)):
                self.__string_values_rendered.append(self.fees.render(Stock.string_values[i], True, BLACK))
            self.__penalties_updated = True # at the beginning is equal to true in order to do the first render
            
    def draw(self): # pragma: no cover
        #Draw stock and spaces for logo and fees
        pygame.draw.rect(self.surface, self.color, self.__rect)
        self.surface.blit(self.__logo, (self.__logo_x, self.__logo_y))
        pygame.draw.rect(self.surface, WHITE, self.__feesrect)
        #Draw stock price and fees
        self.surface.blit(self.__stock_price, (STOCK_WIDTH // 2 - self.__stock_price.get_width() // 2, self.__logo_y + LOGO_HEIGHT + 50))

        for i in range(0,len(self.__new_penalties)):
            #write string value
            self.surface.blit(self.__string_values_rendered[i], (self.__price_x + 10, self.__price_y + 30 * i + 1))
            #write fee value for that string
            if self.__penalties_updated:
                if i == 0: # when the price is updated we set the array as empty
                    self.__fee_price_rendered = []
                fee_price = self.fees.render(str(self.__new_penalties[i]) + " SCUDI", True, BLACK)
                self.__fee_price_rendered.append(fee_price)
                self.surface.blit(fee_price, (self.__price_x + PRICE_WIDTH - fee_price.get_width() - 10, self.__price_y + 30 * i + 1))
            else:
                self.surface.blit(self.__fee_price_rendered[i], (self.__price_x + PRICE_WIDTH - self.__fee_price_rendered[i].get_width() - 10, self.__price_y + 30 * i + 1))

    def update_value(self, new_value):
        self.__new_value = new_value
        self.update_penalties()
        return self.__new_value - self.__original_value

    def update_penalties(self):
        self.__new_penalties = []
        self.__penalties_updated = True 
        for penalty in self.__penalties:
            self.__new_penalties.append(int(round((penalty / self.__original_value) * self.__new_value)))

    # all the getters and setters are below

    def get_original_value(self): # pragma: no cover
        return self.__original_value
    
    def get_stock_value(self): # pragma: no cover
        return self.__new_value
    
    def get_index(self): # pragma: no cover
        return self.__index
    
    def get_penalty(self): # pragma: no cover
        return self.__new_penalties.copy() # we pass a copy so that the original list is not modified
    
    def get_name(self): # pragma: no cover
        return self.__name

    def set_owner(self, player): # pragma: no cover
        self.__owner = player

    def get_owner(self): # pragma: no cover
        return self.__owner
    
    def get_position(self): # pragma: no cover
        return self.__position
    
    def get_color(self): # pragma: no cover
        return self.color
    
    def get_new_value(self): # pragma: no cover
        return self.__new_value