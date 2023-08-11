import pygame
from .constants import *
from .stock import Stock

class Cell:
    # we should have name or position in both the cell and the stock in order to now where to put the stock in case the user will return it to the bank
    def __init__(self, cellDef, cellType, cell_x, cell_y, logo, cellImage, position, name, isCorner = False, angle = 0, enableGraphics = True):
        self.__stocks = None
        if(cellDef is not None):
            self.color = cellDef['color']
            self.__original_value = cellDef['value']
            self.__new_value = self.__original_value
            self.logo = logo
            self.__stocks = []
            for _ in range(0,2):
                self.__stocks.append(Stock(cellDef, position, name, enableGraphics))
            self.__stockIndex = cellDef['index']
            self.angle = cellDef['angle']
        else:
            self.angle = angle
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.cellImage = cellImage
        self.cellType = cellType
        self.position = position
        if enableGraphics:
            self.font_stock_value = pygame.font.Font(None, 30)
            self.surface = pygame.Surface((CORNER_WIDTH, CORNER_HEIGHT)) if isCorner else pygame.Surface((CELL_WIDTH, CELL_HEIGHT))
        
    def draw(self, screen):
        #if it's not a corner draw a cell
        if(self.cellImage is None):
            self.drawCell(screen)
        else:
            self.drawCellImage(screen)

    def drawCell(self, screen):
        #Draw stock and spaces for logo and color
        logo_x = 2#self.cell_x + 2
        logo_y = 5#self.cell_y + 5
        cell_color_x = 0#self.cell_x
        cell_color_y = CELL_HEIGHT - CELL_COLOR_HEIGHT#self.cell_y + CELL_HEIGHT - CELL_COLOR_HEIGHT
        cell_rect = pygame.Rect(0, 0, CELL_WIDTH, CELL_HEIGHT)#pygame.Rect(self.cell_x, self.cell_y, CELL_WIDTH, CELL_HEIGHT)
        logorect = pygame.Rect(logo_x, logo_y, CELL_LOGO_WIDTH, CELL_LOGO_HEIGHT)
        colorrect = pygame.Rect(cell_color_x, cell_color_y, CELL_COLOR_WIDTH, CELL_COLOR_HEIGHT)
        pygame.draw.rect(self.surface, WHITE, cell_rect)
        pygame.draw.rect(self.surface, BLACK, logorect)
        pygame.draw.rect(self.surface, self.color, colorrect)

        #Draw stock price
        stock_price = self.font_stock_value.render( str(self.__new_value), True, BLACK)
        price_x = (CELL_WIDTH - (CELL_WIDTH // 2)) - (stock_price.get_width() // 2)
        price_y = cell_color_y - stock_price.get_height() - 30
        self.surface.blit(stock_price, (price_x, price_y))

        scudi_text = self.font_stock_value.render("SCUDI", True, BLACK)
        scudi_x = (CELL_WIDTH - (CELL_WIDTH // 2)) - (scudi_text.get_width() // 2)
        scudi_y = cell_color_y - scudi_text.get_height() - 10
        self.surface.blit(scudi_text, (scudi_x, scudi_y))
        surfaceRotated = None

        if(self.angle != 0):        
            surfaceRotated = pygame.transform.rotate(self.surface, self.angle)
            
        if(surfaceRotated is not None):
            screen.blit(surfaceRotated, (self.cell_x, self.cell_y))
        else:
            screen.blit(self.surface, (self.cell_x, self.cell_y))

    def drawCellImage(self, screen):
        # Disponi l'immagine sulla finestra
        self.surface.blit(self.cellImage, (0, 0))
        
        surfaceRotated = None
        if(self.angle != 0):            
            surfaceRotated = pygame.transform.rotate(self.surface, self.angle)
            
        if(surfaceRotated is not None):
            screen.blit(surfaceRotated, (self.cell_x, self.cell_y))
        else:
            screen.blit(self.surface, (self.cell_x, self.cell_y))
        
    def get_cell_value(self):
        return self.__new_value
    
    def get_stocks(self):
        if self.__stocks is None:
            return None
        return self.__stocks.copy()
    
    def updateCellValue(self, value):
        self.__new_value = value

    def get_index(self):
        return self.__stockIndex
    
    def sell_stock(self):
        if self.__stocks is None:
            return None
        return self.__stocks.pop()
    
    def add_stock(self, stock):
        if self.__stocks is not None:
            self.__stocks.append(stock)